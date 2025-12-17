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
# Simple Calculator Tab
# -----------------------------------------------------------------------------
st.divider()
st.subheader("🔢 Quick Basic Calculator")
col1, col2 = st.columns([3, 1])
calc_input = col1.text_input("Enter expression:", value="15 * (2 + 3)")
if col2.button("Calculate"):
    try:
        # Use your custom calculator logic here if needed
        result = eval(calc_input)
        st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("""
---
### 💡 How to use on iPad:
1. Open this link in **Safari**.
2. Tap the **Share icon** (square with arrow).
3. Select **"Add to Home Screen"**.
4. Now it works like a real app!
""")
