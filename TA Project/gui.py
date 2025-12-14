import tkinter as tk
from tkinter import filedialog, messagebox
import json
from pda_engine import NPDA

class PDASimulatorGUI:
    def __init__(self, root):
        self.root = root
        root.title("Advanced PDA Simulator")
        root.geometry("1000x600")

        self.pda = None

        top = tk.Frame(root)
        top.pack(pady=10)

        tk.Button(top, text="Load PDA (JSON)", command=self.load_pda).pack(side="left", padx=5)

        tk.Label(top, text="Input String:").pack(side="left")
        self.input_entry = tk.Entry(top, width=30)
        self.input_entry.pack(side="left", padx=5)

        tk.Button(top, text="Run Simulation", command=self.run).pack(side="left", padx=5)

        self.output = tk.Text(root, height=30, font=("Consolas", 11))
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def load_pda(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not path:
            return

        with open(path) as f:
            data = json.load(f)

        self.pda = NPDA(data)
        self.output.insert("end", f"PDA Loaded: {path}\n\n")

    def run(self):
        if not self.pda:
            messagebox.showerror("Error", "Load a PDA first!")
            return

        input_string = self.input_entry.get()
        accepted, trace = self.pda.simulate(input_string)

        self.output.insert("end", "---- Simulation Start ----\n")
        for step in trace:
            self.output.insert("end", step + "\n")

        result = "ACCEPTED" if accepted else "REJECTED"
        self.output.insert("end", f"\nRESULT: {result}\n")
        self.output.insert("end", "---- Simulation End ----\n\n")

root = tk.Tk()
PDASimulatorGUI(root)
root.mainloop()
