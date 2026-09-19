# Research: App Installer & Branding

## Bundling Tool Selection

- **Decision**: Use `PyInstaller`.
- **Rationale**: PyInstaller is the industry standard for packaging Python applications, especially those using PySide6. It supports single-file executables (`--onefile`), can easily bundle external assets like icons and locale files, and has robust support for embedding Windows version/author metadata (via `--version-file`). It is also cross-platform, meaning it can be run on macOS or Linux if needed in the future.
- **Alternatives Considered**: 
  - **Nuitka**: Compiles Python to C before building an executable. It offers performance benefits and better obfuscation, but configuring it to properly include all Qt plugins and assets can be very complex.
  - **cx_Freeze**: A solid alternative, but typically generates a folder with many DLLs rather than a clean single-file executable by default. PyInstaller's `.spec` file system is more flexible for our asset bundling needs.

## Icon Generation

- **Decision**: Use the AI-generated app icon.
- **Rationale**: The user requested a professional icon. We have generated a high-quality square image featuring a PDF document with a magnifying glass and extraction brackets. We will convert this image to `.ico` and `.png` formats to use for the Windows executable and the PySide6 `QApplication` window icon.

## Windows Metadata

- **Decision**: Use a PyInstaller version info file.
- **Rationale**: PyInstaller provides a built-in way to embed metadata (Author, Version, Copyright, Description) into the Windows PE header using a `version_info.txt` file. This satisfies the requirement to display author information in the executable properties.
