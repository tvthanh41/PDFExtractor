import os
import subprocess
import sys

def main():
    print("Building PDF Data Extractor standalone executable...")
    
    # Path to main entry point
    main_script = os.path.join("src", "main.py")
    
    # Base PyInstaller arguments
    args = [
        sys.executable, "-m", "PyInstaller",
        "--name", "PDFExtractor",
        "--noconsole",
        "--onefile",
        "--clean",
        "--add-data", f"src/i18n/locales{os.pathsep}src/i18n/locales",
        "--add-data", f"resources{os.pathsep}resources",
        "--icon", os.path.join("resources", "app_icon.ico"),
        "--version-file", "file_version_info.txt"
    ]
    
    # Run PyInstaller
    print(f"Running command: {' '.join(args)} {main_script}")
    result = subprocess.run(args + [main_script])
    
    if result.returncode == 0:
        print("Build completed successfully. Check the 'dist' directory.")
    else:
        print(f"Build failed with exit code {result.returncode}.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
