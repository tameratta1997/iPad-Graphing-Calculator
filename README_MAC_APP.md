# Calculator Mac App

## ✅ Your Calculator is now a Mac Application!

The calculator has been successfully converted to a native macOS application bundle.

### 📍 Location
The app is located at:
```
/Users/tamerelwakeel/Documents/Python_Projects/Python_Diploma/dist/Calculator.app
```

### 🚀 How to Use

1. **Double-click** `Calculator.app` in the `dist` folder to launch it
2. Or use Finder to navigate to the `dist` folder and open it
3. You can also drag it to your Applications folder for easier access

### 📦 Moving to Applications Folder

To install it like a regular Mac app:

```bash
cp -r dist/Calculator.app /Applications/
```

Or simply drag `Calculator.app` from the `dist` folder to your Applications folder in Finder.

### 🎨 Features

- **Basic Mode**: Standard calculator with basic operations
- **Scientific Mode**: Advanced functions including:
  - Trigonometry (sin, cos, tan and their inverses)
  - Logarithms (ln, log10)
  - Powers and roots (x², x³, x^y, √x, ³√x, ʸ√x)
  - Hyperbolic functions
  - Constants (π, e)
  - Factorial, random numbers
- **Programmer Mode**: 
  - Multiple number bases (HEX, DEC, OCT, BIN)
  - Bitwise operations (AND, OR, XOR, NOT, <<, >>)

### 🔄 Rebuilding the App

If you make changes to the Python code, rebuild the app with:

```bash
# Clean previous build
rm -rf build dist

# Rebuild
python3 setup.py py2app
```

### 📤 Sharing the App

You can share the `Calculator.app` with other Mac users by:

1. **Compress it**: Right-click → Compress "Calculator.app"
2. **Share the .zip file**: The recipient can extract and run it

**Note**: For distribution outside your Mac, you may need to:
- Sign the app with an Apple Developer certificate
- Notarize it with Apple
- Otherwise, users will need to right-click → Open (first time only) to bypass Gatekeeper

### 🛠️ Technical Details

- Built with: py2app
- Python version: 3.13
- GUI Framework: Tkinter
- Architecture: Universal (x86_64 + ARM64)
- Bundle ID: com.calculator.app

### 📝 Files

- `gui_calculator.py` - Main GUI application
- `calculator.py` - Calculator logic module
- `setup.py` - py2app configuration
- `dist/Calculator.app` - The final Mac application

---

Enjoy your Calculator app! 🎉
