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
    
    /* Default calculator buttons (main area) */
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
    
    /* SIDEBAR BUTTONS - Force rectangular shape for ALL buttons */
    section[data-testid="stSidebar"] button,
    div[data-testid="stSidebar"] button,
    [data-testid="stSidebar"] .stButton > button {
        aspect-ratio: auto !important;
        border-radius: 8px !important;
        width: 100% !important;
        height: auto !important;
        min-height: 48px !important;
        padding: 12px 20px !important;
    }
    
    /* Navy 3D styling - MAXIMUM SPECIFICITY */
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"][aria-label*="Add"],
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"][aria-label*="Clear"],
    section[data-testid="stSidebar"] div.stButton > button[kind="secondary"],
    div[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
        background: linear-gradient(145deg, #1e3a8a, #1e40af) !important;
        background-color: #1e40af !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 
            0 6px 12px rgba(30, 58, 138, 0.4),
            inset 0 -2px 4px rgba(0, 0, 0, 0.3),
            inset 0 2px 4px rgba(255, 255, 255, 0.2) !important;
    }
    
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"][aria-label*="Add"]:hover,
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"][aria-label*="Clear"]:hover,
    section[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover,
    div[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
        background: linear-gradient(145deg, #2563eb, #3b82f6) !important;
        background-color: #3b82f6 !important;
        transform: translateY(-2px);
        box-shadow: 
            0 10px 20px rgba(37, 99, 235, 0.5),
            inset 0 -2px 4px rgba(0, 0, 0, 0.3),
            inset 0 2px 4px rgba(255, 255, 255, 0.3) !important;
    }
    
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"][aria-label*="Add"]:active,
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"][aria-label*="Clear"]:active,
    section[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:active,
    div[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:active {
        transform: translateY(1px);
        box-shadow: 
            0 3px 6px rgba(30, 58, 138, 0.4),
            inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
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
    new_func = st.text_input("f(x) =", placeholder="e.g. sin(x) + 2", key="func_input")
    
    add_clicked = st.button("➕ Add to Plot", key="add_plot_btn", use_container_width=True)
    if add_clicked:
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
    
    clear_clicked = st.button("🗑️ Clear All Functions", key="clear_all_btn", use_container_width=True)
    if clear_clicked:
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
    
    # --- Draw Fixed X and Y Axes ---
    ax.axhline(y=0, color='white', linewidth=1.5, alpha=0.8, zorder=1)  # X-axis (horizontal line at y=0)
    ax.axvline(x=0, color='white', linewidth=1.5, alpha=0.8, zorder=1)  # Y-axis (vertical line at x=0)
    
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
    
    /* Mode toggle buttons styling */
    button[key="basic_calc_btn"],
    button[key="scientific_calc_btn"] {
        height: 40px !important;
        min-height: 40px !important;
        font-size: 0.9rem !important;
        padding: 8px 16px !important;
    }

    /* ---------------------------------------------------------------------
       4. MOBILE OPTIMIZATION (iPhone 12 Pro Max & Smaller)
       --------------------------------------------------------------------- */
    @media only screen and (max-width: 600px) {
        div.stButton > button {
            aspect-ratio: auto !important;
            height: 50px !important;
            min-height: 50px !important;
            border-radius: 12px !important; /* Rounded rect instead of circle */
            font-size: 1rem !important;
            margin: 1px !important;
        }
        
        /* Adjust toggle buttons clearly for mobile */
        button[key="basic_calc_btn"],
        button[key="scientific_calc_btn"] {
            font-size: 0.8rem !important;
            padding: 4px 8px !important;
        }
        
        .calc-display {
            font-size: 3rem !important;
            margin-bottom: 5px !important;
        }
    }

</style>
""", unsafe_allow_html=True)

# Force narrow calculator by using 3-column layout with narrow center
spacer_left, calc_column, spacer_right = st.columns([2, 3, 2])

with calc_column:
    # Calculator mode toggle buttons - now within narrow column
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍏 Basic", key="basic_calc_btn", use_container_width=True):
            st.session_state.calculator_mode = "basic"
            st.rerun()
    with col2:
        if st.button("🍏 Scientific", key="scientific_calc_btn", use_container_width=True):
            st.session_state.calculator_mode = "scientific"
            st.rerun()

    # Display current mode
    mode_name = "Basic Calculator" if st.session_state.get("calculator_mode", "scientific") == "basic" else "Scientific Calculator"
    st.markdown(f"<h4 style='text-align: center; color: #90EE90; margin:10px 0;'>{mode_name}</h4>", unsafe_allow_html=True)

# Logic
if "calc_expression" not in st.session_state:
    st.session_state.calc_expression = ""
if "memory" not in st.session_state:
    st.session_state.memory = 0.0
if "second_mode" not in st.session_state:
    st.session_state.second_mode = False  # Toggle for inverse trig functions
if "angle_mode" not in st.session_state:
    st.session_state.angle_mode = "Rad"  # "Rad" or "Deg"
if "calculator_mode" not in st.session_state:
    st.session_state.calculator_mode = "scientific"  # "basic" or "scientific"

def toggle_second_mode():
    st.session_state.second_mode = not st.session_state.second_mode

def toggle_angle_mode():
    st.session_state.angle_mode = "Deg" if st.session_state.angle_mode == "Rad" else "Rad"

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
            import re
            import random
            
            # Start with the expression
            valid_expr = expr
            
            # Basic symbol replacements
            valid_expr = valid_expr.replace('×', '*').replace('÷', '/')
            valid_expr = valid_expr.replace('^', '**')
            valid_expr = valid_expr.replace('²', '**2').replace('³', '**3')
            valid_expr = valid_expr.replace('π', 'math.pi').replace('e', 'math.e')
            
            # Handle trig functions based on angle mode
            if st.session_state.angle_mode == "Deg":
                # For normal trig (input in degrees)
                for trig in ['sin', 'cos', 'tan']:
                    # Match trig(content) where content doesn't contain parens (simple cases)
                    pattern = rf'\b{trig}\(([^()]+)\)'
                    replacement = rf'math.{trig}(math.radians(\1))'
                    valid_expr = re.sub(pattern, replacement, valid_expr)
                
                # For inverse trig (output in degrees)
                for trig in ['asin', 'acos', 'atan']:
                    pattern = rf'\b{trig}\(([^()]+)\)'
                    replacement = rf'math.degrees(math.{trig}(\1))'
                    valid_expr = re.sub(pattern, replacement, valid_expr)
            else:
                # Radians mode - just add math. prefix
                for trig in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
                    pattern = rf'\b{trig}\('
                    replacement = f'math.{trig}('
                    valid_expr = re.sub(pattern, replacement, valid_expr)
            
            # Handle other functions
            other_replacements = {
                'sinh': 'math.sinh', 'cosh': 'math.cosh', 'tanh': 'math.tanh',
                'ln': 'math.log', 'log₁₀': 'math.log10', '√': 'math.sqrt',
                '!': 'math.factorial', 'Rand': 'random.random()'
            }
            for k, v in other_replacements.items():
                valid_expr = valid_expr.replace(k, v)
            
            # Evaluate
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
        color: black !important; /* Black text for operators */
    }
    
    /* Active State */
    div.stButton > button:active {
        filter: brightness(1.3);
        transform: scale(0.95);
    }
    
    /* BASIC CALCULATOR - Constrain width */
    .basic-calculator-container {
        max-width: 350px;
        margin: 0 auto;
    }
    
    header, footer { visibility: hidden; }

</style>
""", unsafe_allow_html=True)

# Render Calculator in Center Column
with calc_column:
    # Display
    st.markdown(f"""<div class='calc-display'>{st.session_state.calc_expression if st.session_state.calc_expression else "0"}</div>""", unsafe_allow_html=True)

    # Conditional Calculator Layout Based on Mode
    if st.session_state.calculator_mode == "basic":
        # Remove container div wrapping since we're using column layout
        
        # BASIC CALCULATOR (4x6 grid like iOS calculator)
        basic_buttons = [
            # Row 1
            ("AC", "AC", "light"), ("+/-", "+/-", "light"), ("%", "%", "light"), ("÷", "÷", "primary"),
            # Row 2
            ("7", "7", "default"), ("8", "8", "default"), ("9", "9", "default"), ("×", "×", "primary"),
            # Row 3
            ("4", "4", "default"), ("5", "5", "default"), ("6", "6", "default"), ("−", "-", "primary"),
            # Row 4
            ("1", "1", "default"), ("2", "2", "default"), ("3", "3", "default"), ("+", "+", "primary"),
            # Row 5
            ("0", "0", "default"), (".", ".", "default"), ("⌫", "⌫", "light"), ("=", "=", "primary"),
        ]
        
        # Render 4-column basic grid
        idx = 0
        for row in range(5):
            cols = st.columns(4, gap="small")
            for c in cols:
                if idx < len(basic_buttons):
                    label, val, kind = basic_buttons[idx]
                    key_type = "primary" if kind == "primary" else "secondary"
                    c.button(label, on_click=calc_press, args=(val,), type=key_type, use_container_width=True, key=f"basic_btn_{idx}")
                    idx += 1

    else:  # scientific mode
        # SCIENTIFIC CALCULATOR (10x5 grid)
        # Dynamic button labels based on mode
        sin_label = "asin" if st.session_state.second_mode else "sin"
        cos_label = "acos" if st.session_state.second_mode else "cos"
        tan_label = "atan" if st.session_state.second_mode else "tan"
        sin_val = "asin(" if st.session_state.second_mode else "sin("
        cos_val = "acos(" if st.session_state.second_mode else "cos("
        tan_val = "atan(" if st.session_state.second_mode else "tan("

        buttons = [
            # Row 1
            ("(", "(", ""), (")", ")", ""), ("mc", "mc", ""), ("m+", "m+", ""), ("m-", "m-", ""), 
            ("mr", "mr", ""), ("AC", "AC", "light"), ("+/-", "-", "light"), ("%", "/100", "light"), ("÷", "÷", "primary"),
            # Row 2
            ("2ⁿᵈ", "2nd", ""), ("x²", "²", ""), ("x³", "³", ""), ("xʸ", "^", ""), ("eˣ", "e^", ""), 
            ("10ˣ", "10^", ""), ("7", "7", "light"), ("8", "8", "light"), ("9", "9", "light"), ("×", "×", "primary"),
            # Row 3
            ("¹/x", "**-1", ""), ("²√x", "√(", ""), ("³√x", "**(1/3)", ""), ("ʸ√x", "**(1/", ""), ("ln", "ln(", ""), 
            ("log₁₀", "log₁₀(", ""), ("4", "4", "light"), ("5", "5", "light"), ("6", "6", "light"), ("−", "-", "primary"),
            # Row 4 - Dynamic trig labels
            ("x!", "!", ""), (sin_label, sin_val, ""), (cos_label, cos_val, ""), (tan_label, tan_val, ""), ("e", "e", ""), 
            ("EE", "*10^", ""), ("1", "1", "light"), ("2", "2", "light"), ("3", "3", "light"), ("+", "+", "primary"),
            # Row 5 - Dynamic angle mode
            (st.session_state.angle_mode, "angle_toggle", ""), ("sinh", "sinh(", ""), ("cosh", "cosh(", ""), ("tanh", "tanh(", ""), ("π", "π", ""), 
            ("Rand", "Rand", ""), ("0", "0", "light"), (".", ".", "light"), ("+/-", "+/-", "light"), ("=", "=", "primary"),
        ]

        # Render 10-column Grid
        idx = 0
        for row in range(5):
            cols = st.columns(10, gap="small")
            for c in cols:
                if idx < len(buttons):
                    label, val, kind = buttons[idx]
                    # Skip empty buttons
                    if label:  
                        # Use primary type for orange buttons, default for others
                        key_type = "primary" if kind == "primary" else "secondary"
                        
                        # Special handling for mode toggle buttons
                        if val == "2nd":
                            c.button(label, on_click=toggle_second_mode, type=key_type, use_container_width=True, key=f"calc_btn_{idx}")
                        elif val == "angle_toggle":
                            c.button(label, on_click=toggle_angle_mode, type=key_type, use_container_width=True, key=f"calc_btn_{idx}")
                        else:
                            c.button(label, on_click=calc_press, args=(val,), type=key_type, use_container_width=True, key=f"calc_btn_{idx}")
                    idx += 1


st.markdown("""
---
### 💡 How to use on iPad:
1. Open this link in **Safari**.
2. Tap the **Share icon** (square with arrow).
3. Select **"Add to Home Screen"**.
4. Now it works like a real app!
---
✨ **Developed By Tamer Elwakeel** | *2025*
""")
