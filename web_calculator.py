import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import re
import itertools
import calculator  # Your custom calculator module

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Graphing Calculator Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #1c1c1c;
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #444;
    }
    .stButton>button:hover {
        background-color: #90EE90;
        color: black;
    }
    .stTextInput>div>div>input {
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #444;
    }
    .sidebar .sidebar-content {
        background-color: #111;
    }
    h1, h2, h3 {
        color: #90EE90 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State for Functions
# -----------------------------------------------------------------------------
if 'functions' not in st.session_state:
    st.session_state.functions = ["sin(x)", "x**2"]

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def evaluate_function(func_str, x_array):
    """Safely evaluates a function string and returns a numpy array"""
    expr = func_str.replace('^', '**')
    replacements = {
        'sqrt': 'np.sqrt', 'sin': 'np.sin', 'cos': 'np.cos', 
        'tan': 'np.tan', 'exp': 'np.exp', 'log': 'np.log', 
        'abs': 'np.abs', 'pi': 'np.pi', 'e': 'np.e'
    }
    for old, new in replacements.items():
        expr = re.sub(r'(?<![a-zA-Z0-9_.])' + old, new, expr)
        
    try:
        # Evaluate with numpy context
        res = eval(expr, {"__builtins__": None}, {"np": np, "x": x_array, "math": math})
        
        # Handle constants
        if np.isscalar(res) or (isinstance(res, np.ndarray) and res.ndim == 0):
            return np.full_like(x_array, res, dtype=float)
        return np.asarray(res, dtype=float)
    except Exception as e:
        return None

# -----------------------------------------------------------------------------
# Sidebar - Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("📊 Settings")
    
    st.subheader("Add Function")
    new_func = st.text_input("f(x) =", placeholder="e.g. sin(x) + 2")
    if st.button("Add to Plot"):
        if new_func and new_func not in st.session_state.functions:
            st.session_state.functions.append(new_func)
            st.rerun()

    st.subheader("Manage Functions")
    for i, func in enumerate(st.session_state.functions):
        cols = st.columns([4, 1])
        cols[0].write(f"`{func}`")
        if cols[1].button("🗑️", key=f"del_{i}"):
            st.session_state.functions.pop(i)
            st.rerun()

    if st.button("Clear All Functions"):
        st.session_state.functions = []
        st.rerun()

    st.divider()
    
    st.subheader("Zoom & Range")
    x_min = st.number_input("X Min", value=-10.0)
    x_max = st.number_input("X Max", value=10.0)
    y_min = st.number_input("Y Min", value=-10.0)
    y_max = st.number_input("Y Max", value=10.0)
    
    st.divider()
    st.markdown("👨‍💻 **Developed By Tamer Elwakeel**")

# -----------------------------------------------------------------------------
# Main Area - Title and Graph
# -----------------------------------------------------------------------------
st.title("🧮 Graphing Calculator Pro")
st.write("A professional graphing tool for iPad, Mobile, and Desktop.")

if not st.session_state.functions:
    st.info("👈 Add a function in the sidebar to start graphing!")
else:
    # --- Prepare Plot ---
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1c1c1c')
    ax.set_facecolor('#1c1c1c')
    
    ax.grid(True, alpha=0.3, color='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    x = np.linspace(x_min, x_max, 1000)
    colors = ['#00ff00', '#ff00ff', '#00ffff', '#ffff00', '#ff8800']
    
    all_y = []
    
    # --- Plot Functions ---
    for i, func_str in enumerate(st.session_state.functions):
        y = evaluate_function(func_str, x)
        if y is not None:
            all_y.append(y)
            color = colors[i % len(colors)]
            ax.plot(x, y, color=color, linewidth=2, label=func_str)
            
            # --- Vertex Detection ---
            dy = np.diff(y)
            extrema_idx = np.where(np.diff(np.sign(dy)))[0] + 1
            for e_idx in extrema_idx:
                xe, ye = x[e_idx], y[e_idx]
                if x_min <= xe <= x_max and y_min <= ye <= y_max:
                    ax.plot(xe, ye, '*', color='#FFD700', markersize=10)
                    ax.annotate(f"({xe:.1f}, {ye:.1f})", (xe, ye), 
                                textcoords="offset points", xytext=(0,-15), 
                                ha='center', color='#FFD700', fontsize=8)

    # --- Intersection Detection ---
    if len(all_y) >= 2:
        for i, j in itertools.combinations(range(len(all_y)), 2):
            diff = all_y[i] - all_y[j]
            crossings = np.where(np.diff(np.sign(diff)))[0]
            for c_idx in crossings:
                x1, x2 = x[c_idx], x[c_idx+1]
                d1, d2 = diff[c_idx], diff[c_idx+1]
                if np.isnan(d1) or np.isnan(d2): continue
                
                # Intersection point
                x_sol = x1 - d1 * (x2 - x1) / (d2 - d1)
                y_sol = all_y[i][c_idx] + (all_y[i][c_idx+1] - all_y[i][c_idx]) * (x_sol - x1) / (x2 - x1)
                
                if y_min <= y_sol <= y_max:
                    ax.plot(x_sol, y_sol, 'wo', markersize=6)
                    ax.annotate(f"Sol: ({x_sol:.1f}, {y_sol:.1f})", (x_sol, y_sol),
                                textcoords="offset points", xytext=(0,10), 
                                ha='center', color='white', fontsize=8,
                                bbox=dict(boxstyle='round,pad=0.2', fc='black', alpha=0.5))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("X")
    ax.set_ylabel("f(X)")
    if st.session_state.functions:
        legend = ax.legend(loc='upper right', facecolor='#2d2d2d', edgecolor='white')
        for text in legend.get_texts():
            text.set_color('white')
            
    st.pyplot(fig)

# -----------------------------------------------------------------------------
# Professional Calculator GUI
# -----------------------------------------------------------------------------
st.divider()

# Wrapper container for the calculator to apply scoped CSS if possible, 
# but for now we rely on the specific button order.

st.markdown("""
<style>
    /* Display Screen Styles (Custom Div) */
    .calc-display {
        font-family: 'Courier New', Courier, monospace;
        font-size: 2.5rem;
        background-color: #000000;
        color: #fff;
        text-align: right;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px; /* Space between screen and buttons */
        border: 1px solid #333;
        min-height: 70px;
        box-shadow: inset 0 0 10px rgba(255,255,255,0.1);
    }
    
    /* Responsive Calculator Container
       On Mobile (Portrait): Takes full width naturally.
       On Desktop/Tablet: Restricts width to simulate a phone/calculator size.
    */
    .main .stHorizontalBlock {
        max-width: 500px;
        margin: 0 auto !important;
    }
    
    /* Ensure the display matches the button grid width */
    div[data-testid="stMarkdownContainer"] > div.calc-display {
        max-width: 500px;
        margin: 0 auto;
    }

    /* Button Styles */
    div.stButton > button {
        width: 100%;
        aspect-ratio: 1 / 1; /* Make buttons perfectly circular/square-ish */
        border-radius: 50%;
        font-size: 22px;
        font-weight: 500;
        border: none;
        margin-bottom: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.1s;
    }
    
    div.stButton > button:active {
        transform: scale(0.95);
    }

    /* Colors */
    div.stButton > button { background-color: #333; color: white; }
    div.stButton > button[kind="primary"] { background-color: #ff9f0a !important; color: white !important; }

</style>
""", unsafe_allow_html=True)

st.subheader(" Calculator")

# Logic
if "calc_expression" not in st.session_state:
    st.session_state.calc_expression = ""

def calc_press(val):
    if val == "C":
        st.session_state.calc_expression = ""
    elif val == "=":
        try:
            expr = st.session_state.calc_expression
            expr = expr.replace('×', '*').replace('÷', '/')
            expr = expr.replace('^', '**').replace('π', 'math.pi')
            expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos')
            expr = expr.replace('tan', 'math.tan').replace('√', 'math.sqrt')
            res = eval(expr, {"__builtins__": None}, {"math": math, "abs": abs})
            if isinstance(res, float) and res.is_integer():
                res = int(res)
            st.session_state.calc_expression = str(res)
        except:
            st.session_state.calc_expression = "Error"
    elif val == "⌫":
        st.session_state.calc_expression = st.session_state.calc_expression[:-1]
    else:
        st.session_state.calc_expression += str(val)

# --- Calculator UI ---

# Display Screen
st.markdown(f"""<div class='calc-display'>{st.session_state.calc_expression if st.session_state.calc_expression else "0"}</div>""", unsafe_allow_html=True)

# Define Keyboard Layout
# [Label, Value, type]
buttons = [
    ("sin", "sin(", "default"), ("cos", "cos(", "default"), ("tan", "tan(", "default"), ("C", "C", "primary"),
    ("√", "sqrt(", "default"),  ("^", "^", "default"),      ("π", "pi", "default"),     ("⌫", "⌫", "primary"),
    ("7", "7", "default"),      ("8", "8", "default"),      ("9", "9", "default"),      ("÷", "÷", "primary"),
    ("4", "4", "default"),      ("5", "5", "default"),      ("6", "6", "default"),      ("×", "×", "primary"),
    ("1", "1", "default"),      ("2", "2", "default"),      ("3", "3", "default"),      ("−", "-", "primary"),
    ("0", "0", "default"),      (".", ".", "default"),      ("(", "(", "default"),      ("+", "+", "primary"),
    (")", ")", "default"),      ("", "", "default"),        ("", "", "default"),        ("=", "=", "primary"),
]

# Render Grid
idx = 0
for row in range(7):
        # Nested columns for the button grid
        cols = st.columns(4, gap="small")
        for c in cols:
            if idx < len(buttons):
                label, val, kind = buttons[idx]
                if label:
                    # We use the type='primary' to trigger the orange CSS we wrote above
                    if kind == 'primary':
                        c.button(label, on_click=calc_press, args=(val,), type="primary", use_container_width=True)
                    else:
                        c.button(label, on_click=calc_press, args=(val,), use_container_width=True)
                idx += 1

st.markdown("""
---
### 💡 How to use on iPad:
1. Open this link in **Safari**.
2. Tap the **Share icon** (square with arrow).
3. Select **"Add to Home Screen"**.
4. Now it works like a real app!
---
✨ **Developed By Tamer Elwakeel** | *Python Diploma 2024*
""")
