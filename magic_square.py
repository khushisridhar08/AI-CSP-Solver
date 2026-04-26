from csp import CSP


def create_magic_square_csp(fixed_values=None):
    n = 3
    magic_sum = 15

    if fixed_values is None:
        fixed_values = {}

    variables = []
    domains = {}
    neighbors = {}

    for r in range(n):
        for c in range(n):
            cell = (r, c)
            variables.append(cell)

            if cell in fixed_values:
                domains[cell] = [fixed_values[cell]]
            else:
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
        return val1 != val2

    csp = CSP(variables, domains, neighbors, constraint)
    csp.n = n
    csp.magic_sum = magic_sum
    csp.extra_constraint = is_magic_square_consistent

    return csp


def is_magic_square_consistent(var, value, assignment, csp):
    temp_assignment = assignment.copy()
    temp_assignment[var] = value

    assigned_values = list(temp_assignment.values())

    if len(assigned_values) != len(set(assigned_values)):
        return False

    n = csp.n
    target = csp.magic_sum

    for r in range(n):
        row = [(r, c) for c in range(n)]
        values = [temp_assignment[cell] for cell in row if cell in temp_assignment]

        if len(values) == n and sum(values) != target:
            return False
        if len(values) < n and sum(values) >= target:
            return False

    for c in range(n):
        col = [(r, c) for r in range(n)]
        values = [temp_assignment[cell] for cell in col if cell in temp_assignment]

        if len(values) == n and sum(values) != target:
            return False
        if len(values) < n and sum(values) >= target:
            return False

    diag1 = [(i, i) for i in range(n)]
    values = [temp_assignment[cell] for cell in diag1 if cell in temp_assignment]

    if len(values) == n and sum(values) != target:
        return False
    if len(values) < n and sum(values) >= target:
        return False

    diag2 = [(i, n - 1 - i) for i in range(n)]
    values = [temp_assignment[cell] for cell in diag2 if cell in temp_assignment]

    if len(values) == n and sum(values) != target:
        return False
    if len(values) < n and sum(values) >= target:
        return False

    return True