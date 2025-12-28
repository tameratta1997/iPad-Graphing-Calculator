# How to Create the Windows version (.exe)

Since you are currently working on macOS, I cannot directly generate a Windows `.exe` file for you (cross-compilation is tricky and often fails).

However, I have prepared all the necessary files so you can easily build it on any Windows machine.

### Instructions:

1.  **Copy the Project Folder**: Copy the entire `Python_Diploma` folder to a Windows computer.
2.  **Install Python**: Ensure Python is installed on the Windows machine.
3.  **Run the Build Script**:
    *   Open the folder in Windows File Explorer.
    *   Double-click the `build_windows.bat` file I created.
    *   This script will automatically:
        *   Install the required libraries (`numpy`, `matplotlib`, `pyinstaller`, etc.)
        *   Build the standalone `.exe` file using the correct icon.

### Troubleshooting: "pip is not recognized" error?

If you see an error saying `'pip' is not recognized` or `'python' is not found`:

1.  It means Python is installed but **not added to your system PATH**.
2.  **To Fix:**
    *   Re-install Python.
    *   **CRITICAL STEP**: On the very first screen of the installer, look at the bottom and check the box that says:
        *   **[x] Add Python to environment variables** (or **Add to PATH**)
    *   Once checked, click Install.
    *   Run `build_windows.bat` again.

4.  **Find the output**: 
    *   Once the script finishes, check your **Desktop**.
    *   You will find `ScientificCalculator.exe`. 
    *   You can copy this single file anywhere and run it without needing Python installed.
