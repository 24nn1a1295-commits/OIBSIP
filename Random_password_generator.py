
import string
import secrets
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

AMBIGUOUS = set("0O1lI")


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("520x560")
        self.root.resizable(False, False)

        self.history = []

        self.length_var = tk.IntVar(value=12)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)

        self.password_var = tk.StringVar()
        self.strength_var = tk.StringVar(value="Strength: Medium")

        self.build_ui()

    def build_ui(self):
        title = ttk.Label(self.root, text="Secure Password Generator", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="x")

        ttk.Label(frame, text="Password Length").pack(anchor="w")
        ttk.Spinbox(frame, from_=8, to=64, textvariable=self.length_var, width=8).pack(anchor="w", pady=(0, 10))

        ttk.Label(frame, text="Include Character Types").pack(anchor="w")
        ttk.Checkbutton(frame, text="Uppercase (A-Z)", variable=self.upper_var).pack(anchor="w")
        ttk.Checkbutton(frame, text="Lowercase (a-z)", variable=self.lower_var).pack(anchor="w")
        ttk.Checkbutton(frame, text="Numbers (0-9)", variable=self.digits_var).pack(anchor="w")
        ttk.Checkbutton(frame, text="Symbols (!@#$...)", variable=self.symbols_var).pack(anchor="w")

        ttk.Checkbutton(
            frame,
            text="Exclude ambiguous characters (0, O, 1, l, I)",
            variable=self.exclude_ambiguous_var,
        ).pack(anchor="w", pady=(8, 0))

        ttk.Button(frame, text="Generate Password", command=self.generate_password).pack(fill="x", pady=12)

        ttk.Label(frame, text="Generated Password").pack(anchor="w")
        entry = ttk.Entry(frame, textvariable=self.password_var, font=("Consolas", 12), state="readonly")
        entry.pack(fill="x", pady=(0, 8))

        ttk.Button(frame, text="Copy to Clipboard", command=self.copy_password).pack(fill="x")

        ttk.Label(frame, textvariable=self.strength_var).pack(anchor="w", pady=(10, 4))
        self.progress = ttk.Progressbar(frame, maximum=100)
        self.progress.pack(fill="x")

        ttk.Label(frame, text="Last 5 Generated Passwords").pack(anchor="w", pady=(12, 4))
        self.history_box = tk.Listbox(frame, height=5)
        self.history_box.pack(fill="both", expand=True)

        if not CLIPBOARD_AVAILABLE:
            ttk.Label(
                frame,
                text="Install pyperclip for clipboard support: pip install pyperclip",
                foreground="gray",
            ).pack(anchor="w", pady=(8, 0))

    def build_pool(self):
        pools = []

        if self.upper_var.get():
            chars = string.ascii_uppercase
            if self.exclude_ambiguous_var.get():
                chars = "".join(c for c in chars if c not in AMBIGUOUS)
            pools.append(chars)

        if self.lower_var.get():
            chars = string.ascii_lowercase
            if self.exclude_ambiguous_var.get():
                chars = "".join(c for c in chars if c not in AMBIGUOUS)
            pools.append(chars)

        if self.digits_var.get():
            chars = string.digits
            if self.exclude_ambiguous_var.get():
                chars = "".join(c for c in chars if c not in AMBIGUOUS)
            pools.append(chars)

        if self.symbols_var.get():
            pools.append(string.punctuation)

        return pools

    def generate_password(self):
        length = self.length_var.get()
        pools = self.build_pool()

        if length < 8:
            messagebox.showerror("Invalid Length", "Password length must be at least 8 characters.")
            return

        if len(pools) < 2:
            messagebox.showerror(
                "Selection Error",
                "Select at least two character types for a stronger password.",
            )
            return

        required = [secrets.choice(pool) for pool in pools]
        all_chars = "".join(pools)

        remaining = [secrets.choice(all_chars) for _ in range(length - len(required))]
        password_list = required + remaining
        secrets.SystemRandom().shuffle(password_list)
        password = "".join(password_list)

        self.password_var.set(password)
        self.update_strength(password, pools)
        self.add_history(password)

        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)

    def update_strength(self, password, pools):
        length = len(password)
        diversity = len(pools)

        score = 0
        if length >= 8:
            score += 25
        if length >= 12:
            score += 25
        if diversity >= 3:
            score += 25
        if diversity == 4:
            score += 25

        self.progress["value"] = score

        if score < 50:
            label = "Weak"
        elif score < 75:
            label = "Medium"
        else:
            label = "Strong"

        self.strength_var.set(f"Strength: {label}")

    def add_history(self, password):
        self.history.insert(0, password)
        self.history = self.history[:5]

        self.history_box.delete(0, tk.END)
        for item in self.history:
            self.history_box.insert(tk.END, item)

    def copy_password(self):
        password = self.password_var.get()
        if not password:
            messagebox.showinfo("Nothing to Copy", "Generate a password first.")
            return

        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard.")
        else:
            messagebox.showwarning(
                "Clipboard Unavailable",
                "Install pyperclip: pip install pyperclip",
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
    
