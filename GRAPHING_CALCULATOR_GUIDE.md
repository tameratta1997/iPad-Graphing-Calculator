# 📊 Graphing Calculator - User Guide

## 🎉 New Feature: Function Graphing!

Your calculator now includes a powerful **Graphing Mode** that can plot any mathematical function!

## 🚀 Quick Start

1. **Run the calculator:**
   ```bash
   python3 gui_calculator_graphing.py
   ```

2. **Switch to Graphing mode:**
   - Click the ■ button (top right)
   - Select "Graphing"

3. **Plot your first function:**
   - Type a function in the input box (e.g., `sin(x)`)
   - Click "Plot" or press Enter
   - Watch your function appear on the graph!

## 📐 Graphing Mode Features

### Function Input
- **Syntax:** Use `x` as your variable
- **Examples:**
  - `sin(x)` - Sine wave
  - `x**2` - Parabola
  - `sqrt(x)` - Square root
  - `exp(x)` - Exponential
  - `1/x` - Hyperbola
  - `x**3 - 2*x + 1` - Cubic polynomial

### Supported Functions
| Function | Syntax | Example |
|----------|--------|---------|
| **Trigonometric** | `sin(x)`, `cos(x)`, `tan(x)` | `sin(2*x)` |
| **Powers** | `x**n` or `x^n` | `x**3` |
| **Square Root** | `sqrt(x)` | `sqrt(x+5)` |
| **Exponential** | `exp(x)` | `exp(-x)` |
| **Logarithm** | `log(x)` | `log(x**2)` |
| **Absolute Value** | `abs(x)` | `abs(sin(x))` |

### Quick Function Buttons
Click any quick function button to instantly plot:
- `sin(x)` - Sine wave
- `cos(x)` - Cosine wave
- `x²` - Quadratic
- `x³` - Cubic
- `√x` - Square root
- `1/x` - Reciprocal
- `e^x` - Exponential growth
- `ln(x)` - Natural logarithm

### Multiple Functions
- Plot multiple functions simultaneously
- Each function gets a different color
- Functions are listed in the function list
- Remove individual functions with the "Remove" button
- Clear all functions with "Clear All"

### Zoom & Pan Controls

**X Range:** Control horizontal viewing window
- Default: -10 to 10
- Example: Set to -5 to 5 for closer view

**Y Range:** Control vertical viewing window
- Default: -10 to 10
- Example: Set to 0 to 100 for positive values only

**Update Button:** Apply new range settings

### Graph Features
- ✅ **Grid lines** for easy reading
- ✅ **Axis labels** (x and f(x))
- ✅ **Legend** showing all plotted functions
- ✅ **Dark theme** matching calculator design
- ✅ **High resolution** 1000 points per function
- ✅ **Auto-scaling** with manual override

## 🎯 Example Use Cases

### 1. Comparing Trigonometric Functions
```
Plot: sin(x)
Plot: cos(x)
Plot: tan(x)
X Range: -10 to 10
Y Range: -2 to 2
```

### 2. Polynomial Analysis
```
Plot: x**2
Plot: x**3
Plot: x**4
X Range: -3 to 3
Y Range: -10 to 10
```

### 3. Exponential vs Logarithmic
```
Plot: exp(x)
Plot: log(x)
X Range: -2 to 5
Y Range: -2 to 10
```

### 4. Custom Complex Functions
```
Plot: sin(x) * exp(-x/10)
Plot: x**2 * cos(x)
Plot: sqrt(abs(x)) * sin(x)
```

## 🧮 All Calculator Modes

### 1. **Basic Mode**
Standard calculator with:
- Numbers 0-9
- Operations: +, -, ×, ÷
- Functions: AC, +/-, %
- Perfect for everyday calculations

### 2. **Scientific Mode**
Advanced mathematics:
- Trigonometry: sin, cos, tan (and inverses)
- Logarithms: ln, log₁₀
- Powers: x², x³, xʸ, 2ˣ
- Roots: √x, ³√x, ʸ√x
- Hyperbolic functions
- Constants: π, e
- Factorial, random numbers

### 3. **Programmer Mode**
Number systems and bitwise operations:
- Bases: HEX, DEC, OCT, BIN
- Bitwise: AND, OR, XOR, NOT
- Shifts: <<, >>
- Hexadecimal digits: A-F

### 4. **Graphing Mode** ⭐ NEW!
Function visualization:
- Plot any mathematical function
- Multiple functions simultaneously
- Adjustable viewing window
- Quick function templates
- Interactive controls

## 🔧 Building as Mac App

To create a standalone Mac application:

```bash
# Build the graphing calculator app
python3 setup_graphing.py py2app

# Install to Applications
cp -r dist/Graphing\ Calculator.app /Applications/

# Add to Dock
open /Applications/Graphing\ Calculator.app
# Then: Right-click icon → Options → Keep in Dock
```

## 💡 Tips & Tricks

### Graphing Tips
1. **Start simple:** Test with `sin(x)` or `x**2` first
2. **Adjust ranges:** If you don't see your function, try wider ranges
3. **Use parentheses:** For complex expressions like `sin(2*x + 1)`
4. **Combine functions:** Try `sin(x) + cos(x)`
5. **Experiment:** The calculator validates functions automatically

### Function Syntax
- **Multiplication:** Use `*` explicitly (e.g., `2*x` not `2x`)
- **Powers:** Use `**` or `^` (e.g., `x**2` or `x^2`)
- **Division:** Use `/` (e.g., `1/x`)
- **Nested functions:** `sin(cos(x))` works!

### Common Errors
- **"Error in function":** Check your syntax
  - Use `*` for multiplication: `2*x` not `2x`
  - Use `**` for powers: `x**2` not `x2`
- **Function not visible:** Adjust Y range
- **Vertical lines:** Function may have discontinuities (e.g., `tan(x)`)

## 🎨 Color Scheme
Functions are plotted in vibrant colors:
1. 🟢 Green
2. 🟣 Magenta
3. 🔵 Cyan
4. 🟡 Yellow
5. 🟠 Orange

Colors cycle if you plot more than 5 functions.

## ⌨️ Keyboard Shortcuts
- **Enter:** Plot the current function
- **Mode switching:** Click ■ button (top right)

## 📝 Technical Details

### Dependencies
- **Python 3.13**
- **tkinter:** GUI framework
- **numpy:** Numerical computations
- **matplotlib:** Graph plotting
- **calculator.py:** Math operations module

### Graph Resolution
- 1000 points per function for smooth curves
- Adjustable via code if needed

### Performance
- Handles complex functions efficiently
- Multiple functions plotted simultaneously
- Real-time updates when changing ranges

## 🆘 Troubleshooting

**Q: Graph is blank**
- Check if function is valid
- Try wider X/Y ranges
- Ensure function uses `x` as variable

**Q: Function won't plot**
- Verify syntax (use `*` for multiplication)
- Check for typos in function names
- Try a simple function first (e.g., `x`)

**Q: App won't start**
- Ensure matplotlib and numpy are installed:
  ```bash
  pip3 install matplotlib numpy
  ```

**Q: Graph looks choppy**
- This is normal for functions with discontinuities (like `tan(x)`)
- Try adjusting the Y range to see more detail

## 🌟 Example Functions to Try

### Beautiful Patterns
```
sin(x) * cos(x)
sin(x**2)
exp(-x**2)
x * sin(10/x)
sin(x) / x
```

### Mathematical Curves
```
x**3 - 3*x**2 + 2*x
sqrt(abs(x))
1 / (1 + x**2)
exp(-abs(x))
```

### Oscillations
```
sin(x) * exp(-x/5)
cos(x) + sin(2*x)
sin(x) + sin(3*x) / 3
```

---

## 🎓 Learning Resources

Use the graphing calculator to:
- **Visualize** mathematical concepts
- **Explore** function behavior
- **Compare** different functions
- **Verify** calculus homework
- **Discover** mathematical patterns

---

**Enjoy your new Graphing Calculator!** 🎉📊

For questions or issues, the calculator validates all inputs and provides helpful error messages.
