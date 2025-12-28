import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import numpy as np
from pda_engine import PDA

class PDASimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 PROFESSIONAL PDA SIMULATOR")
        self.root.geometry("1600x1000")
        self.pda = PDA()
        self.accepted = False
        self.setup_ui()

    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#0D47A1')
        title_frame.pack(fill='x', pady=10)
        tk.Label(title_frame, text="🎓 PUSHDOWN AUTOMATON SIMULATOR", font=("Arial", 28, "bold"), 
                fg='white', bg='#0D47A1').pack(pady=15)

        # Controls
        control_frame = ttk.LabelFrame(self.root, text="Control Panel", padding=25)
        control_frame.pack(fill="x", padx=25, pady=10)

        ttk.Label(control_frame, text="Input String:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.input_entry = ttk.Entry(control_frame, width=25, font=("Courier", 16))
        self.input_entry.grid(row=0, column=1, padx=15)
        self.input_entry.insert(0, "aa")

        ttk.Label(control_frame, text="Language:", font=("Arial", 12, "bold")).grid(row=0, column=2, sticky="w", padx=(25,0))
        self.sample = tk.StringVar(value="Even number of a")
        self.dropdown = ttk.Combobox(control_frame, textvariable=self.sample, state="readonly", width=18)
        self.dropdown["values"] = ["Even number of a", "Odd number of a", "Balanced Parentheses", "Even Palindrome", "a^n b^n"]
        self.dropdown.grid(row=0, column=3, padx=15)

        ttk.Button(control_frame, text="▶ START", command=self.start).grid(row=0, column=4, padx=15)
        ttk.Button(control_frame, text="⏭ STEP", command=self.next_step).grid(row=0, column=5, padx=15)
        ttk.Button(control_frame, text="📊 FA DIAGRAM", command=self.show_fa_diagram).grid(row=0, column=6, padx=15)

        self.status = tk.Label(control_frame, text="READY", font=("Arial", 16, "bold"), fg="darkgreen", bg="lightgreen")
        self.status.grid(row=1, column=0, columnspan=7, pady=15, sticky="ew")

        # Main panels
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=25, pady=10)

        table_frame = ttk.LabelFrame(main_frame, text="COMPUTATION STEPS", padding=15)
        table_frame.pack(side="left", fill="both", expand=True, padx=(0,15))

        self.table = ttk.Treeview(table_frame, columns=("Step", "Input", "Action", "Stack"), show="headings", height=25)
        self.table.heading("Step", text="STEP")
        self.table.heading("Input", text="INPUT")
        self.table.heading("Action", text="TRANSITION")
        self.table.heading("Stack", text="STACK TOP")
        self.table.column("Step", width=80)
        self.table.column("Input", width=100)
        self.table.column("Action", width=350)
        self.table.column("Stack", width=120)
        self.table.pack(fill="both", expand=True)

        stack_frame = ttk.LabelFrame(main_frame, text="STACK", padding=20)
        stack_frame.pack(side="right", fill="y")

        self.stack_label = tk.Label(stack_frame, text="STACK EMPTY", font=("Courier", 20, "bold"), fg="navy", bg="#E1F5FE")
        self.stack_label.pack(pady=20)

        self.stack_list = tk.Listbox(stack_frame, height=25, font=("Courier", 18, "bold"), bg="#E8F5E8")
        self.stack_list.pack(fill="y", pady=10)

    def start(self):
        self.table.delete(*self.table.get_children())
        self.stack_list.delete(0, tk.END)
        self.pda.reset()
        input_str = self.input_entry.get().strip()
        
        self.accepted = self.pda.run_simulation(self.sample.get(), input_str)
        self.status.config(text=f"✓ {len(self.pda.steps)} STEPS | {'✅ ACCEPTED' if self.accepted else '❌ REJECTED'}", 
                          fg="darkgreen" if self.accepted else "darkred")

    def next_step(self):
        step = self.pda.next_step()
        if step:
            self.table.insert("", "end", values=(step["step"], step["input"], step["action"], step["stack_top"]))
            self.update_stack(step["stack"])

    def update_stack(self, stack):
        self.stack_list.delete(0, tk.END)
        self.stack_label.config(text=f"STACK: {len(stack)}")
        for sym in reversed(stack):
            self.stack_list.insert(tk.END, f"  {sym}  ")

    def show_fa_diagram(self):
        if not self.pda.steps:
            messagebox.showwarning("ERROR", "Run START first!")
            return

        fig, ax = plt.subplots(figsize=(24, 14), facecolor='white')
        ax.set_xlim(-3, len(self.pda.steps)*2 + 6)
        ax.set_ylim(-7, 8)
        ax.axis('off')

        positions = np.linspace(3, len(self.pda.steps)*2 + 1, len(self.pda.steps) + 2)

        # START STATE
        ax.arrow(-1.5, 0, 3.5, 0, head_width=0.3, fc='black', lw=5)
        start_circle = Circle((positions[0], 0), 0.5, fc='#4CAF50', ec='darkgreen', lw=6)
        ax.add_patch(start_circle)
        ax.text(positions[0], 0.15, 'q₀', ha='center', va='center', fontsize=24, fontweight='bold', color='white')

        # COMPUTATION STATES
        for i, step in enumerate(self.pda.steps):
            x = positions[i+1]
            state_circle = Circle((x, 0), 0.45, fc='#2196F3', ec='#1976D2', lw=5)
            ax.add_patch(state_circle)
            ax.text(x, 0.15, f'q{step["step"]}', ha='center', fontsize=22, fontweight='bold', color='white')
            ax.text(x, -0.7, step["input"], ha='center', fontsize=32, fontweight='bold', color='black')

        # FINAL STATE
        final_x = positions[-1]
        if self.accepted:
            outer = Circle((final_x, 0), 0.7, fc='none', ec='#4CAF50', lw=8)
            inner = Circle((final_x, 0), 0.5, fc='#4CAF50', ec='darkgreen', lw=6)
            ax.add_patch(outer)
            ax.add_patch(inner)
            ax.text(final_x, 0.15, 'F', ha='center', fontsize=28, fontweight='bold', color='white')
        else:
            reject_box = Rectangle((final_x-0.6, -0.8), 1.2, 1.6, fc='#F44336', ec='darkred', lw=5)
            ax.add_patch(reject_box)
            ax.text(final_x, 0, '✗', ha='center', fontsize=40, fontweight='bold', color='white')

        # 🎯 PERFECT ARROWS WITH TRANSITION LABELS
        for i in range(len(self.pda.steps)):
            start_x, end_x = positions[i], positions[i+1]
            
            # ARROW (thick + curved)
            ax.annotate('', xy=(end_x-0.3, 0.1), xytext=(start_x+0.3, -0.1),
                       arrowprops=dict(arrowstyle='->', lw=6, color='black',
                                     connectionstyle="arc3,rad=0.2"))
            
            # TRANSITION LABEL (HUGE + POSITIONED ON ARROW)
            label = self.pda.steps[i]['action']
            mid_x = (start_x + end_x) / 2
            mid_y = 1.2  # Positioned ABOVE arrow
            
            # WHITE BACKGROUND BOX + BLACK TEXT
            ax.text(mid_x, mid_y, label, ha='center', va='center', fontsize=18, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.6", fc='white', ec='black', lw=2),
                   transform=ax.transData)

        # INPUT TAPE
        tape_start = positions[0] - 1.5
        tape_end = positions[-1] + 1.5
        tape = Rectangle((tape_start, -5), tape_end-tape_start, 1, fc='#FF5722', ec='darkorange', lw=6)
        ax.add_patch(tape)
        ax.text((tape_start+tape_end)/2, -4.5, self.input_entry.get(), ha='center', fontsize=28, fontweight='bold', color='white')

        # INFO
        info_x = (positions[0] + positions[-1])/2
        ax.text(info_x, 6.5, f"LANGUAGE: {self.sample.get()}", ha='center', fontsize=26, fontweight='bold')
        result_text = f"RESULT: {'ACCEPTED ✓' if self.accepted else 'REJECTED ✗'}"
        ax.text(info_x, 5.8, result_text, ha='center', fontsize=24, fontweight='bold', 
               color='darkgreen' if self.accepted else 'darkred')

        plt.suptitle("PUSHDOWN AUTOMATON - COMPUTATION PATH", fontsize=32, fontweight='bold', y=0.95)
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(0.1)
        self.status.config(text="✅ FA WITH TRANSITION LABELS!", fg="darkgreen")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDASimulator(root)
    root.mainloop()
