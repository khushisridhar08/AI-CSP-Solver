from csp import CSP


def create_magic_square_csp():
    # 3x3 magic square
    n = 3
    magic_sum = 15

    variables = []
    domains = {}
    neighbors = {}

    for r in range(n):
        for c in range(n):
            cell = (r, c)
            variables.append(cell)
            domains[cell] = list(range(1, 10))

    for r in range(n):
        for c in range(n):
            cell = (r, c)
            neighbor_set = set()

            for i in range(n):
                for j in range(n):
                    if (i, j) != cell:
                        neighbor_set.add((i, j))

            neighbors[cell] = list(neighbor_set)

    def constraint(var1, val1, var2, val2):
        # all cells must have unique values
        return val1 != val2

    csp = CSP(variables, domains, neighbors, constraint)
    csp.n = n
    csp.magic_sum = magic_sum
    csp.extra_constraint = is_magic_square_consistent
    return csp


def is_magic_square_consistent(var, value, assignment, csp):
    temp_assignment = assignment.copy()
    temp_assignment[var] = value

    # uniqueness
    assigned_values = list(temp_assignment.values())
    if len(assigned_values) != len(set(assigned_values)):
        return False

    n = csp.n
    target = csp.magic_sum

    # Check rows
    for r in range(n):
        row_cells = [(r, c) for c in range(n)]
        row_values = [temp_assignment[cell] for cell in row_cells if cell in temp_assignment]

        if len(row_values) == n:
            if sum(row_values) != target:
                return False
        elif sum(row_values) >= target:
            return False

    # Check columns
    for c in range(n):
        col_cells = [(r, c) for r in range(n)]
        col_values = [temp_assignment[cell] for cell in col_cells if cell in temp_assignment]

        if len(col_values) == n:
            if sum(col_values) != target:
                return False
        elif sum(col_values) >= target:
            return False

    # Main diagonal
    diag1_cells = [(i, i) for i in range(n)]
    diag1_values = [temp_assignment[cell] for cell in diag1_cells if cell in temp_assignment]
    if len(diag1_values) == n:
        if sum(diag1_values) != target:
            return False
    elif sum(diag1_values) >= target:
        return False

    # Other diagonal
    diag2_cells = [(i, n - 1 - i) for i in range(n)]
    diag2_values = [temp_assignment[cell] for cell in diag2_cells if cell in temp_assignment]
    if len(diag2_values) == n:
        if sum(diag2_values) != target:
            return False
    elif sum(diag2_values) >= target:
        return False

    return True


def print_magic_square(solution):
    if solution is None:
        print("No magic square solution found.")
        return

    print("\nMagic Square Solution:")
    for r in range(3):
        row = []
        for c in range(3):
            row.append(str(solution[(r, c)]))
        print(" ".join(row))