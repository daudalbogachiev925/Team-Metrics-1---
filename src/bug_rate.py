from dataclasses import dataclass, field

@dataclass
class Bug:
    id: str
    created_at: str
    resolved_at: str = ""
    severity: str = "minor"
    reopened: bool = False
    module: str = ""

def bug_rate(bugs, sprints_count):
    if sprints_count == 0:
        return 0
    return round(len(bugs) / sprints_count, 2)

def reopened_ratio(bugs):
    if not bugs:
        return 0
    return round(sum(1 for b in bugs if b.reopened) / len(bugs) * 100, 1)

def bug_by_severity(bugs):
    result = {}
    for b in bugs:
        result[b.severity] = result.get(b.severity, 0) + 1
    return result

def bug_by_module(bugs):
    result = {}
    for b in bugs:
        result[b.module] = result.get(b.module, 0) + 1
    return dict(sorted(result.items(), key=lambda x: -x[1]))

def escape_rate(bugs_found_prod, bugs_found_test):
    total = bugs_found_prod + bugs_found_test
    if total == 0:
        return 0
    return round(bugs_found_prod / total * 100, 1)
