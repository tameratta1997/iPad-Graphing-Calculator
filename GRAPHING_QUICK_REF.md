# 📊 Graphing Calculator - Quick Reference

## 🎯 Function Syntax Quick Guide

### Basic Operations
```
Addition:       x + 5
Subtraction:    x - 3
Multiplication: 2*x        (must use *)
Division:       x/2
Power:          x**2  or  x^2
```

### Common Functions
```
sin(x)          Sine
cos(x)          Cosine
tan(x)          Tangent
sqrt(x)         Square root
exp(x)          e^x
log(x)          Natural logarithm (ln)
abs(x)          Absolute value
```

### Example Functions
```
SIMPLE:
x                  Linear
x**2               Parabola
sin(x)             Sine wave
1/x                Hyperbola

INTERMEDIATE:
x**3 - 2*x         Cubic
sin(2*x)           Fast sine
sqrt(x + 5)        Shifted root
exp(-x)            Decay

ADVANCED:
sin(x) * exp(-x/10)        Damped oscillation
x**2 * cos(x)              Modulated parabola
sin(x) / x                 Sinc function
exp(-x**2)                 Gaussian bell curve
```

## 🎨 4 Calculator Modes

| Mode | Icon | Features |
|------|------|----------|
| **Basic** | 🔢 | 0-9, +, -, ×, ÷, %, +/- |
| **Scientific** | 🔬 | sin, cos, log, √, x², π, e |
| **Programmer** | 💻 | HEX, BIN, AND, OR, XOR, << |
| **Graphing** | 📊 | Plot functions, zoom, multiple graphs |

## ⌨️ Quick Actions

### In Graphing Mode
- **Enter** = Plot function
- **Type function** → Click "Plot"
- **Click quick button** = Instant plot
- **Select function** → "Remove" = Delete it
- **"Clear All"** = Remove all functions

### Switch Modes
1. Click **■** (top right)
2. Select mode from menu

## 🎯 Pro Tips

✅ **DO:**
- Use `*` for multiplication: `2*x`
- Use `**` for powers: `x**3`
- Use parentheses: `sin(2*x + 1)`
- Start with simple functions
- Adjust ranges if graph is blank

❌ **DON'T:**
- Write `2x` (use `2*x`)
- Write `x2` (use `x**2`)
- Forget the variable `x`

## 📐 Default Settings
- **X Range:** -10 to 10
- **Y Range:** -10 to 10
- **Resolution:** 1000 points
- **Colors:** Green, Magenta, Cyan, Yellow, Orange

## 🚀 Getting Started (3 Steps)
1. Open calculator → Click **■** → Select "Graphing"
2. Type `sin(x)` in the input box
3. Press **Enter** or click **Plot**

**That's it!** You're graphing! 🎉

---

## 📱 File Locations

```
gui_calculator_graphing.py     Main application
setup_graphing.py              Build Mac app
GRAPHING_CALCULATOR_GUIDE.md   Full documentation
```

## 🔧 Build Mac App

```bash
python3 setup_graphing.py py2app
cp -r dist/Graphing\ Calculator.app /Applications/
```

---

**Happy Graphing!** 📊✨
