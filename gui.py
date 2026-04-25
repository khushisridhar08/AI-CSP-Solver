import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox

from solver import solve
from magic_square import create_magic_square_csp
from exam_scheduling import create_exam_scheduling_csp



class CSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSP Solver Project")
        self.root.geometry("900x650")

        self.method_var = tk.StringVar(value="4")

        self.bg = "#f4f6f8"
        self.card_bg = "#ffffff"
        self.primary = "#2563eb"
        self.primary_dark = "#1e40af"
        self.text = "#111827"
        self.muted = "#4b5563"

        self.root.configure(bg=self.bg)

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.home_frame = tk.Frame(self.container, padx=20, pady=20)
        self.magic_frame = tk.Frame(self.container, padx=20, pady=20)
        self.exam_frame = tk.Frame(self.container, padx=20, pady=20)

        for frame in [self.home_frame, self.magic_frame, self.exam_frame]:
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_home_page()
        self.create_magic_page()
        self.create_exam_page()

        self.show_frame(self.home_frame)

    def show_frame(self, frame):
        frame.tkraise()
        self.root.update_idletasks()

    def go_home(self):
        self.show_frame(self.home_frame)

    def get_solver_config(self):
        choice = self.method_var.get()

        if choice == "1":
            return False, False, False, "Basic Backtracking"
        elif choice == "2":
            return True, False, False, "Backtracking + MRV"
        elif choice == "3":
            return True, True, False, "Backtracking + MRV + LCV"
        else:
            return True, True, True, "Full Optimized Solver"

    def add_method_selector(self, parent):
        method_frame = tk.LabelFrame(parent, text="Select Solving Method", padx=10, pady=10)
        method_frame.pack(fill="x", pady=10)

        methods = [
            (
                "1. Basic Backtracking - tries values one by one and goes back when a conflict occurs",
                "1"
            ),
            (
                "2. Backtracking + MRV - chooses the variable with the fewest remaining options first",
                "2"
            ),
            (
                "3. Backtracking + MRV + LCV - chooses values that create the least future conflicts",
                "3"
            ),
            (
                "4. Full Optimized Solver - uses MRV, LCV, and Forward Checking for faster solving",
                "4"
            ),
        ]

        for text, value in methods:
            tk.Radiobutton(
                method_frame,
                text=text,
                variable=self.method_var,
                value=value,
                justify="left",
                anchor="w",
                wraplength=800
            ).pack(anchor="w", pady=4)

    def create_home_page(self):
        title = tk.Label(
            self.home_frame,
            text="Constraint Satisfaction Problem Solver",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            self.home_frame,
            text="Magic Square and University Exam Scheduling",
            font=("Arial", 12)
        )
        subtitle.pack(pady=5)

        desc = tk.Label(
            self.home_frame,
            text="Choose a problem below to explore AI-based constraint solving.",
            font=("Arial", 11)
        )
        desc.pack(pady=20)

        button_frame = tk.Frame(self.home_frame)
        button_frame.pack(pady=30)

        tk.Button(
            button_frame,
            text="Magic Square Solver",
            width=25,
            height=2,
            command=lambda: self.show_frame(self.magic_frame)
        ).pack(pady=10)

        tk.Button(
            button_frame,
            text="Exam Scheduling Solver",
            width=25,
            height=2,
            command=lambda: self.show_frame(self.exam_frame)
        ).pack(pady=10)

        tk.Button(
            button_frame,
            text="Exit",
            width=25,
            height=2,
            command=self.root.destroy
        ).pack(pady=10)

    def create_magic_page(self):
        title = tk.Label(
            self.magic_frame,
            text="Magic Square Solver",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        desc = tk.Label(
            self.magic_frame,
            text="Solve a 3x3 Magic Square or compare solving strategies for this problem.",
            font=("Arial", 11)
        )
        desc.pack(pady=5)

        self.add_method_selector(self.magic_frame)

        button_frame = tk.Frame(self.magic_frame)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Solve Magic Square",
            width=20,
            command=self.solve_magic_square
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            button_frame,
            text="Compare Solving Methods",
            width=20,
            command=self.compare_magic_square
        ).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            button_frame,
            text="Back to Home",
            width=20,
            command=self.go_home
        ).grid(row=0, column=2, padx=10, pady=5)

        output_frame = tk.LabelFrame(self.magic_frame, text="Output", padx=10, pady=10)
        output_frame.pack(fill="both", expand=True, pady=10)

        self.magic_output = tk.Text(output_frame, height=20, wrap="word", font=("Courier", 11))
        self.magic_output.pack(fill="both", expand=True)

    def create_exam_page(self):
        title = tk.Label(
            self.exam_frame,
            text="University Exam Scheduling Solver",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        desc = tk.Label(
            self.exam_frame,
            text="Sample inputs are preloaded below for quick testing.\nYou may edit them or enter your own custom exam schedule.",
            font=("Arial", 11, "bold"),
            justify="center"
        )
        desc.pack(pady=5)

        input_frame = tk.LabelFrame(self.exam_frame, text="Custom Exam Input", padx=10, pady=10)
        input_frame.pack(fill="x", pady=10)

        tk.Label(
            input_frame,
            text="Exams (comma-separated):"
        ).pack(anchor="w")

        self.exam_input = tk.Entry(input_frame, width=100)
        self.exam_input.pack(pady=3)
        self.exam_input.insert(0, "Math, Physics, Chemistry, Biology, History")

        tk.Label(
            input_frame,
            text="Conflicting Subjects (cannot share the same slot):"
        ).pack(anchor="w")

        tk.Label(
            input_frame,
            text="Example: Math-Physics, Chemistry-Biology",
            font=("Arial", 9)
    ).pack(anchor="w")

        self.conflict_input = tk.Entry(input_frame, width=100)
        self.conflict_input.pack(pady=3)
        self.conflict_input.insert(
            0,
            "Math-Physics, Math-Chemistry, Physics-Biology, Chemistry-Biology, Chemistry-History"
        )

        tk.Label(
            input_frame,
            text="Number of time slots:"
        ).pack(anchor="w")

        self.slot_input = tk.Entry(input_frame, width=20)
        self.slot_input.pack(anchor="w", pady=3)
        self.slot_input.insert(0, "3")


        tk.Label(
            input_frame,
            text="Maximum exams allowed per time slot:"
        ).pack(anchor="w", pady=(8, 0))

        self.max_exam_slot_input = tk.Entry(input_frame, width=20)
        self.max_exam_slot_input.pack(anchor="w", pady=3)
        self.max_exam_slot_input.insert(0, "2")


        tk.Label(
            input_frame,
            text="Unavailable Slots:"
        ).pack(anchor="w", pady=(8, 0))

        tk.Label(
            input_frame,
            text="Example: Math-1, Chemistry-3",
            font=("Arial", 9)
        ).pack(anchor="w")

        self.unavailable_input = tk.Entry(input_frame, width=20)
        self.unavailable_input.pack(anchor="w", pady=3)
        self.unavailable_input.insert(0, "")


        self.add_method_selector(self.exam_frame)

        button_frame = tk.Frame(self.exam_frame)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Solve Exam Scheduling",
            width=20,
            command=self.solve_exam_scheduling
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            button_frame,
            text="Compare Solving Methods",
            width=20,
            command=self.compare_exam_scheduling
        ).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            button_frame,
            text="Back to Home",
            width=20,
            command=self.go_home
        ).grid(row=0, column=2, padx=10, pady=5)

        output_frame = tk.LabelFrame(self.exam_frame, text="Output", padx=10, pady=10)
        output_frame.pack(fill="both", expand=True, pady=10)

        self.exam_output = tk.Text(output_frame, height=20, wrap="word", font=("Courier", 11))
        self.exam_output.pack(fill="both", expand=True)

    def format_magic_square(self, solution):
        if not solution:
            return "No solution found.\n"

        lines = []
        border = "+---+---+---+"
        lines.append(border)

        for r in range(3):
            row = []
            for c in range(3):
                row.append(f" {solution[(r, c)]} ")
            lines.append("|" + "|".join(row) + "|")
            lines.append(border)

        return "\n".join(lines)
    
    def solve_magic_square(self):
        self.magic_output.delete("1.0", tk.END)

        use_mrv, use_lcv, use_fc, method_name = self.get_solver_config()

        csp = create_magic_square_csp()
        solution, runtime, backtracks = solve(
            csp,
            use_mrv=use_mrv,
            use_lcv=use_lcv,
            use_forward_checking=use_fc
        )

        self.magic_output.insert(tk.END, "===== MAGIC SQUARE SOLUTION =====\n\n")
        self.magic_output.insert(tk.END, f"Method Used: {method_name}\n\n")
        self.magic_output.insert(tk.END, self.format_magic_square(solution))
        self.magic_output.insert(tk.END, f"\n\nRuntime: {runtime:.6f} sec\n")
        self.magic_output.insert(tk.END, f"Backtracks: {backtracks}\n")
        self.magic_output.insert(tk.END, "\nComplete.\n")

    def show_comparison_charts(self, problem_name, methods, runtimes, backtracks):
        short_names = ["Basic", "MRV", "MRV+LCV", "Full"]

        fig, axes = plt.subplots(2, 1, figsize=(8, 8))

        axes[0].bar(short_names, runtimes)
        axes[0].set_title(f"{problem_name} - Runtime Comparison")
        axes[0].set_xlabel("Solving Method")
        axes[0].set_ylabel("Runtime (seconds)")

        axes[1].bar(short_names, backtracks)
        axes[1].set_title(f"{problem_name} - Backtrack Comparison")
        axes[1].set_xlabel("Solving Method")
        axes[1].set_ylabel("Number of Backtracks")

        fig.suptitle(f"{problem_name} Strategy Comparison", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.show()

    def compare_magic_square(self):
        self.magic_output.delete("1.0", tk.END)

        configs = [
            ("Basic Backtracking", False, False, False),
            ("Backtracking + MRV", True, False, False),
            ("Backtracking + MRV + LCV", True, True, False),
            ("Full Optimized Solver", True, True, True),
        ]

        method_names = []
        runtimes = []
        backtrack_counts = []

        self.magic_output.insert(tk.END, "===== MAGIC SQUARE SOLVING METHODS COMPARISON =====\n\n")
        self.magic_output.insert(
            tk.END,
            "This compares different AI solving methods using runtime and backtrack count.\n\n"
        )

        best_solution = None

        for name, use_mrv, use_lcv, use_fc in configs:
            csp = create_magic_square_csp()
            solution, runtime, backtracks = solve(
                csp,
                use_mrv=use_mrv,
                use_lcv=use_lcv,
                use_forward_checking=use_fc
            )

            method_names.append(name)
            runtimes.append(runtime)
            backtrack_counts.append(backtracks)

            if solution and best_solution is None:
                best_solution = solution

            self.magic_output.insert(tk.END, f"{name}\n")
            self.magic_output.insert(tk.END, f"  Runtime: {runtime:.6f} sec\n")
            self.magic_output.insert(tk.END, f"  Backtracks: {backtracks}\n")
            self.magic_output.insert(tk.END, f"  Solved: {'Yes' if solution else 'No'}\n\n")

        if best_solution:
            self.magic_output.insert(tk.END, "Sample Magic Square Solution:\n\n")
            self.magic_output.insert(tk.END, self.format_magic_square(best_solution))
            self.magic_output.insert(tk.END, "\n\n")

        self.magic_output.insert(tk.END, "Charts opened in separate windows.\n")
        self.magic_output.insert(tk.END, "Complete.\n")

        self.show_comparison_charts(
            "Magic Square",
            method_names,
            runtimes,
            backtrack_counts
        )
 
    def get_exam_user_input(self):
        exams_text = self.exam_input.get().strip()
        conflicts_text = self.conflict_input.get().strip()
        slots_text = self.slot_input.get().strip()
        max_per_slot_text = self.max_exam_slot_input.get().strip()
        unavailable_text = self.unavailable_input.get().strip()

        exams = [exam.strip() for exam in exams_text.split(",") if exam.strip()]

        if not exams:
            messagebox.showerror(
                "Invalid Input",
                "Please enter at least one exam."
            )
            return None

        conflicts = []
        if conflicts_text:
            for pair in conflicts_text.split(","):
                if "-" in pair:
                    a, b = pair.split("-", 1)
                    conflicts.append((a.strip(), b.strip()))

        try:
            num_slots = int(slots_text)
            if num_slots <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Number of time slots must be a positive whole number."
            )
            return None

        try:
            max_exams_per_slot = int(max_per_slot_text)
            if max_exams_per_slot <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Maximum exams per time slot must be a positive whole number."
            )
            return None

        unavailable = {}

        if unavailable_text:
            for item in unavailable_text.split(","):
                if "-" in item:
                    exam, slot = item.split("-", 1)
                    exam = exam.strip()
                    slot = slot.strip()

                    if not slot.isdigit():
                        messagebox.showerror(
                            "Invalid Input",
                            "Unavailable slots must use numbers, for example: AI-1, Math-2."
                        )
                        return None

                    slot_name = f"Slot {slot}"

                    if exam not in unavailable:
                        unavailable[exam] = []

                    unavailable[exam].append(slot_name)

        return exams, conflicts, num_slots, max_exams_per_slot, unavailable

    def solve_exam_scheduling(self):
        self.exam_output.delete("1.0", tk.END)

        use_mrv, use_lcv, use_fc, method_name = self.get_solver_config()

        data = self.get_exam_user_input()
        if data is None:
            return

        exams, conflicts, num_slots, max_exams_per_slot, unavailable = data

        csp = create_exam_scheduling_csp(
            exams=exams,
            conflicts=conflicts,
            num_slots=num_slots,
            max_exams_per_slot=max_exams_per_slot,
            unavailable=unavailable
        )

        solution, runtime, backtracks = solve(
            csp,
            use_mrv=use_mrv,
            use_lcv=use_lcv,
            use_forward_checking=use_fc
        )

        self.exam_output.insert(tk.END, "===== EXAM SCHEDULING SOLUTION =====\n\n")
        self.exam_output.insert(tk.END, f"Method Used: {method_name}\n")
        self.exam_output.insert(tk.END, f"Number of Exams: {len(exams)}\n")
        self.exam_output.insert(tk.END, f"Number of Time Slots: {num_slots}\n")
        self.exam_output.insert(tk.END, f"Max Exams Per Slot: {max_exams_per_slot}\n\n")

        if solution:
            for exam in sorted(solution.keys()):
                self.exam_output.insert(tk.END, f"{exam} -> {solution[exam]}\n")
        else:
            self.exam_output.insert(tk.END, "No valid schedule found.\n")
            self.exam_output.insert(tk.END, "Try increasing the number of time slots.\n")

        self.exam_output.insert(tk.END, f"\nRuntime: {runtime:.6f} sec\n")
        self.exam_output.insert(tk.END, f"Backtracks: {backtracks}\n")
        self.exam_output.insert(tk.END, "\nComplete.\n")

    def compare_exam_scheduling(self):
        self.exam_output.delete("1.0", tk.END)

        data = self.get_exam_user_input()
        if data is None:
            return

        exams, conflicts, num_slots, max_exams_per_slot, unavailable = data

        configs = [
            ("Basic Backtracking", False, False, False),
            ("Backtracking + MRV", True, False, False),
            ("Backtracking + MRV + LCV", True, True, False),
            ("Full Optimized Solver", True, True, True),
        ]

        method_names = []
        runtimes = []
        backtrack_counts = []

        self.exam_output.insert(tk.END, "===== EXAM SCHEDULING SOLVING METHODS COMPARISON =====\n\n")
        self.exam_output.insert(
            tk.END,
            "This compares different AI solving methods using runtime and backtrack count.\n\n"
        )

        self.exam_output.insert(tk.END, f"Number of Exams: {len(exams)}\n")
        self.exam_output.insert(tk.END, f"Number of Time Slots: {num_slots}\n")
        self.exam_output.insert(tk.END, f"Max Exams Per Slot: {max_exams_per_slot}\n\n")

        for name, use_mrv, use_lcv, use_fc in configs:
            csp = create_exam_scheduling_csp(
                exams=exams,
                conflicts=conflicts,
                num_slots=num_slots,
                max_exams_per_slot=max_exams_per_slot,
                unavailable=unavailable
            )

            solution, runtime, backtracks = solve(
                csp,
                use_mrv=use_mrv,
                use_lcv=use_lcv,
                use_forward_checking=use_fc
            )

            method_names.append(name)
            runtimes.append(runtime)
            backtrack_counts.append(backtracks)

            self.exam_output.insert(tk.END, f"{name}\n")
            self.exam_output.insert(tk.END, f"  Runtime: {runtime:.6f} sec\n")
            self.exam_output.insert(tk.END, f"  Backtracks: {backtracks}\n")
            self.exam_output.insert(tk.END, f"  Solved: {'Yes' if solution else 'No'}\n\n")

        self.exam_output.insert(tk.END, "Charts opened in separate windows.\n")
        self.exam_output.insert(tk.END, "Complete.\n")

        self.show_comparison_charts(
            "Exam Scheduling",
            method_names,
            runtimes,
            backtrack_counts
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = CSPApp(root)
    root.mainloop()