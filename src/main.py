import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Ensure src module is in path if run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui.main_window import MainWindow
from src.controllers.template_controller import AppController
from src.i18n import translator
from src.i18n.locale_loader import LocaleLoader
from src.services.preferences_service import PreferencesService

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Modern look across platforms
    
    from PySide6.QtGui import QIcon
    # Resolve resource path for PyInstaller
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    icon_path = os.path.join(base_path, "resources", "app_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Bootstrap i18n
    lang = PreferencesService.get_language()
    active = LocaleLoader.load(lang)
    fallback = LocaleLoader.load_english()
    translator.load(active, fallback)
    
    app_controller = AppController()
    window = MainWindow(app_controller)
    app_controller.set_main_window(window)
    
    # Open initial empty tab
    app_controller.new_template()
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
