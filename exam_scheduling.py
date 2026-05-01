from csp import CSP

# Create the exam scheduling CSP
def create_exam_scheduling_csp(
    exams,
    conflicts,
    num_slots,
    max_exams_per_slot=2,
    unavailable=None
):
    if unavailable is None:
        unavailable = {}

    variables = exams

    domains = {}

    for exam in exams:
        all_slots = [f"Slot {i+1}" for i in range(num_slots)]

        blocked = unavailable.get(exam, [])

        domains[exam] = [slot for slot in all_slots if slot not in blocked]

    neighbors = {exam: [] for exam in exams}

    for a, b in conflicts:
        if a in exams and b in exams:
            neighbors[a].append(b)
            neighbors[b].append(a)

    def constraint(var1, val1, var2, val2):
        return val1 != val2

    csp = CSP(variables, domains, neighbors, constraint)
    csp.max_exams_per_slot = max_exams_per_slot
    csp.extra_constraint = slot_limit_constraint

    return csp

# Slot limit constraint
def slot_limit_constraint(var, value, assignment, csp):
    temp = assignment.copy()
    temp[var] = value

    count = {}

    for _, slot in temp.items():
        count[slot] = count.get(slot, 0) + 1

        if count[slot] > csp.max_exams_per_slot:
            return False

    return True