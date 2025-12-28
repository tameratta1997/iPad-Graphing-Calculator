import tkinter as tk
from tkinter import ttk, messagebox
import calculator
import math
import os
import json
# Heavy libraries (numpy, matplotlib) will be lazily imported when needed
# to improve application startup time.

# Placeholders for lazy modules
np = None
plt = None
FigureCanvasTkAgg = None
Figure = None

# -----------------------------------------------------------------------------
# Color Scheme Configuration
# -----------------------------------------------------------------------------
COLOR_BG = "#1c1c1c"         # Main Window Background
COLOR_BTN_NUM = "#505050"    # Number keys (0-9) background (Dark Gray)
COLOR_BTN_OP = "#90EE90"     # Operations keys (+, -, *, /) background (Light Green)
COLOR_BTN_TOP = "#D4D4D2"    # Top row keys (AC, +/-, %) background (Light Gray)
COLOR_BTN_SCI = "#2d2d2d"    # Scientific function keys background (Darker Gray)
COLOR_TEXT_WHITE = "#ffffff" # White text color (for numbers and sci keys)
COLOR_TEXT_BLACK = "#000000" # Black text color (for op keys and top keys)

CONFIG_FILE = os.path.expanduser("~/.scientific_calculator_config.json")

class CalculatorGUI:
    """
    Main GUI class for the Calculator application with Graphing capabilities.
    Handles the window setup, layout management (Basic/Scientific/Programmer/Graphing),
    button creation, events, and calculation logic.
    """
    def __init__(self, root):
        """
        Initialize the Calculator application.
        
        Args:
            root (tk.Tk): The root window object.
        """
        self.root = root
        self.root.title("Graphing Calculator - Developed by Tamer Elwakeel")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False) # Disable resizing to keep fixed layout

        self.current_mode = self.load_config()  # Load last mode
        self.expression = []         # Stores the operation history (e.g., ['5', '+', '3'])
        self.current_val = "0"       # Current number being displayed or typed
        self.new_input = True        # Flag to clear display on new number input
        self.prog_base = 10          # Base for Programmer mode (10=DEC, 16=HEX, etc.)
        self.is_mac = self.root.tk.call('tk', 'windowingsystem') == 'aqua' # Detect macOS

        # Graphing mode variables
        self.graph_functions = []    # List of functions to plot
        self.graph_colors = ['#00ff00', '#ff00ff', '#00ffff', '#ffff00', '#ff8800']
        self.x_min, self.x_max = -10, 10
        self.y_min, self.y_max = -10, 10

        # --- Main Layout Container ---
        self.main_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.main_frame.pack(fill="both", expand=True)

        # --- Header Section (Mode Switcher) ---
        self.setup_header()

        # --- Display Area (Screen) ---
        self.setup_display()

        # --- Keyboard Area (Buttons) ---
        self.keyboard_frame = tk.Frame(self.main_frame, bg=COLOR_BG)
        self.keyboard_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Build initial layout (Basic Mode)
        self.build_layout()

    def setup_header(self):
        """
        Sets up the top header bar containing the mode switcher button.
        """
        self.header_frame = tk.Frame(self.main_frame, bg=COLOR_BG, height=30)
        self.header_frame.pack(fill="x", padx=5, pady=2)
        
        # Mode Button: Uses a unicode grid symbol to look like a keypad/menu icon
        self.mode_btn_label = tk.Label(self.header_frame, text="\u25A6", bg=COLOR_BG, fg=COLOR_TEXT_WHITE,
                                     font=("Arial", 24), cursor="hand2")
        
        # Position at the top right as requested
        self.mode_btn_label.pack(side="right", padx=10)

        # Create a popup menu for selecting modes
        self.mode_menu = tk.Menu(self.root, tearoff=0)
        
        # Helper variable for checking the active mode in the menu
        self.mode_var = tk.StringVar(value=self.current_mode)
        
        # Add mode options
        self.mode_menu.add_radiobutton(label="Basic", variable=self.mode_var, value="Basic", command=lambda: self.switch_mode("Basic"))
        self.mode_menu.add_radiobutton(label="Scientific", variable=self.mode_var, value="Scientific", command=lambda: self.switch_mode("Scientific"))
        self.mode_menu.add_radiobutton(label="Programmer", variable=self.mode_var, value="Programmer", command=lambda: self.switch_mode("Programmer"))
        self.mode_menu.add_radiobutton(label="Graphing", variable=self.mode_var, value="Graphing", command=lambda: self.switch_mode("Graphing"))

        # Bind click event to show the menu
        self.mode_btn_label.bind("<Button-1>", self.show_mode_menu)

    def show_mode_menu(self, event):
        """
        Displays the mode selection popup menu at the cursor position.
        """
        try:
            self.mode_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.mode_menu.grab_release()

    def setup_display(self):
        """
        Sets up the calculator display screen.
        """
        self.display_frame = tk.Frame(self.main_frame, bg=COLOR_BG)
        self.display_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Main number display label
        self.lbl_display = tk.Label(self.display_frame, text="0", bg=COLOR_BG, fg=COLOR_TEXT_WHITE, 
                                    font=("Helvetica", 48), anchor="e")
        self.lbl_display.pack(fill="x")
        
        # Additional frame for Programmer mode base indicators (HEX, DEC, etc.)
        self.prog_display_frame = tk.Frame(self.main_frame, bg=COLOR_BG)

    def create_btn(self, parent, text, cmd, type="num", width=1, height=1):
        """
        Creates a custom styled button using a Frame and a Label.
        Standard tk.Buttons cannot have their background color changed easily on macOS.
        
        Args:
            parent: Parent widget.
            text: Button label text.
            cmd: Function to execute on click.
            type: Category of button ('num', 'op', 'top', 'sci') for styling.
            width, height: (Deprecated) Dimensions.
        
        Returns:
            tk.Frame: The frame widget containing the button label.
        """
        # --- Determine Colors based on button type ---
        if type == "num":
            bg, fg = COLOR_BTN_NUM, COLOR_TEXT_WHITE
        elif type == "op":
            bg, fg = COLOR_BTN_OP, COLOR_TEXT_BLACK
            if text == "=": fg = COLOR_TEXT_BLACK
        elif type == "top":
            bg, fg = COLOR_BTN_TOP, COLOR_TEXT_BLACK
        elif type == "sci":
            bg, fg = COLOR_BTN_SCI, COLOR_TEXT_WHITE
        else:
            bg, fg = COLOR_BTN_NUM, COLOR_TEXT_WHITE

        # Frame acts as the border/container (creates the spacing look)
        frame = tk.Frame(parent, bg="#1c1c1c", padx=1, pady=1)

        # Label acts as the interactive button
        pady = 10
        if self.current_mode == "Scientific": pady = 5
        if self.current_mode == "Programmer": pady = 5
        
        lbl = tk.Label(frame, text=text, bg=bg, fg=fg, font=("Arial", 18), width=4, height=2)
        
        # Special styling for '0' key in Basic mode (needs to be wider)
        if text == "0" and self.current_mode == "Basic":
             lbl.config(width=9, anchor="w", padx=20)
        
        lbl.pack(fill="both", expand=True)
        
        # --- Helper for Press Effect (Lighten color on press) ---
        def adjust_color(hex_color, brightness_offset=40):
            if not hex_color.startswith("#"): return hex_color
            color = hex_color.strip("#")
            r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
            r = min(255, max(0, r + brightness_offset))
            g = min(255, max(0, g + brightness_offset))
            b = min(255, max(0, b + brightness_offset))
            return f"#{r:02x}{g:02x}{b:02x}"

        press_color = adjust_color(bg, 30)

        # --- Button Event Bindings ---
        def on_press(e):
            lbl.config(bg=press_color) # Visual feedback
            cmd() # Execute command
            
        def on_release(e):
            lbl.config(bg=bg) # Reset color on release
            
        lbl.bind("<Button-1>", on_press)
        lbl.bind("<ButtonRelease-1>", on_release)
        
        # Hover effect handling (currently resets color on leave to be safe)
        def on_enter(e): pass 
        def on_leave(e): lbl.config(bg=bg)
            
        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)

        return frame

    def load_config(self):
        """Loads last mode from config file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get("mode", "Basic")
        except: pass
        return "Basic"

    def save_config(self):
        """Saves current mode to config file"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"mode": self.current_mode}, f)
        except: pass

    def clean_keyboard(self):
        """
        Removes all widgets from the keyboard area to prepare for a layout switch.
        Also resets grid configuration to avoid layout artifacts.
        """
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()
        for widget in self.prog_display_frame.winfo_children():
            widget.destroy()
        self.prog_display_frame.pack_forget()
        
        # Reset grid weights
        for i in range(20):
            self.keyboard_frame.grid_columnconfigure(i, weight=0)
            self.keyboard_frame.grid_rowconfigure(i, weight=0)

    def switch_mode(self, mode):
        """
        Switches the calculator mode and rebuilds the interface.
        
        Args:
            mode (str): "Basic", "Scientific", "Programmer", or "Graphing".
        """
        self.current_mode = mode
        self.save_config() # Save the new mode
        self.mode_var.set(mode) # Update menu selection checkmark
        self.clean_keyboard()   # Clear old keys
        self.build_layout()     # Build new layout
        self.current_val = "0"  # Reset value
        self.update_display()   # Update screen

    def build_layout(self):
        """
        Determines which layout to build based on current_mode and sets window size.
        """
        if self.current_mode == "Basic":
            self.root.geometry("320x480")
            self.build_basic_keyboard()
        elif self.current_mode == "Scientific":
            self.root.geometry("680x400")
            self.build_scientific_keyboard()
        elif self.current_mode == "Programmer":
            self.root.geometry("500x580")
            self.build_programmer_keyboard()
        elif self.current_mode == "Graphing":
            self.root.geometry("900x700")
            self.build_graphing_mode()

    def build_basic_keyboard(self):
        """
        Constructs the standard calculator layout (0-9, basic ops).
        """
        keys = [
            ("AC", "top", self.clear), ("+/-", "top", self.negate), ("%", "top", self.percent), ("/", "op", lambda: self.op("/")),
            ("7", "num", lambda: self.num("7")), ("8", "num", lambda: self.num("8")), ("9", "num", lambda: self.num("9")), ("*", "op", lambda: self.op("*")),
            ("4", "num", lambda: self.num("4")), ("5", "num", lambda: self.num("5")), ("6", "num", lambda: self.num("6")), ("-", "op", lambda: self.op("-")),
            ("1", "num", lambda: self.num("1")), ("2", "num", lambda: self.num("2")), ("3", "num", lambda: self.num("3")), ("+", "op", lambda: self.op("+")),
            ("0", "num", lambda: self.num("0")), (".", "num", lambda: self.num(".")), ("=", "op", self.calculate)
        ]
        
        # Configure Grid (4 columns, 5 rows)
        for i in range(5): self.keyboard_frame.grid_rowconfigure(i, weight=1)
        for i in range(4): self.keyboard_frame.grid_columnconfigure(i, weight=1)

        row, col = 0, 0
        for text, type_, cmd in keys:
            colspan = 2 if text == "0" else 1
            btn = self.create_btn(self.keyboard_frame, text, cmd, type_)
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=1, pady=1)
            
            col += colspan
            if col >= 4:
                col = 0
                row += 1

    def build_scientific_keyboard(self):
        """
        Constructs the Scientific calculator layout, including trig functions, roots, logs, etc.
        """
        self.sci_btn_labels = {} # Store labels to update text (e.g., when 2nd is pressed)
        
        # Unicode Labels for Root Functions
        L_SQRT = "\u00B2\u221Ax" # ²√x
        L_CBRT = "\u00B3\u221Ax" # ³√x
        L_YROOT = "\u02B8\u221Ax" # ʸ√x

        # Layout Design: 10 columns total (6 sci functions + 4 basic keys)
        sci_keys = [
            ["(", ")", "mc", "m+", "m-", "mr"],
            ["2nd", "x^2", "x^3", "x^y", "y^x", "2^x"],
            ["1/x", L_SQRT, L_CBRT, L_YROOT, "ln", "log10"],
            ["x!", "sin", "cos", "tan", "e", "EE"],
            ["Rad", "sinh", "cosh", "tanh", "pi", "Rand"]
        ]
        basic_keys_grid = [
            ["AC", "+/-", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        for i in range(5): self.keyboard_frame.grid_rowconfigure(i, weight=1)
        for i in range(10): self.keyboard_frame.grid_columnconfigure(i, weight=1)
            
        # Place Scientific Keys (Left side)
        for r, row_keys in enumerate(sci_keys):
            for c, k in enumerate(row_keys):
                cmd = lambda x=k: self.sci_op(x)
                
                # Special command bindings
                if k in ["(", ")"]: 
                    cmd = lambda x=k: self.num(x) 
                elif k == "x^y":
                     cmd = lambda: self.op("**")
                elif k == "y^x":
                     cmd = lambda: self.op("ypow")
                elif k == L_YROOT:
                     cmd = lambda: self.op("yroot")
                elif k == "2nd":
                     cmd = self.toggle_2nd
                
                btn_frame = self.create_btn(self.keyboard_frame, k, cmd, "sci")
                
                # Store label for dynamic text updating (for 2nd button functionality)
                try:
                    lbl = btn_frame.winfo_children()[0]
                    self.sci_btn_labels[k] = lbl
                    # Maintain highlight state if 2nd is active
                    if k == "2nd" and getattr(self, 'second_active', False):
                         lbl.config(bg=COLOR_BTN_OP, fg=COLOR_TEXT_BLACK) 
                except: pass

                btn_frame.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

        # Place Basic Keys (Right side columns 6-9)
        for r, row_keys in enumerate(basic_keys_grid):
            current_col = 6
            for k in row_keys:
                type_ = "num"
                if k in ["AC", "+/-", "%"]: type_ = "top"
                elif k in ["/", "*", "-", "+", "="]: type_ = "op"
                
                cmd = lambda x=k: self.num(x)
                if k == "AC": cmd = self.clear
                elif k == "=": cmd = self.calculate
                elif k == "+/-": cmd = self.negate
                elif k == "%": cmd = self.percent
                elif type_ == "op": cmd = lambda x=k: self.op(x)
                
                colspan = 2 if k == "0" else 1
                btn = self.create_btn(self.keyboard_frame, k, cmd, type_)
                btn.grid(row=r, column=current_col, columnspan=colspan, sticky="nsew", padx=1, pady=1)
                
                current_col += colspan

    def build_programmer_keyboard(self):
        """
        Constructs the Programmer calculator layout (HEX, DEC, BIN, logical ops).
        """
        # Show the Base selection toolbar (HEX/DEC/OCT/BIN)
        self.prog_display_frame.pack(fill="x", padx=10, before=self.keyboard_frame)
        
        # Create Base switching buttons
        for t, b in [("HEX", 16), ("DEC", 10), ("OCT", 8), ("BIN", 2)]:
            bg_color = COLOR_BTN_SCI if self.prog_base != b else COLOR_BTN_OP
            lbl = tk.Label(self.prog_display_frame, text=t, bg=bg_color, fg=COLOR_TEXT_WHITE, font=("Arial", 12))
            lbl.pack(side="left", expand=True, fill="x", padx=1, pady=2)
            lbl.bind("<Button-1>", lambda e, v=b: self.set_base(v))

        prog_keys = [
            ["AC", "+/-", "%", "/", "AND", "OR"],
            ["7", "8", "9", "*", "XOR", "NOT"],
            ["4", "5", "6", "-", "<<", ">>"],
            ["1", "2", "3", "+", "A", "B"],
            ["0", "=", "C", "D", "E", "F"]
        ]
        
        for i in range(5): self.keyboard_frame.grid_rowconfigure(i, weight=1)
        for i in range(6): self.keyboard_frame.grid_columnconfigure(i, weight=1)

        for r, row in enumerate(prog_keys):
            for c, val in enumerate(row):
                 type_ = "num"
                 if val in ["/", "*", "-", "+", "="]: type_="op"
                 elif val in ["AC", "+/-", "%"]: type_="top"
                 elif val in ["AND", "OR", "XOR", "NOT", "<<", ">>", "A","B","C","D","E","F"]: type_="sci"
                 
                 cmd = lambda x=val: self.num(x)
                 if val == "AC": cmd = self.clear
                 elif val == "=": cmd = self.calculate
                 elif type_ == "op": cmd = lambda x=val: self.op(x)
                 elif val in ["AND", "OR", "XOR", "NOT", "<<", ">>"]: cmd = lambda x=val: self.op(x)
                 
                 btn = self.create_btn(self.keyboard_frame, val, cmd, type_)
                 btn.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

    def build_graphing_mode(self):
        """
        Constructs the Graphing calculator mode with function input and plot display.
        """
        # Lazy Import Heavy Libraries
        global np, plt, FigureCanvasTkAgg, Figure
        if np is None:
            import numpy as np
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure

        # Create main container
        graph_container = tk.Frame(self.keyboard_frame, bg=COLOR_BG)
        graph_container.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Control Panel (Top) ---
        control_frame = tk.Frame(graph_container, bg=COLOR_BG)
        control_frame.pack(fill="x", pady=(0, 10))

        # Function input
        tk.Label(control_frame, text="f(x) =", bg=COLOR_BG, fg=COLOR_TEXT_WHITE, 
                font=("Arial", 14)).pack(side="left", padx=5)
        
        self.func_entry = tk.Entry(control_frame, bg=COLOR_BTN_NUM, fg=COLOR_TEXT_WHITE,
                                   font=("Courier", 14), insertbackground=COLOR_TEXT_WHITE)
        self.func_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.func_entry.insert(0, "sin(x)")
        
        # Add function button
        add_btn = tk.Button(control_frame, text="Plot", bg=COLOR_BTN_OP, fg=COLOR_TEXT_BLACK,
                           font=("Arial", 12, "bold"), command=self.add_function, cursor="hand2")
        add_btn.pack(side="left", padx=5)

        # Clear all button
        clear_btn = tk.Button(control_frame, text="Clear All", bg=COLOR_BTN_TOP, fg=COLOR_TEXT_BLACK,
                             font=("Arial", 12), command=self.clear_all_functions, cursor="hand2")
        clear_btn.pack(side="left", padx=5)

        # --- Range Controls ---
        range_frame = tk.Frame(graph_container, bg=COLOR_BG)
        range_frame.pack(fill="x", pady=(0, 10))

        tk.Label(range_frame, text="X Range:", bg=COLOR_BG, fg=COLOR_TEXT_WHITE,
                font=("Arial", 12)).pack(side="left", padx=5)
        
        self.x_min_entry = tk.Entry(range_frame, bg=COLOR_BTN_NUM, fg=COLOR_TEXT_WHITE,
                                    font=("Arial", 12), width=6, insertbackground=COLOR_TEXT_WHITE)
        self.x_min_entry.pack(side="left", padx=2)
        self.x_min_entry.insert(0, "-10")
        
        tk.Label(range_frame, text="to", bg=COLOR_BG, fg=COLOR_TEXT_WHITE,
                font=("Arial", 12)).pack(side="left", padx=2)
        
        self.x_max_entry = tk.Entry(range_frame, bg=COLOR_BTN_NUM, fg=COLOR_TEXT_WHITE,
                                    font=("Arial", 12), width=6, insertbackground=COLOR_TEXT_WHITE)
        self.x_max_entry.pack(side="left", padx=2)
        self.x_max_entry.insert(0, "10")

        tk.Label(range_frame, text="Y Range:", bg=COLOR_BG, fg=COLOR_TEXT_WHITE,
                font=("Arial", 12)).pack(side="left", padx=(20, 5))
        
        self.y_min_entry = tk.Entry(range_frame, bg=COLOR_BTN_NUM, fg=COLOR_TEXT_WHITE,
                                    font=("Arial", 12), width=6, insertbackground=COLOR_TEXT_WHITE)
        self.y_min_entry.pack(side="left", padx=2)
        self.y_min_entry.insert(0, "-10")
        
        tk.Label(range_frame, text="to", bg=COLOR_BG, fg=COLOR_TEXT_WHITE,
                font=("Arial", 12)).pack(side="left", padx=2)
        
        self.y_max_entry = tk.Entry(range_frame, bg=COLOR_BTN_NUM, fg=COLOR_TEXT_WHITE,
                                    font=("Arial", 12), width=6, insertbackground=COLOR_TEXT_WHITE)
        self.y_max_entry.pack(side="left", padx=2)
        self.y_max_entry.insert(0, "10")

        update_btn = tk.Button(range_frame, text="Update", bg=COLOR_BTN_OP, fg=COLOR_TEXT_BLACK,
                              font=("Arial", 10), command=self.update_graph, cursor="hand2")
        update_btn.pack(side="left", padx=10)

        # --- Function List ---
        list_frame = tk.Frame(graph_container, bg=COLOR_BG)
        list_frame.pack(fill="x", pady=(0, 10))

        tk.Label(list_frame, text="Functions:", bg=COLOR_BG, fg=COLOR_TEXT_WHITE,
                font=("Arial", 12, "bold")).pack(side="left", padx=5)
        
        self.func_listbox = tk.Listbox(list_frame, bg=COLOR_BTN_NUM, fg=COLOR_TEXT_WHITE,
                                       font=("Courier", 10), height=3, selectmode=tk.SINGLE)
        self.func_listbox.pack(side="left", fill="x", expand=True, padx=5)

        remove_btn = tk.Button(list_frame, text="Remove", bg=COLOR_BTN_TOP, fg=COLOR_TEXT_BLACK,
                              font=("Arial", 10), command=self.remove_function, cursor="hand2")
        remove_btn.pack(side="left", padx=5)

        # --- Graph Canvas ---
        self.fig = Figure(figsize=(8, 5), facecolor='#2d2d2d')
        self.ax = self.fig.add_subplot(111, facecolor='#1c1c1c')
        
        # Style the plot
        self.ax.spines['bottom'].set_color(COLOR_TEXT_WHITE)
        self.ax.spines['top'].set_color(COLOR_TEXT_WHITE)
        self.ax.spines['left'].set_color(COLOR_TEXT_WHITE)
        self.ax.spines['right'].set_color(COLOR_TEXT_WHITE)
        self.ax.tick_params(colors=COLOR_TEXT_WHITE)
        self.ax.xaxis.label.set_color(COLOR_TEXT_WHITE)
        self.ax.yaxis.label.set_color(COLOR_TEXT_WHITE)
        self.ax.grid(True, alpha=0.3, color=COLOR_TEXT_WHITE)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Quick function buttons
        quick_frame = tk.Frame(graph_container, bg=COLOR_BG)
        quick_frame.pack(fill="x", pady=(10, 0))

        tk.Label(quick_frame, text="Quick Functions:", bg=COLOR_BG, fg=COLOR_TEXT_WHITE,
                font=("Arial", 10)).pack(side="left", padx=5)

        quick_funcs = [
            ("sin(x)", "sin(x)"),
            ("cos(x)", "cos(x)"),
            ("x²", "x**2"),
            ("x³", "x**3"),
            ("√x", "sqrt(x)"),
            ("1/x", "1/x"),
            ("e^x", "exp(x)"),
            ("ln(x)", "log(x)"),
        ]

        for label, func in quick_funcs:
            btn = tk.Button(quick_frame, text=label, bg=COLOR_BTN_SCI, fg=COLOR_TEXT_WHITE,
                           font=("Arial", 9), command=lambda f=func: self.insert_quick_function(f),
                           cursor="hand2")
            btn.pack(side="left", padx=2)

        # Bind Enter key to plot function
        self.func_entry.bind("<Return>", lambda e: self.add_function())

    def insert_quick_function(self, func):
        """Insert a quick function into the entry field"""
        self.func_entry.delete(0, tk.END)
        self.func_entry.insert(0, func)
        self.add_function()

    def add_function(self):
        """Add a function to the graph"""
        func_str = self.func_entry.get().strip()
        if not func_str:
            return
        
        # --- Robust Validation ---
        try:
            # Prepare expression (Standardizing notation)
            expr = func_str.replace('^', '**')
            replacements = {
                'sqrt': 'np.sqrt', 'sin': 'np.sin', 'cos': 'np.cos', 
                'tan': 'np.tan', 'exp': 'np.exp', 'log': 'np.log', 
                'abs': 'np.abs', 'pi': 'np.pi', 'e': 'np.e'
            }
            for old, new in replacements.items():
                # Only replace if not preceded by a word character (preventing double replacement)
                import re
                expr = re.sub(r'(?<![a-zA-Z0-9_.])' + old, new, expr)

            # Test validation with a small array to mimic real plotting
            test_x = np.array([1.0, 2.0])
            safe_dict = {"x": test_x, "np": np, "math": math}
            res = eval(expr, {"__builtins__": None}, safe_dict)
            
            # Verify result can be treated as an array
            _ = np.atleast_1d(res)

            if func_str not in self.graph_functions:
                self.graph_functions.append(func_str)
                self.func_listbox.insert(tk.END, func_str)
                # Dynamic auto-fit on add
                self.update_graph(auto_fit=True)
                self.func_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Invalid Function", f"Error in function: {str(e)}\n\nUse 'x' as variable.\nExamples: sin(x), x**2, sqrt(x)")

    def remove_function(self):
        """Remove selected function from the graph"""
        selection = self.func_listbox.curselection()
        if selection:
            idx = selection[0]
            self.func_listbox.delete(idx)
            del self.graph_functions[idx]
            self.update_graph(auto_fit=True)

    def clear_all_functions(self):
        """Clear all functions from the graph"""
        self.graph_functions = []
        self.func_listbox.delete(0, tk.END)
        # Reset to default range
        self.x_min_entry.delete(0, tk.END); self.x_min_entry.insert(0, "-10")
        self.x_max_entry.delete(0, tk.END); self.x_max_entry.insert(0, "10")
        self.y_min_entry.delete(0, tk.END); self.y_min_entry.insert(0, "-10")
        self.y_max_entry.delete(0, tk.END); self.y_max_entry.insert(0, "10")
        self.update_graph()

    def _evaluate_function(self, func_str, x_array):
        """Helper to evaluate a function string safely and return a broadcasted array"""
        expr = func_str.replace('^', '**')
        replacements = {
            'sqrt': 'np.sqrt', 'sin': 'np.sin', 'cos': 'np.cos', 
            'tan': 'np.tan', 'exp': 'np.exp', 'log': 'np.log', 
            'abs': 'np.abs', 'pi': 'np.pi', 'e': 'np.e'
        }
        import re
        for old, new in replacements.items():
            expr = re.sub(r'(?<![a-zA-Z0-9_.])' + old, new, expr)
            
        res = eval(expr, {"__builtins__": None}, {"np": np, "x": x_array})
        
        # Force scalar results (like 2) into arrays matching x_array
        if np.isscalar(res) or (isinstance(res, np.ndarray) and res.ndim == 0):
            return np.full_like(x_array, res, dtype=float)
        return np.asarray(res, dtype=float)

    def update_graph(self, auto_fit=False):
        """Update the graph with current functions and ranges"""
        
        # --- Handle Dynamic Auto-Fitting ---
        if auto_fit and self.graph_functions:
            try:
                # 1. Broad scan to find intersections and interesting points
                scan_x = np.linspace(-50, 50, 1000)
                scan_points_x = []
                scan_points_y = []
                all_y_scans = []
                
                for f_str in self.graph_functions:
                    try:
                        y_scan = self._evaluate_function(f_str, scan_x)
                        all_y_scans.append(y_scan)
                        
                        # A. Add roots roughly
                        roots_idx = np.where(np.diff(np.sign(y_scan)))[0]
                        for r_idx in roots_idx: 
                            scan_points_x.append(scan_x[r_idx])
                            scan_points_y.append(y_scan[r_idx])
                            
                        # B. Add vertices (local extrema)
                        # Find where derivative changes sign
                        dy = np.diff(y_scan)
                        extrema_idx = np.where(np.diff(np.sign(dy)))[0] + 1
                        for e_idx in extrema_idx:
                            scan_points_x.append(scan_x[e_idx])
                            scan_points_y.append(y_scan[e_idx])
                            
                    except: all_y_scans.append(None)

                # 2. Find intersections globally
                solutions_x = []
                solutions_y = []
                import itertools
                for i, j in itertools.combinations(range(len(all_y_scans)), 2):
                    if all_y_scans[i] is not None and all_y_scans[j] is not None:
                        diff = all_y_scans[i] - all_y_scans[j]
                        crossings = np.where(np.diff(np.sign(diff)))[0]
                        for c_idx in crossings:
                            solutions_x.append(scan_x[c_idx])
                            solutions_y.append(all_y_scans[i][c_idx])

                # 3. Decision for Range
                # Collect all "important" points (solutions, roots, vertices)
                all_points_x = solutions_x + scan_points_x
                all_points_y = solutions_y + scan_points_y
                
                if all_points_x:
                    # Focus on all interesting features
                    self.x_min = min(all_points_x)
                    self.x_max = max(all_points_x)
                    self.y_min = min(all_points_y)
                    self.y_max = max(all_points_y)
                    
                    # Apply some intelligent padding
                    padding_x = (self.x_max - self.x_min) * 0.4 if (self.x_max - self.x_min) > 0 else 5
                    padding_y = (self.y_max - self.y_min) * 0.4 if (self.y_max - self.y_min) > 0 else 5
                    
                    self.x_min -= max(2, padding_x)
                    self.x_max += max(2, padding_x)
                    self.y_min -= max(2, padding_y)
                    self.y_max += max(2, padding_y)
                else:
                    self.x_min, self.x_max = -10, 10
                    self.y_min, self.y_max = -10, 10

                # Sanitize ranges (limit to reasonable view)
                self.x_min, self.x_max = max(-100, self.x_min), min(100, self.x_max)
                self.y_min, self.y_max = max(-100, self.y_min), min(100, self.y_max)
                if abs(self.y_max - self.y_min) < 0.1: self.y_min -= 1; self.y_max += 1
                
                # Update UI entries
                self.x_min_entry.delete(0, tk.END); self.x_min_entry.insert(0, f"{self.x_min:.1f}")
                self.x_max_entry.delete(0, tk.END); self.x_max_entry.insert(0, f"{self.x_max:.1f}")
                self.y_min_entry.delete(0, tk.END); self.y_min_entry.insert(0, f"{self.y_min:.1f}")
                self.y_max_entry.delete(0, tk.END); self.y_max_entry.insert(0, f"{self.y_max:.1f}")
            except Exception as e:
                print(f"Auto-fit failed: {e}")

        # --- Standard Range Update (from UI) ---
        try:
            self.x_min = float(self.x_min_entry.get())
            self.x_max = float(self.x_max_entry.get())
            self.y_min = float(self.y_min_entry.get())
            self.y_max = float(self.y_max_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Range", "Please enter valid numbers for ranges")
            return

        # Clear the plot
        self.ax.clear()
        self.ax.set_facecolor('#1c1c1c')
        self.ax.grid(True, alpha=0.3, color=COLOR_TEXT_WHITE)
        
        # Add fixed X and Y reference axes (as requested)
        self.ax.axhline(y=0, color=COLOR_TEXT_WHITE, linewidth=2.5, alpha=0.8)
        self.ax.axvline(x=0, color=COLOR_TEXT_WHITE, linewidth=2.5, alpha=0.8)
        
        # Generate x values
        x = np.linspace(self.x_min, self.x_max, 1000)
        
        # Store y values for intersection detection
        all_y = []
        
        # Plot each function
        for idx, func_str in enumerate(self.graph_functions):
            try:
                y = self._evaluate_function(func_str, x)
                all_y.append(y)
                
                # Plot with color
                color = self.graph_colors[idx % len(self.graph_colors)]
                self.ax.plot(x, y, color=color, linewidth=2, label=func_str)

                # --- Vertex Visualization ---
                # Find local extrema using sign change in derivative
                dy = np.diff(y)
                extrema_idx = np.where(np.diff(np.sign(dy)))[0] + 1
                
                for e_idx in extrema_idx:
                    xe, ye = x[e_idx], y[e_idx]
                    # Only plot if within visible range
                    if self.x_min <= xe <= self.x_max and self.y_min <= ye <= self.y_max:
                        # Gold star for vertices
                        self.ax.plot(xe, ye, marker='*', markersize=8, color='#FFD700', markeredgecolor='black')
                        
                        # Add coordinate label for vertex
                        self.ax.annotate(f"Vert: ({xe:.2f}, {ye:.2f})", 
                                       xy=(xe, ye), 
                                       xytext=(0, -15), 
                                       textcoords='offset points',
                                       color='#FFD700',
                                       fontsize=8,
                                       ha='center',
                                       bbox=dict(boxstyle='round,pad=0.2', fc='black', alpha=0.6))
            except Exception as e:
                print(f"Error plotting {func_str}: {e}")
        
        # --- Intersection / Solution Detection ---
        if len(all_y) >= 2:
            import itertools
            for i, j in itertools.combinations(range(len(all_y)), 2):
                y1, y2 = all_y[i], all_y[j]
                
                # Check for sign change in difference (crossings)
                diff = y1 - y2
                # Use sign bit to find crossings
                idx_crossings = np.where(np.diff(np.sign(diff)))[0]
                
                for c_idx in idx_crossings:
                    # Linear interpolation
                    x1, x2 = x[c_idx], x[c_idx+1]
                    d1, d2 = diff[c_idx], diff[c_idx+1]
                    
                    if np.isnan(d1) or np.isnan(d2) or np.isinf(d1) or np.isinf(d2):
                        continue
                        
                    # Calculate crossing point
                    x_sol = x1 - d1 * (x2 - x1) / (d2 - d1)
                    
                    # Precise y calculation using linear interpolation on one of the functions
                    y_sol = all_y[i][c_idx] + (all_y[i][c_idx+1] - all_y[i][c_idx]) * (x_sol - x1) / (x2 - x1)
                    
                    # Only show solutions within the visible Y range
                    if self.y_min <= y_sol <= self.y_max:
                        # Plot solution point (white dot with halo)
                        self.ax.plot(x_sol, y_sol, 'wo', markersize=6, alpha=0.8)
                        self.ax.plot(x_sol, y_sol, 'yo', markersize=10, alpha=0.3) # Halo
                        
                        # Add coordinate label
                        self.ax.annotate(f"({x_sol:.2f}, {y_sol:.2f})", 
                                       xy=(x_sol, y_sol), 
                                       xytext=(5, 5), 
                                       textcoords='offset points',
                                       color='white',
                                       fontsize=8,
                                       bbox=dict(boxstyle='round,pad=0.2', fc='black', alpha=0.5))
        
        # Set labels and limits
        self.ax.set_xlabel('x', fontsize=12, color=COLOR_TEXT_WHITE)
        self.ax.set_ylabel('f(x)', fontsize=12, color=COLOR_TEXT_WHITE)
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)
        
        # Add legend if there are functions
        if self.graph_functions:
            legend = self.ax.legend(facecolor='#2d2d2d', edgecolor=COLOR_TEXT_WHITE, 
                                   fontsize=9, loc='upper right')
            for text in legend.get_texts():
                text.set_color(COLOR_TEXT_WHITE)
        
        # Style axes
        self.ax.spines['bottom'].set_color(COLOR_TEXT_WHITE)
        self.ax.spines['top'].set_color(COLOR_TEXT_WHITE)
        self.ax.spines['left'].set_color(COLOR_TEXT_WHITE)
        self.ax.spines['right'].set_color(COLOR_TEXT_WHITE)
        self.ax.tick_params(colors=COLOR_TEXT_WHITE)
        
        # Redraw canvas
        self.canvas.draw()

    # -------------------------------------------------------------------------
    # Logic & Event Handling Methods (from original calculator)
    # -------------------------------------------------------------------------

    def toggle_2nd(self):
        """
        Toggles the '2nd' mode for scientific functions (e.g., sin -> sin⁻¹).
        Updates button text and internal state.
        """
        self.second_active = not getattr(self, 'second_active', False)
        
        # Update '2nd' button visual state (Highlight when active)
        if "2nd" in self.sci_btn_labels:
            lbl = self.sci_btn_labels["2nd"]
            if self.second_active:
                lbl.config(bg=COLOR_BTN_OP, fg=COLOR_TEXT_BLACK) 
            else:
                 lbl.config(bg=COLOR_BTN_SCI, fg=COLOR_TEXT_WHITE)

        # Map of Standard Label -> Inverse Label
        mapping = {
            "sin": "sin⁻¹", "cos": "cos⁻¹", "tan": "tan⁻¹",
            "sinh": "sinh⁻¹", "cosh": "cosh⁻¹", "tanh": "tanh⁻¹",
            "ln": "e\u02e3", "log10": "10\u02e3"
        }
        
        # Update labels on the keys
        for k, new_text in mapping.items():
            if k in self.sci_btn_labels:
                lbl = self.sci_btn_labels[k]
                if self.second_active:
                    lbl.config(text=new_text)
                else:
                    lbl.config(text=k)

    def set_base(self, new_base):
        """
        Switches the number system base (Dec, Hex, Oct, Bin) in Programmer mode.
        Converts the current value to the new base.
        """
        try:
            # Parse current value back to integer first
            if "." in self.current_val:
                val = int(float(self.current_val))
            else:
                val = int(self.current_val, self.prog_base)
            self.prog_base = new_base
            
            # Convert integer to new base string
            if new_base == 16: self.current_val = hex(val).upper()[2:]
            elif new_base == 8: self.current_val = oct(val)[2:]
            elif new_base == 2: self.current_val = bin(val)[2:]
            else: self.current_val = str(val)
            
            self.update_display()
            self.clean_keyboard() 
            self.build_layout() # Rebuild to update active base highlight
            
        except Exception:
            self.prog_base = new_base

    def num(self, key):
        """
        Handles numeric input (digits 0-9, A-F, and decimal point).
        """
        if self.new_input:
            self.current_val = key
            self.new_input = False
        else:
            if key == "." and "." in self.current_val: return # Prevent multiple dots
            self.current_val += key
        self.update_display()

    def op(self, operator):
        """
        Handles operator input (+, -, *, /, etc.).
        Stores current value and operator for later calculation.
        """
        val_to_store = self.current_val
        # In Programmer mode, ensure we store decimal value for calculation
        if self.current_mode == "Programmer":
            try:
                val_to_store = str(int(self.current_val, self.prog_base))
            except: pass
            
        self.expression.append(val_to_store)
        self.expression.append(operator)
        self.new_input = True
        self.update_display() # Update display (might show partial expression)
        
    def sci_op(self, func):
        """
        Handles Scientific operations (immediately calculated functions like sin, cos, sqrt).
        Also handles random number generation.
        """
        try:
            val = float(self.current_val)
            res = 0
            is_2nd = getattr(self, 'second_active', False)
            
            # Unicode labels to match button text
            L_SQRT = "\u00B2\u221Ax" 
            L_CBRT = "\u00B3\u221Ax" 

            # --- Trigonometry ---
            if func == "sin": res = math.asin(val) if is_2nd else calculator.sin(val)
            elif func == "cos": res = math.acos(val) if is_2nd else calculator.cos(val)
            elif func == "tan": res = math.atan(val) if is_2nd else calculator.tan(val)
            
            # --- Logarithms ---
            elif func == "ln": res = math.exp(val) if is_2nd else calculator.log(val) # inv ln is e^x
            elif func == "log10": res = 10**val if is_2nd else math.log10(val)
            
            # --- Roots ---
            elif func == L_SQRT: res = calculator.sqrt(val)
            elif func == L_CBRT: res = val ** (1/3) 
            
            # --- Powers ---
            elif func == "x^2": res = val ** 2
            elif func == "x^3": res = val ** 3
            elif func == "1/x": res = 1 / val
            elif func == "2^x": res = 2 ** val
            
            # --- Other Math ---
            elif func == "x!": res = math.factorial(int(val))
            elif func == "e": res = math.e
            elif func == "pi": res = math.pi
            
            # --- Hyperbolic ---
            elif func == "sinh": res = math.asinh(val) if is_2nd else math.sinh(val)
            elif func == "cosh": res = math.acosh(val) if is_2nd else math.cosh(val)
            elif func == "tanh": res = math.atanh(val) if is_2nd else math.tanh(val)
            
            # --- Random ---
            elif func == "Rand":
                 import random
                 res = random.random()
            
            # Update current value with result
            if func in ["e", "pi", "Rand"]: self.current_val = str(res)
            else: self.current_val = str(res)
            
            self.new_input = True
            self.update_display()
        except:
            self.lbl_display.config(text="Error")

    def negate(self):
        """
        Toggles positive/negative sign of the current value.
        """
        try:
            if self.current_val.startswith("-"): self.current_val = self.current_val[1:]
            else: self.current_val = "-" + self.current_val
            self.update_display()
        except: pass

    def percent(self):
        """
        Divides the current value by 100.
        """
        try:
            val = float(self.current_val)
            self.current_val = str(val / 100)
            self.new_input = True
            self.update_display()
        except: pass

    def calculate(self):
        """
        Performs the final calculation based on the stored expression and current value.
        Handles standard math, bitwise logic, and custom scientific operators (yroot, ypow).
        """
        val_to_store = self.current_val
        if self.current_mode == "Programmer":
            try:
                val_to_store = str(int(self.current_val, self.prog_base))
            except: pass
        self.expression.append(val_to_store)
        
        full_expr = "".join(self.expression)
        try:
            # --- Pre-processing for Custom Operators ---
            # 1. Handle y^x (Reverse Power: entered as [Exp] ypow [Base], computes Base**Exp)
            while "ypow" in self.expression:
                idx = self.expression.index("ypow")
                if idx > 0 and idx < len(self.expression) - 1:
                     base = float(self.expression[idx+1])
                     exp = float(self.expression[idx-1])
                     res = base ** exp
                     self.expression[idx-1] = str(res)
                     del self.expression[idx:idx+2]
                else: break

            # 2. Handle yroot (Yth Root: entered as [Base] yroot [Root], computes Base**(1/Root))
            while "yroot" in self.expression:
                idx = self.expression.index("yroot")
                if idx > 0 and idx < len(self.expression) - 1:
                     base = float(self.expression[idx-1]) 
                     root_val = float(self.expression[idx+1])
                     if root_val == 0: res = 0 
                     else: res = base ** (1/root_val)
                     self.expression[idx-1] = str(res)
                     del self.expression[idx:idx+2]
                else: break

            # --- Evaluation ---
            local_expr = "".join(self.expression)
            
            # Replace Programmer Mode text operators with Python bitwise operators
            local_expr = local_expr.replace("AND", "&").replace("OR", "|").replace("XOR", "^").replace("NOT", "~")
            # Ensure bitwise shifts are valid symbols (redundant but safe)
            local_expr = local_expr.replace("<<", "<<").replace(">>", ">>")
            
            res = eval(local_expr) # Execute standard Python math
            
            # --- Result Formatting ---
            if self.current_mode == "Programmer":
                res = int(res)
                # Convert result back to current base
                if self.prog_base == 16: self.current_val = hex(res).upper()[2:]
                elif self.prog_base == 8: self.current_val = oct(res)[2:]
                elif self.prog_base == 2: self.current_val = bin(res)[2:]
                else: self.current_val = str(res)
            else:
                self.current_val = str(res)
                
            self.expression = []
            self.new_input = True
            self.update_display()
        except:
            self.lbl_display.config(text="Error")
            self.expression = []
            self.new_input = True

    def clear(self):
        """
        Clears the inputs and resets the calculator state.
        """
        self.current_val = "0"
        self.expression = []
        self.new_input = True
        self.update_display()

    def to_superscript(self, text):
        """
        Converts digits to unicode superscript characters for display.
        Used for power expressions like 5².
        """
        mapping = {
            "0":"\u2070", "1":"\u00B9", "2":"\u00B2", "3":"\u00B3", "4":"\u2074", 
            "5":"\u2075", "6":"\u2076", "7":"\u2077", "8":"\u2078", "9":"\u2079",
            "-":"\u207B", "+":"\u207A", ".":"\u02D9", " ":" "
        }
        res = ""
        for char in str(text):
            res += mapping.get(char, char)
        return res

    def update_display(self):
        """
        Updates the display label with the current value or expression.
        Handles formatting for power functions to show base^exponent style.
        """
        
        # --- Handle Power Function Formatting (Base^Exp) ---
        if "**" in self.expression:
            # Standard Power: Base ^ Exponent
            base = self.expression[0] if self.expression else ""
            exponent = self.current_val
            txt = f"{base}{self.to_superscript(exponent)}"
            
            # Truncate if too long (simple approach)
            if len(txt) > 25: txt = "..." + txt[-25:]
            self.lbl_display.config(text=txt)
            
        elif "ypow" in self.expression:
            # Reverse Power: We want to show Base ^ (typed Exponent)
            exp_val = self.expression[0] if self.expression else "" # This is the exponent
            base_val = self.current_val # This is the base
            
            if base_val == "0" and self.new_input:
                txt = f"?{self.to_superscript(exp_val)}"
            else:
                txt = f"{base_val}{self.to_superscript(exp_val)}"
                
            if len(txt) > 25: txt = "..." + txt[-25:]
            self.lbl_display.config(text=txt)
            
        else:
            # --- Standard Display ---
            disp_txt = self.current_val
            if len(disp_txt) > 20: disp_txt = "..." + disp_txt[-20:]
            self.lbl_display.config(text=disp_txt)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
