from solver import solve
from magic_square import create_magic_square_csp
from exam_scheduling import create_exam_scheduling_csp

# Compare different solving methods for exam scheduling
def compare_exam_scheduling():
    print("\n===== EXAM SCHEDULING EXPERIMENTS =====")

    configs = [
        ("Basic Backtracking", False, False, False),
        ("Backtracking + MRV", True, False, False),
        ("Backtracking + MRV + LCV", True, True, False),
        ("Backtracking + MRV + LCV + Forward Checking", True, True, True),
    ]

    for name, use_mrv, use_lcv, use_fc in configs:
        csp = create_magic_square_csp()
        solution, runtime, backtracks = solve(
            csp,
            use_mrv=use_mrv,
            use_lcv=use_lcv,
            use_forward_checking=use_fc
        )

        print(f"\n{name}")
        print(f"Runtime: {runtime:.6f} sec")
        print(f"Backtracks: {backtracks}")
        print(f"Solved: {'Yes' if solution else 'No'}")

# Compare different solving methods for exam scheduling
def compare_exam_scheduling():
    print("\n===== EXAM SCHEDULING EXPERIMENTS =====")

    configs = [
        ("Basic Backtracking", False, False, False),
        ("Backtracking + MRV", True, False, False),
        ("Backtracking + MRV + LCV", True, True, False),
        ("Backtracking + MRV + LCV + Forward Checking", True, True, True),
    ]

    for name, use_mrv, use_lcv, use_fc in configs:
        csp = create_exam_scheduling_csp()
        solution, runtime, backtracks = solve(
            csp,
            use_mrv=use_mrv,
            use_lcv=use_lcv,
            use_forward_checking=use_fc
        )

        print(f"\n{name}")
        print(f"Runtime: {runtime:.6f} sec")
        print(f"Backtracks: {backtracks}")
        print(f"Solved: {'Yes' if solution else 'No'}")