from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QMessageBox)
from PySide6.QtGui import QFont
from src.i18n import t

class SettingsDialog(QDialog):
    def __init__(self, preferences, available_languages, parent=None):
        super().__init__(parent)
        self.preferences = preferences
        self.available_languages = available_languages
        self.setWindowTitle(t("settings.title"))
        self.setMinimumWidth(300)
        self.setup_ui()
        self.load_preferences()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Language Selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel(t("settings.label.language"))
        self.lang_combo = QComboBox()
        self.lang_combo.setToolTip(t("tooltip.settings.language"))
        
        # Populate language combo box
        self.lang_codes = []
        for code, name in self.available_languages.items():
            self.lang_combo.addItem(name)
            self.lang_codes.append(code)
            
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_ok = QPushButton(t("btn.ok"))
        self.btn_cancel = QPushButton(t("btn.cancel"))
        
        self.btn_ok.clicked.connect(self.on_ok)
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

    def load_preferences(self):
        current_lang = self.preferences.get_language()
        if current_lang in self.lang_codes:
            index = self.lang_codes.index(current_lang)
            self.lang_combo.setCurrentIndex(index)

    def on_ok(self):
        selected_index = self.lang_combo.currentIndex()
        if selected_index >= 0 and selected_index < len(self.lang_codes):
            selected_code = self.lang_codes[selected_index]
            current_lang = self.preferences.get_language()
            
            if selected_code != current_lang:
                self.preferences.set_language(selected_code)
                QMessageBox.information(self, t("msg.info"), t("settings.info.restart"))
                
        self.accept()
