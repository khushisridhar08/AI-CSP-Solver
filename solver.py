import time
import copy


def is_consistent(var, value, assignment, csp):
    for neighbor in csp.neighbors[var]:
        if neighbor in assignment:
            if not csp.constraint(var, value, neighbor, assignment[neighbor]):
                return False

    if hasattr(csp, "extra_constraint"):
        if not csp.extra_constraint(var, value, assignment, csp):
            return False

    return True


def get_legal_values(var, assignment, domains, csp):
    legal = []
    for value in domains[var]:
        if is_consistent(var, value, assignment, csp):
            legal.append(value)
    return legal


def select_unassigned_variable(assignment, domains, csp, use_mrv=True):
    unassigned = [v for v in csp.variables if v not in assignment]

    if not use_mrv:
        return unassigned[0]

    return min(unassigned, key=lambda var: len(get_legal_values(var, assignment, domains, csp)))


def order_domain_values(var, assignment, domains, csp, use_lcv=True):
    values = domains[var][:]

    if not use_lcv:
        return values

    def conflicts(value):
        count = 0
        for neighbor in csp.neighbors[var]:
            if neighbor not in assignment:
                for neighbor_value in domains[neighbor]:
                    if not csp.constraint(var, value, neighbor, neighbor_value):
                        count += 1
        return count

    return sorted(values, key=conflicts)


def forward_check(var, value, domains, assignment, csp):
    new_domains = copy.deepcopy(domains)

    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment:
            new_domains[neighbor] = [
                v for v in new_domains[neighbor]
                if csp.constraint(var, value, neighbor, v)
            ]

            if len(new_domains[neighbor]) == 0:
                return None

    return new_domains


def backtrack(assignment, domains, csp, use_mrv=True, use_lcv=True, use_forward_checking=True):
    if len(assignment) == len(csp.variables):
        return assignment

    var = select_unassigned_variable(assignment, domains, csp, use_mrv)

    for value in order_domain_values(var, assignment, domains, csp, use_lcv):
        if is_consistent(var, value, assignment, csp):
            assignment[var] = value

            if use_forward_checking:
                new_domains = forward_check(var, value, domains, assignment, csp)
            else:
                new_domains = copy.deepcopy(domains)

            if new_domains is not None:
                result = backtrack(
                    assignment,
                    new_domains,
                    csp,
                    use_mrv=use_mrv,
                    use_lcv=use_lcv,
                    use_forward_checking=use_forward_checking
                )
                if result is not None:
                    return result

            del assignment[var]

    csp.backtrack_count += 1
    return None


def solve(csp, use_mrv=True, use_lcv=True, use_forward_checking=True):
    csp.backtrack_count = 0
    start = time.time()

    result = backtrack(
        assignment={},
        domains=copy.deepcopy(csp.domains),
        csp=csp,
        use_mrv=use_mrv,
        use_lcv=use_lcv,
        use_forward_checking=use_forward_checking
    )

    end = time.time()
    runtime = end - start

    return result, runtime, csp.backtrack_count