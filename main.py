import tkinter as tk
from tkinter import messagebox

from password_checker import check_password_strength
from password_generator import generate_password

import hashlib
import sqlite3

# ---------------------------
# Analyze Password Function
# ---------------------------

def analyze_password():

    password = password_entry.get()

    if password == "":
        messagebox.showwarning("Warning", "Please enter a password.")
        return

    strength, suggestions = check_password_strength(password)

    strength_label.config(text=f"Strength: {strength}")

    suggestions_text.delete(1.0, tk.END)

    if suggestions:
        for s in suggestions:
            suggestions_text.insert(tk.END, f"• {s}\n")
    else:
        suggestions_text.insert(tk.END, "Excellent Password!")

    # Check password reuse
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM passwords WHERE password_hash=?",
        (hashed_password,)
    )

    existing = cursor.fetchone()

    if existing:
        reuse_label.config(
            text="Password already used before!",
            fg="red"
        )
    else:
        reuse_label.config(
            text="Password is unique.",
            fg="green"
        )

        cursor.execute(
            "INSERT INTO passwords(password_hash) VALUES(?)",
            (hashed_password,)
        )

        conn.commit()

    conn.close()

# ---------------------------
# Generate Password Function
# ---------------------------

def generate_strong_password():

    strong_password = generate_password()

    generated_password_label.config(
        text=strong_password
    )

# ---------------------------
# GUI Window
# ---------------------------

root = tk.Tk()

root.title("Password Strength Analyzer")
root.geometry("500x500")
root.resizable(False, False)

# ---------------------------
# Title
# ---------------------------

title_label = tk.Label(
    root,
    text="PASSWORD STRENGTH ANALYZER",
    font=("Arial", 16, "bold")
)

title_label.pack(pady=10)

# ---------------------------
# Password Entry
# ---------------------------

password_label = tk.Label(
    root,
    text="Enter Password:",
    font=("Arial", 12)
)

password_label.pack()

password_entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 12),
    show="*"
)

password_entry.pack(pady=10)

# ---------------------------
# Analyze Button
# ---------------------------

analyze_button = tk.Button(
    root,
    text="Analyze Password",
    command=analyze_password,
    bg="lightblue",
    font=("Arial", 11)
)

analyze_button.pack(pady=10)

# ---------------------------
# Strength Result
# ---------------------------

strength_label = tk.Label(
    root,
    text="Strength:",
    font=("Arial", 12, "bold")
)

strength_label.pack(pady=10)

# ---------------------------
# Suggestions
# ---------------------------

suggestions_label = tk.Label(
    root,
    text="Suggestions:",
    font=("Arial", 12)
)

suggestions_label.pack()

suggestions_text = tk.Text(
    root,
    height=6,
    width=45,
    font=("Arial", 10)
)

suggestions_text.pack(pady=10)

# ---------------------------
# Reuse Detection
# ---------------------------

reuse_label = tk.Label(
    root,
    text="",
    font=("Arial", 11, "bold")
)

reuse_label.pack(pady=5)

# ---------------------------
# Generate Password Button
# ---------------------------

generate_button = tk.Button(
    root,
    text="Generate Strong Password",
    command=generate_strong_password,
    bg="lightgreen",
    font=("Arial", 11)
)

generate_button.pack(pady=10)

generated_password_label = tk.Label(
    root,
    text="",
    font=("Arial", 12, "bold"),
    fg="blue"
)

generated_password_label.pack(pady=10)

# ---------------------------
# Run App
# ---------------------------

root.mainloop()