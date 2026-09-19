# Quickstart Validation Guide: App Installer & Branding

This guide describes how to validate the bundled application.

## Prerequisites

- Windows OS
- Python 3.11+ (for building only)
- PyInstaller installed (`pip install pyinstaller`)

## 1. Build the Executable

Run the build script from the repository root:

```bash
python build_app.py
```

**Expected Outcome**: A `dist/` folder is created containing `PDFExtractor.exe`.

## 2. Verify Metadata and Icon

1. Navigate to the `dist/` directory in Windows File Explorer.
2. Verify that `PDFExtractor.exe` has the custom app icon (magnifying glass over PDF).
3. Right-click `PDFExtractor.exe` -> **Properties** -> **Details** tab.
4. Verify the Author, Version (e.g., 1.0.0), and Copyright information match the project metadata.

## 3. Run the Standalone App

Double-click `PDFExtractor.exe` to launch the application.

**Expected Outcome**:
- The application launches successfully without opening a terminal window (`--noconsole`).
- The application window displays the custom app icon in the title bar and taskbar.
- The UI language loads correctly (proving that `locales/` were bundled properly).

## 4. Verify "About" Dialog

In the running application, click **Help** -> **About**.

**Expected Outcome**:
- A dialog opens displaying the application name, version, author, and description.
