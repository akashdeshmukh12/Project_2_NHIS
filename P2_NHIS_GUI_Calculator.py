

# ── STEP 1: Import required modules ──────────────────────
# tkinter   : GUI library (built into Python)
# math      : Provides mathematical functions (sin, cos, etc.)
import tkinter as tk
import math


# ── STEP 2: Define the Calculator Application class ──────



class ScientificCalculator:

    def __init__(self, root):


        # ── STEP 3: Configure the main window ────────────
        
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.configure(bg="#1a1a2e")          # dark navy background
        self.root.resizable(False, False)           # fixed window size

        # ── STEP 4: State variable ────────────────────────
        # StringVar is a tkinter-aware string. When we change it,
        # the display widget updates automatically (data binding).
        
        self.expression = tk.StringVar()
        self.expression.set("0")                   # start with "0"

        # Track whether we're in Degrees or Radians mode
        
        self.use_degrees = True

        # ── STEP 5: Build the UI ──────────────────────────
        
        self._build_display()
        self._build_buttons()




    # STEP 6: Build the display screen
    

    def _build_display(self):
        display_frame = tk.Frame(self.root, bg="#1a1a2e")
        display_frame.pack(fill="x", padx=10, pady=(15, 5))

        self.display = tk.Entry(
            display_frame,
            textvariable=self.expression,   # link to our StringVar
            font=("Helvetica", 26, "bold"),
            bg="#7083b9",                   # slightly lighter dark blue
            fg="#100f0f",                   # white text
            bd=0,
            justify="right",                # numbers align to the right
            state="readonly",               # user cannot type directly
            insertbackground="white",
            relief="flat",
        )
        self.display.pack(fill="x", ipady=15, padx=5)


    # STEP 7: Define ALL button configurations
    

    def _build_buttons(self):

        # Colour palette matching the phone screenshot
        DARK   = "#2d2d44"      # default button colour
        BLUE   = "#0078d4"      # highlight colour (AC button)
        LIGHT  = "#3d3d5c"      # slightly lighter buttons
        TEXT   = "#ffffff"
        CYAN   = "#4cc9f0"      # trig / special function colour
        ORANGE = "#f77f00"      # operator colour

        # ── Button layout ────────────────────────────────
        # (text, col, row, action, bg, fg)
        buttons = [
            # Row 0 — Control row
            ("AC",  0, 0, "AC",   BLUE,   TEXT),
            ("C",   1, 0, "DEL",  DARK,   "#ff6b6b"),
            ("Deg", 4, 0, "Deg",  DARK,   TEXT),
            ("e",   3, 0, "e",    LIGHT,  CYAN),
            ("√",   5, 0, "sqrt", LIGHT,  CYAN),
            ("π",   2, 0, "pi",   LIGHT,  CYAN),

            # Row 1 — 7 8 9 and functions
            ("7",   0, 1, "7",    DARK,   TEXT),
            ("8",   1, 1, "8",    DARK,   TEXT),
            ("9",   2, 1, "9",    DARK,   TEXT),
            ("( )", 3, 1, "()",   LIGHT,  TEXT),
            ("log", 4, 1, "log",  LIGHT,  CYAN),
            ("sin", 5, 1, "sin",  LIGHT,  CYAN),
            

            # Row 2 — 4 5 6 and functions
            ("4",   0, 2, "4",    DARK,   TEXT),
            ("5",   1, 2, "5",    DARK,   TEXT),
            ("6",   2, 2, "6",    DARK,   TEXT),
            ("%",   3, 2, "%",    LIGHT,  TEXT),
            ("ln",  4, 2, "ln",   LIGHT,  CYAN),
            ("cos", 5, 2, "cos",  LIGHT,  CYAN),
            

            # Row 3 — 1 2 3 and functions
            ("1",   0, 3, "1",    DARK,   TEXT),
            ("2",   1, 3, "2",    DARK,   TEXT),
            ("3",   2, 3, "3",    DARK,   TEXT),
            ("÷",   3, 3, "/",    LIGHT,  ORANGE),
            ("+",   4,3, "+",    LIGHT,  ORANGE),
            ("tan", 5, 3, "tan",  LIGHT,  CYAN),
            

            # Row 4 — 0 . operators
            ("0",   0, 4, "0",    DARK,   TEXT),
            (".",   1, 4, ".",    DARK,   TEXT),
            ("=",   2, 4, "=",    "#e040fb", TEXT),  # purple = button
            ("×",   3, 4, "*",    LIGHT,  ORANGE),
            ("−",   4, 4, "-",    LIGHT,  ORANGE),
            ("^",   5, 4, "^",    LIGHT,  ORANGE),
        ]

        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(padx=8, pady=8)

        # ── STEP 8: Create each button dynamically ────────
        # We use a lambda to "capture" the current action value
        # for each buttons.
        
        for (text, col, row, action, bg, fg) in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Helvetica", 14, "bold"),
                width=5,
                height=2,
                bg=bg,
                fg=fg,
                activebackground="#555577",
                activeforeground=TEXT,
                bd=0,
                relief="flat",
                cursor="hand2",
                command=lambda a=action: self._click(a),   # lambda captures 'a'
            )
            btn.grid(row=row, column=col, padx=3, pady=3)


    # STEP 9: Handle button clicks
    # This single method handles ALL button presses by
    # checking what 'action' was passed in.
    
    def _click(self, action):
        current = self.expression.get()

        # Helper: replace display with new value
        
        def set_expr(val):
            self.expression.set(val)

        # ── Clear all ────────────────────────────────────
        
        if action == "AC":
            set_expr("0")

        # ── Delete last character (backspace) ─────────────
        
        elif action == "DEL":
            new = current[:-1]
            set_expr(new if new and new != "-" else "0")

        # ── Toggle Degrees / Radians ──────────────────────
        
        elif action == "Deg":
            self.use_degrees = not self.use_degrees
            mode = "Deg" if self.use_degrees else "Rad"
            # Update the Deg/Rad button label
            self._update_deg_button(mode)


        # ── Square root ───────────────────────────────────
        
        elif action == "sqrt":
            try:
                result = math.sqrt(float(eval(current)))
                set_expr(self._format(result))
            except Exception:
                set_expr("Error")

        # ── Auto-bracket balancer () ─────────────────────
        
        elif action == "()":
            open_count = current.count("(") - current.count(")")
            if open_count <= 0:
                new = ("" if current == "0" else current) + "("
            else:
                new = current + ")"
            set_expr(new)

        # ── Mathematical constants ─────────────────────────
        
        elif action == "pi":
            append = "3.14159265358979"
            set_expr("" if current == "0" else current + append)
            set_expr(("" if current == "0" else current) + append)

        elif action == "e":
            append = "2.71828182845905"
            set_expr(("" if current == "0" else current) + append)

        # ── Trigonometric functions ────────────────────────
        # We evaluate the current expression first, then apply the function.
        
        elif action in ("sin", "cos", "tan"):
            try:
                val = float(eval(current))
                angle = math.radians(val) if self.use_degrees else val
                result = getattr(math, action)(angle)
                set_expr(self._format(result))
            except Exception:
                set_expr("Error")

        # ── Logarithms ──────
        elif action == "ln":
            try:
                result = math.log(float(eval(current)))
                set_expr(self._format(result))
            except Exception:
                set_expr("Error")

        elif action == "log":
            try:
                result = math.log10(float(eval(current)))
                set_expr(self._format(result))
            except Exception:
                set_expr("Error")

        # ── Evaluate expression ────
        # eval() parses and computes a math string.
        # We replace ^ with ** because Python uses ** for powers.

        elif action == "=":
            try:
                expr = current.replace("^", "**")
                result = eval(expr)         
                set_expr(self._format(result))
            except ZeroDivisionError:
                set_expr("÷ by 0!")
            except Exception:
                set_expr("Error")

        # ── Append digit or operator ─────

        else:
            if current == "0" and action not in ("+", "-", "*", "/", "."):
                set_expr(action)
            else:
                set_expr(current + action)

    # STEP 10: Format the result nicely
    # If the result is a whole number (e.g. 4.0) show it as
    # "4" instead of "4.0". Otherwise round to 10 decimals
    # to avoid floating-point noise like 0.30000000000000004.

    def _format(self, value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(round(value, 10))

    # Helper: update the Deg/Rad button text live

    def _update_deg_button(self, mode):
        for widget in self.root.winfo_children():
            for child in widget.winfo_children():
                if hasattr(child, "cget") and child.cget("text") in ("Deg", "Rad"):
                    child.config(text=mode)


# ── STEP 11: Entry point ──────────────────────────────────
# This block runs only when the script is executed directly
# (not when imported as a module). It creates the window
# and starts the tkinter event loop, which waits for user
# interactions (clicks, key presses) forever until closed.

if __name__ == "__main__":
    root = tk.Tk()                          # create the main window
    app = ScientificCalculator(root)        # instantiate our calculator
    root.mainloop()                         # start listening for events
