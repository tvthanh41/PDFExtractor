import pymupdf as fitz
from PySide6.QtWidgets import QFileDialog, QMessageBox
from src.domain.models import Template, BoundingBox
from src.domain.enums import RuleType
from src.services.template_repository import TemplateRepository
from src.strategies.factory import ExtractionStrategyFactory
from src.ui.rule_dialog import RuleDialog
from src.ui.workspace_tab import WorkspaceTabWidget
from src.ui.preview_dialog import PreviewDialog
from src.ui.rule_preview_dialog import RulePreviewDialog
from src.controllers.batch_controller import BatchController
from src.i18n import t

class AppController:
    """Manages the application lifecycle and multiple template tabs."""
    def __init__(self):
        self.main_window = None
        self.template_controllers = [] # list of TemplateController

    def set_main_window(self, main_window):
        self.main_window = main_window

    def rename_tab_for_controller(self, controller):
        """Update the tab title for the given controller's view."""
        if not self.main_window:
            return
            
        try:
            index = self.template_controllers.index(controller)
            self.main_window.rename_workspace_tab(index, controller.template.name)
        except ValueError:
            pass

    def new_template(self):
        controller = TemplateController(app_controller=self)
        view = WorkspaceTabWidget(controller)
        controller.set_view(view)
        
        self.template_controllers.append(controller)
        if self.main_window:
            self.main_window.add_workspace_tab(view, controller.template.name)

    def open_template(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self.main_window, t("menu.file.open_template").replace("...", ""), "", "Template Files (*.pdftpl)"
        )
        if file_name:
            template = TemplateRepository.load(file_name)
            controller = TemplateController(template, app_controller=self)
            view = WorkspaceTabWidget(controller)
            controller.set_view(view)
            
            # populate table
            for rule in template.rules:
                view.add_rule_to_table(rule)
                
            self.template_controllers.append(controller)
            if self.main_window:
                self.main_window.add_workspace_tab(view, template.name)

    def close_tab(self, index):
        if not self.main_window:
            return
        # Could add unsaved changes prompt here
        self.main_window.remove_workspace_tab(index)
        if index < len(self.template_controllers):
            self.template_controllers.pop(index)

    def run_batch(self):
        from src.ui.batch_config_dialog import BatchConfigDialog
        dialog = BatchConfigDialog(self.main_window)
        if dialog.exec():
            batch_ctrl = BatchController(self.main_window)
            batch_ctrl.start_batch(dialog.template_path, dialog.input_dir, dialog.output_csv)

    def open_settings(self):
        from src.ui.settings_dialog import SettingsDialog
        from src.services.preferences_service import PreferencesService
        from src.i18n.locale_loader import LocaleLoader
        dialog = SettingsDialog(PreferencesService, LocaleLoader.discover(), self.main_window)
        dialog.exec()


class TemplateController:
    """Manages a single template workspace tab."""
    def __init__(self, template=None, app_controller=None):
        self.template = template if template else Template(name=t("menu.file.new_template"))
        self.app_controller = app_controller
        self.view = None
        self.current_pdf_path = None
        self.doc = None
        self.selected_rule_id = None

    def set_view(self, view):
        self.view = view

    def open_pdf(self):
        if not self.view: return
        file_name, _ = QFileDialog.getOpenFileName(
            self.view, t("btn.open_pdf"), "", "PDF Files (*.pdf)"
        )
        if file_name:
            self.current_pdf_path = file_name
            self.doc = fitz.open(file_name)
            self.view.canvas.load_document(file_name)

    def add_rule(self):
        if not self.view: return
        dialog = RuleDialog(self.view)
        if dialog.exec():
            rule = dialog.get_rule()
            self.template.rules.append(rule)
            self.view.add_rule_to_table(rule)

    def add_box_rule(self, box: BoundingBox):
        if not self.view: return
        dialog = RuleDialog(self.view, predefined_box=box)
        if dialog.exec():
            rule = dialog.get_rule()
            self.template.rules.append(rule)
            self.view.add_rule_to_table(rule)

    def edit_rule(self, index: int):
        if not self.view: return
        if index < 0 or index >= len(self.template.rules):
            return
        rule = self.template.rules[index]
        dialog = RuleDialog(self.view, rule=rule)
        if dialog.exec():
            updated_rule = dialog.get_rule()
            self.template.rules[index] = updated_rule
            self.view.update_rule_in_table(index, updated_rule)
            
    def reselect_rule_region(self, index: int):
        if not self.view: return
        if index < 0 or index >= len(self.template.rules):
            return
        rule = self.template.rules[index]
        if getattr(rule, 'rule_type', None) != RuleType.BOUNDING_BOX:
            self.view.show_error(t("msg.not_box_rule") if t("msg.not_box_rule") != "msg.not_box_rule" else "Cannot reselect region for non-bounding box rules.")
            return
        self.reselecting_row = index
        self.view.toggle_box_mode()

    def finish_reselect_rule_region(self, box: BoundingBox):
        if not self.view: return
        if not hasattr(self, 'reselecting_row') or self.reselecting_row is None:
            return
        index = self.reselecting_row
        self.reselecting_row = None
        if index < 0 or index >= len(self.template.rules):
            return
        rule = self.template.rules[index]
        rule.box = box
        self.template.rules[index] = rule
        self.select_rule(index)

    def delete_rule(self, index: int):
        if not self.view: return
        if index < 0 or index >= len(self.template.rules):
            return
        self.template.rules.pop(index)
        self.view.rules_table.removeRow(index)
        self.select_rule(-1)
            
    def select_rule(self, index: int):
        if not self.view: return
        if index < 0 or index >= len(self.template.rules):
            self.selected_rule_id = None
            self.view.update_preview("None")
            if hasattr(self.view, 'canvas') and self.view.canvas:
                self.view.canvas.highlight_box(None)
            return
            
        rule = self.template.rules[index]
        self.selected_rule_id = getattr(rule, 'rule_id', None)
        
        if self.doc:
            try:
                strategy = ExtractionStrategyFactory.create(rule)
                val = strategy.extract(self.doc, self.view.canvas.current_page)
                self.view.update_preview(str(val))
            except Exception as e:
                self.view.update_preview(f"Error: {str(e)}")
        else:
            self.view.update_preview("None")
            
        if hasattr(self.view, 'canvas') and self.view.canvas:
            if getattr(rule, 'rule_type', None) == RuleType.BOUNDING_BOX:
                self.view.canvas.highlight_box(getattr(rule, 'box', None))
            else:
                self.view.canvas.highlight_box(None)

    def save_template(self):
        if not self.view: return
        if not self.template.rules:
            self.view.show_error(t("msg.cannot_save_empty"))
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self.view, t("btn.save_template"), f"{self.template.name}.pdftpl", "Template Files (*.pdftpl)"
        )
        if file_name:
            TemplateRepository.save(self.template, file_name)
            # Notify app controller to rename the tab
            if self.app_controller:
                self.app_controller.rename_tab_for_controller(self)
            self.view.show_info(t("msg.saved_ok").format(path=file_name))

    def preview_extraction(self):
        if not self.view: return
        if not self.doc:
            self.view.show_error(t("msg.no_pdf"))
            return
            
        if not self.template.rules:
            self.view.show_error(t("msg.no_rules_preview"))
            return
            
        results = {}
        page_num = self.view.canvas.current_page
        
        for rule in self.template.rules:
            strategy = ExtractionStrategyFactory.create(rule)
            val = strategy.extract(self.doc, page_num)
            results[getattr(rule, 'key_name', str(rule))] = val
            
        import os, datetime, getpass
        metadata = {}
        metadata["file name"] = os.path.basename(self.current_pdf_path) if self.current_pdf_path else "Unknown"
        metadata["file path"] = self.current_pdf_path if self.current_pdf_path else "Unknown"
        metadata["generated time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            metadata["user"] = getpass.getuser()
        except Exception:
            metadata["user"] = "Unknown"
        metadata["template name"] = self.template.name
        
        final_results = metadata.copy()
        final_results.update(results)
            
        dialog = PreviewDialog(final_results, self.view)
        dialog.exec()

    def preview_single_rule(self, index: int):
        if not self.view: return
        if not self.doc:
            self.view.show_error(t("msg.no_pdf_preview"))
            return
            
        if index < 0 or index >= len(self.template.rules):
            return
            
        rule = self.template.rules[index]
        page_num = self.view.canvas.current_page
        
        try:
            strategy = ExtractionStrategyFactory.create(rule)
            val = strategy.extract(self.doc, page_num)
            
            dialog = RulePreviewDialog(getattr(rule, 'key_name', str(rule)), val, self.view)
            dialog.exec()
        except Exception as e:
            self.view.show_error(t("msg.failed_preview").format(error=str(e)))

