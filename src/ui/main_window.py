from PySide6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                               QMenuBar, QMenu, QFileDialog, QMessageBox, QHBoxLayout, QPushButton)
from PySide6.QtGui import QAction, QScreen
from PySide6.QtCore import Qt
from src.i18n import t

class MainWindow(QMainWindow):
    def __init__(self, app_controller):
        super().__init__()
        self.app_controller = app_controller
        self.setWindowTitle(t("window.title"))
        
        # Responsive sizing
        screen: QScreen = self.screen()
        geom = screen.availableGeometry()
        self.resize(int(geom.width() * 0.8), int(geom.height() * 0.8))
        
        self.setup_ui()
        
    def setup_ui(self):
        # Central Tab Widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.app_controller.close_tab)
        self.setCentralWidget(self.tab_widget)
        
        # Menu
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu(t("menu.file"))
        
        new_action = QAction(t("menu.file.new_template"), self)
        new_action.triggered.connect(self.app_controller.new_template)
        file_menu.addAction(new_action)
        
        open_action = QAction(t("menu.file.open_template"), self)
        open_action.triggered.connect(self.app_controller.open_template)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        batch_action = QAction(t("menu.file.run_batch"), self)
        batch_action.triggered.connect(self.app_controller.run_batch)
        file_menu.addAction(batch_action)

        # Edit Menu
        edit_menu = menubar.addMenu(t("menu.edit"))
        
        settings_action = QAction(t("menu.edit.settings") if t("menu.edit.settings") != "menu.edit.settings" else "Settings", self)
        settings_action.triggered.connect(self.app_controller.open_settings)
        edit_menu.addAction(settings_action)
        
        # Help Menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
    def show_about_dialog(self):
        # We can read the version from metadata, but for now hardcode per spec
        QMessageBox.about(
            self,
            "About PDF Data Extractor",
            "<h3>PDF Data Extractor</h3>"
            "<p>Version: 1.0.0</p>"
            "<p>Author: github-spec-kit</p>"
            "<p>Copyright (c) 2026 github-spec-kit</p>"
            "<p>A modern PySide6-based application for extracting structured data from PDF files using rule-based templates.</p>"
        )
        
    def add_workspace_tab(self, widget, title=None):
        if title is None:
            title = t("menu.file.new_template")
        index = self.tab_widget.addTab(widget, title)
        self.tab_widget.setCurrentIndex(index)
        return index
        
    def remove_workspace_tab(self, index):
        self.tab_widget.removeTab(index)

    def rename_workspace_tab(self, index: int, title: str):
        """Update the title of the tab at the given index."""
        self.tab_widget.setTabText(index, title)
