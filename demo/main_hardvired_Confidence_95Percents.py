import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.stats import t
import numpy as np

def confidence_to_alpha(confidence):
    return round(1 - confidence / 100, 4)

def calculate_r_critical(alpha, n, tail_type="2-tailed"):
    df = n - 2
    if df <= 0:
        raise ValueError("Sample size must be at least 3.")
    if tail_type == "1-tailed":
        t_crit = t.ppf(1 - alpha, df)
    else:
        t_crit = t.ppf(1 - alpha / 2, df)
    r_crit = t_crit / np.sqrt(t_crit ** 2 + df)
    return r_crit, t_crit, df

def on_confidence_change(*args):
    level = confidence_level.get()
    if level in confidence_alpha_map:
        alpha = confidence_alpha_map[level]
        entry_alpha.delete(0, tk.END)
        entry_alpha.insert(0, str(alpha))

def calculate_and_plot():
    try:
        alpha = float(entry_alpha.get())
        n = int(entry_n.get())
        tail_type = tail_mode.get()

        r_critical, t_critical, df = calculate_r_critical(alpha, n, tail_type)

        result_label.config(text=f"Critical r-value (±): {r_critical:.3f}")

        ax.clear()
        x_vals = np.linspace(-5, 5, 1000)
        y_vals = t.pdf(x_vals, df)
        ax.plot(x_vals, y_vals, color='black', label='t-distribution')

        if tail_type == "1-tailed":
            x_fill = np.linspace(t_critical, 5, 500)
            ax.fill_between(x_fill, t.pdf(x_fill, df), color='red', alpha=0.5, label=f'Critical region (α = {alpha})')
            ax.axvline(t_critical, color='red', linestyle='--', label=f't_critical = {t_critical:.3f}')
        else:
            t_crit_pos = t_critical
            t_crit_neg = -t_critical
            ax.fill_between(np.linspace(t_crit_pos, 5, 500), t.pdf(np.linspace(t_crit_pos, 5, 500), df), color='red', alpha=0.5, label=f'Right critical region (α/2 = {alpha / 2})')
            ax.fill_between(np.linspace(-5, t_crit_neg, 500), t.pdf(np.linspace(-5, t_crit_neg, 500), df), color='blue', alpha=0.5, label=f'Left critical region (α/2 = {alpha / 2})')
            ax.axvline(t_crit_pos, color='red', linestyle='--', label=f'+t_critical = {t_crit_pos:.3f}')
            ax.axvline(t_crit_neg, color='blue', linestyle='--', label=f'-t_critical = {t_crit_neg:.3f}')

        ax.set_title("t-Distribution with Critical Region", fontsize=18)
        ax.set_xlabel('t-value', fontsize=14)
        ax.set_ylabel('Probability Density', fontsize=14)
        ax.legend(fontsize=12)
        canvas.draw()

        calc_summary.config(text=f"""n = {n}
df = {df}
α = {alpha}
t_critical = {t_critical:.4f}
r_critical = ± {r_critical:.4f} ({tail_type})""")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_plot():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        fig.savefig(file_path)
        messagebox.showinfo("Saved", f"Plot saved to:\n{file_path}")

def exit_app():
    plt.close('all')
    root.destroy()

# -------------------------- GUI START ----------------------------

root = tk.Tk()
root.title("Critical r-value Calculator and Visualizer AJ")
root.geometry("1600x1000")
root.protocol("WM_DELETE_WINDOW", exit_app)

# Confidence Level to Alpha Mapping
confidence_alpha_map = {"90%": 0.10, "95%": 0.05, "99%": 0.01}
confidence_level = tk.StringVar(value="95%")
confidence_level.trace_add("write", on_confidence_change)

# -------- Top Frame --------
top_frame = tk.Frame(root, padx=10, pady=10)
top_frame.pack(fill=tk.X)

tk.Label(top_frame, text="Confidence Level:", font=("Arial", 18)).pack(side=tk.LEFT)
confidence_menu = tk.OptionMenu(top_frame, confidence_level, *confidence_alpha_map.keys())
confidence_menu.config(font=("Arial", 18))
confidence_menu.pack(side=tk.LEFT, padx=10)

tk.Label(top_frame, text="Significance Level (α):", font=("Arial", 18)).pack(side=tk.LEFT)
entry_alpha = tk.Entry(top_frame, width=6, font=("Arial", 18))
entry_alpha.insert(0, "0.05")
entry_alpha.pack(side=tk.LEFT, padx=10)

tk.Label(top_frame, text="Sample Size (n):", font=("Arial", 18)).pack(side=tk.LEFT)
entry_n = tk.Entry(top_frame, width=6, font=("Arial", 18))
entry_n.insert(0, "14")
entry_n.pack(side=tk.LEFT, padx=10)

tail_mode = tk.StringVar(value="2-tailed")
tk.Label(top_frame, text="Test Type:", font=("Arial", 18)).pack(side=tk.LEFT)
tail_option = tk.OptionMenu(top_frame, tail_mode, "1-tailed", "2-tailed")
tail_option.config(font=("Arial", 18))
tail_option.pack(side=tk.LEFT, padx=10)

tk.Button(top_frame, text="Calculate & Plot", command=calculate_and_plot, bg="#007acc", fg="white", font=("Arial", 18, "bold")).pack(side=tk.LEFT, padx=10)
tk.Button(top_frame, text="💾 Save Plot", command=save_plot, bg="#28a745", fg="white", font=("Arial", 18, "bold")).pack(side=tk.LEFT, padx=10)
tk.Button(top_frame, text="❌ Exit", command=exit_app, bg="#cc0000", fg="white", font=("Arial", 18, "bold")).pack(side=tk.LEFT, padx=10)

# -------- Result --------
result_label = tk.Label(root, text="Critical r-value (±):", font=("Arial", 22, "bold"))
result_label.pack(pady=10)

# -------- Plot Frame --------
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

left_panel = tk.Frame(main_frame)
left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(9, 6))
canvas = FigureCanvasTkAgg(fig, master=left_panel)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

right_panel = tk.Frame(main_frame, bg="#f0f6ff", width=520, padx=20)
right_panel.pack(side=tk.RIGHT, fill=tk.Y)
right_panel.pack_propagate(0)

tk.Label(
    right_panel, text="🧮 Calculation Summary",
    font=("Helvetica", 22, "bold"), bg="#f0f6ff", fg="#003366"
).pack(pady=(10, 5))

calc_summary = tk.Label(
    right_panel, text="", bg="#f0f6ff",
    justify="left", font=("Courier", 18)
)
calc_summary.pack(pady=10, anchor="w")

tk.Label(
    right_panel, text="📘 Explanation",
    font=("Helvetica", 22, "bold"), bg="#f0f6ff", fg="#003366"
).pack(pady=(10, 5))

legend = tk.Label(
    right_panel,
    text=(
        "This tool calculates the critical Pearson r-value\n"
        "from significance level (α) and sample size (n).\n\n"
        "Inputs:\n"
        "  • Confidence level (%): 90, 95, or 99\n"
        "  • α (Significance Level) — default from Confidence\n"
        "  • n (Sample size ≥ 3)\n"
        "  • Test type: 1-tailed or 2-tailed\n\n"
        "Outputs:\n"
        "  • df = n - 2\n"
        "  • t_critical from t-distribution\n"
        "  • r_critical (correlation cutoff)"
    ),
    bg="#f0f6ff", justify="left", font=("Helvetica", 16), anchor="w", wraplength=500
)
legend.pack(pady=(0, 10), anchor="w")

# Run GUI loop
root.mainloop()
