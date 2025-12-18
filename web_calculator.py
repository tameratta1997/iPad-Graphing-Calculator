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
# Professional Header with Photo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("tamer_photo.jpg", width=120)
with col2:
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
    /* ---------------------------------------------------------------------
       1. LAYOUT CONTAINER (The "Phone" Box)
       --------------------------------------------------------------------- */
    
    /* 
       Target the main block containing the calculator.
       We want it to act like a mobile phone screen regardless of the device.
       
       LANDSCAPE MODE (Desktop/iPad Horizontal):
       The limiting factor is Height. We set width relative to height (e.g., 60% of height).
       
       PORTRAIT MODE (Phone/iPad Vertical):
       The limiting factor is Width. We set width to almost 100%.
    */
    
    .main .block-container {
        max-width: 100% !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important; 
        padding-right: 1rem !important;
    }

    /* We wrap the calculator content in a specific width-constrained block via CSS on the Streamlit grid */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        width: 100% !important;
        margin: 0 auto !important;
        
        /* 
           STRICT SIZE CONTROL:
           Set to 380px (Typical Smartphone Width).
           This ensures it looks like a real handheld calculator on Desktop,
           rather than a giant poster.
        */
        max-width: 380px !important; 
    }

    /* ---------------------------------------------------------------------
       2. DISPLAY SCREEN
       --------------------------------------------------------------------- */
    .calc-display {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 3rem; /* Reduced from 4rem for better fit */
        background-color: transparent; 
        color: #fff;
        text-align: right;
        border: none;
        margin-bottom: 0px;
        padding-right: 10px;
        line-height: 1.2;
    }

    /* ---------------------------------------------------------------------
       3. ROUND BUTTONS
       --------------------------------------------------------------------- */
    div.stButton > button {
        width: 100% !important;
        height: auto !important;
        aspect-ratio: 1 / 1 !important; /* FORCES CIRCLE SHAPE */
        border-radius: 50% !important;
        
        display: flex;
        align-items: center;
        justify-content: center;
        
        font-size: 1.5rem !important; /* Reduced from 1.8rem */
        font-weight: 400 !important;
        
        border: 1px solid rgba(255,255,255,0.05) !important;
        margin: 0 auto !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    
    /* Button Colors */
    /* Numbers (Dark Grey) */
    div.stButton > button { 
        background-color: #333333 !important; 
        color: white !important; 
    }
    
    /* Operators (Orange) */
    div.stButton > button[kind="primary"] { 
        background-color: #ff9f0a !important; 
        color: white !important; 
    }
    
    /* Active State (Tap effect) */
    div.stButton > button:active {
        filter: brightness(1.3);
        transform: scale(0.95);
    }
    
    /* Hide the default streamlit top padding to make it look like an app */
    header { visibility: hidden; }
    footer { visibility: hidden; }

</style>
""", unsafe_allow_html=True)

st.subheader(" Calculator")

# Logic
if "calc_expression" not in st.session_state:
    st.session_state.calc_expression = ""
if "memory" not in st.session_state:
    st.session_state.memory = 0.0

def calc_press(val):
    expr = st.session_state.calc_expression
    
    # Clear & Memory
    if val == "AC":
        st.session_state.calc_expression = ""
    elif val == "⌫":
        st.session_state.calc_expression = expr[:-1]
    elif val == "mc":
        st.session_state.memory = 0.0
    elif val == "m+":
        try: st.session_state.memory += float(eval(expr))
        except: pass
    elif val == "m-":
        try: st.session_state.memory -= float(eval(expr))
        except: pass
    elif val == "mr":
        st.session_state.calc_expression += str(st.session_state.memory)
        
    # Execution
    elif val == "=":
        try:
            # Replace visual symbols with python syntax
            valid_expr = expr
            replacements = {
                '×': '*', '÷': '/', '^': '**', 'π': 'math.pi', 'e': 'math.e',
                'sin': 'math.sin', 'cos': 'math.cos', 'tan': 'math.tan',
                'sinh': 'math.sinh', 'cosh': 'math.cosh', 'tanh': 'math.tanh',
                'ln': 'math.log', 'log₁₀': 'math.log10', '√': 'math.sqrt',
                '!': 'math.factorial', 'Rand': 'random.random()',
                '²': '**2', '³': '**3'
            }
            # Handle special cases like percentages or just replace strings
            # Simple replace approach for MVP scientific calc
            for k, v in replacements.items():
                valid_expr = valid_expr.replace(k, v)
                
            # Safe eval context
            import random
            context = {"math": math, "abs": abs, "random": random}
            res = eval(valid_expr, {"__builtins__": None}, context)
            
            if isinstance(res, float) and res.is_integer():
                res = int(res)
            st.session_state.calc_expression = str(res)
        except:
            st.session_state.calc_expression = "Error"
            
    # Standard Input
    else:
        st.session_state.calc_expression += str(val)

# --- Wide Landscape Layout CSS ---
st.markdown("""
<style>
    /* 1. CONTAINER: Wide Landscape Logic */
    .main .block-container {
        max-width: 1000px !important; /* Allow wide calculator */
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }
    
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        max-width: 100% !important;
        width: 100% !important;
    }

    /* 2. DISPLAY SCREEN */
    .calc-display {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 3.5rem;
        background-color: transparent; 
        color: #fff;
        text-align: right;
        border: none;
        margin-bottom: 10px;
        padding-right: 15px;
    }

    /* 3. BUTTONS (10 Columns) */
    div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1.2 / 1 !important; /* Slightly oval for landscape density */
        border-radius: 40% !important;
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        border: none !important;
        margin: 2px !important;
        padding: 0 !important;
        background-color: #333; /* Dark Grey (Scientific) Default */
        color: white !important;
    }

    /* Operators (Orange) via Primary Type */
    div.stButton > button[kind="primary"] { 
        background-color: #ff9f0a !important; 
    }
    
    /* Active State */
    div.stButton > button:active {
        filter: brightness(1.3);
        transform: scale(0.95);
    }
    
    header, footer { visibility: hidden; }

</style>
""", unsafe_allow_html=True)

st.subheader(" Scientific Calculator")

# Display
st.markdown(f"""<div class='calc-display'>{st.session_state.calc_expression if st.session_state.calc_expression else "0"}</div>""", unsafe_allow_html=True)

# 10x5 Scientific Grid
# [Label, Value, Kind]
# Kind: 'default' (dark grey), 'light' (lighter grey - handled by CSS hack or just ignored for MVP), 'primary' (orange)
buttons = [
    # Row 1
    ("(", "(", ""), (")", ")", ""), ("mc", "mc", ""), ("m+", "m+", ""), ("m-", "m-", ""), 
    ("mr", "mr", ""), ("AC", "AC", "light"), ("+/-", "-", "light"), ("%", "/100", "light"), ("÷", "÷", "primary"),
    # Row 2
    ("2ⁿᵈ", "", ""), ("x²", "²", ""), ("x³", "³", ""), ("xʸ", "^", ""), ("eˣ", "e^", ""), 
    ("10ˣ", "10^", ""), ("7", "7", "light"), ("8", "8", "light"), ("9", "9", "light"), ("×", "×", "primary"),
    # Row 3
    ("¹/x", "**-1", ""), ("²√x", "√(", ""), ("³√x", "**(1/3)", ""), ("ʸ√x", "**(1/", ""), ("ln", "ln(", ""), 
    ("log₁₀", "log₁₀(", ""), ("4", "4", "light"), ("5", "5", "light"), ("6", "6", "light"), ("−", "-", "primary"),
    # Row 4
    ("x!", "!", ""), ("sin", "sin(", ""), ("cos", "cos(", ""), ("tan", "tan(", ""), ("e", "e", ""), 
    ("EE", "*10^", ""), ("1", "1", "light"), ("2", "2", "light"), ("3", "3", "light"), ("+", "+", "primary"),
    # Row 5
    ("Rad", "", ""), ("sinh", "sinh(", ""), ("cosh", "cosh(", ""), ("tanh", "tanh(", ""), ("π", "π", ""), 
    ("Rand", "Rand", ""), ("0", "0", "light"), (".", ".", "light"), ("+/-", "+/-", "light"), ("=", "=", "primary"),
]

# Render 10-column Grid
idx = 0
for row in range(5):
    cols = st.columns(10, gap="small")
    for c in cols:
        if idx < len(buttons):
            label, val, kind = buttons[idx]
            # Use primary type for orange buttons, default for others
            # (Note: Streamlit doesn't support a 3rd color type natively without component tricks, 
            # so we stick to Dark/Orange to ensure stability)
            key_type = "primary" if kind == "primary" else "secondary"
            c.button(label, on_click=calc_press, args=(val,), type=key_type, use_container_width=True)
            idx += 1

st.markdown("""
---
### 💡 How to use on iPad:
1. Open this link in **Safari**.
2. Tap the **Share icon** (square with arrow).
3. Select **"Add to Home Screen"**.
4. Now it works like a real app!
---
✨ **Developed By Tamer Elwakeel** | *Python Diploma 2025*
""")
