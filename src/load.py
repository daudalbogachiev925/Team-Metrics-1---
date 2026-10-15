from dataclasses import dataclass

@dataclass
class Task:
    id: str
    assignee: str
    type: str
    estimate_hours: float
    actual_hours: float
    sprint: str
    status: str

def load_per_developer(tasks, sprint=None):
    filtered = tasks if not sprint else [t for t in tasks if t.sprint == sprint]
    result = {}
    for t in filtered:
        result.setdefault(t.assignee, {"tasks": 0, "estimate": 0, "actual": 0})
        result[t.assignee]["tasks"] += 1
        result[t.assignee]["estimate"] += t.estimate_hours
        result[t.assignee]["actual"] += t.actual_hours
    for a, data in result.items():
        data["accuracy"] = round(data["estimate"] / max(data["actual"], 1) * 100, 1)
    return result

def unbalanced_load(load_data, threshold=0.4):
    if not load_data:
        return []
    values = [d["actual"] for d in load_data.values()]
    avg = sum(values) / len(values)
    unbalanced = []
    for author, data in load_data.items():
        deviation = abs(data["actual"] - avg) / avg if avg else 0
        if deviation > threshold:
            unbalanced.append({
                "developer": author,
                "hours": data["actual"],
                "deviation_pct": round(deviation * 100, 1),
                "direction": "overload" if data["actual"] > avg else "underload",
            })
    return unbalanced

def estimation_accuracy(tasks):
    if not tasks:
        return 0
    ratios = [min(t.estimate_hours / max(t.actual_hours, 0.1), 2.0)
              for t in tasks]
    return round(sum(ratios) / len(ratios) * 100, 1)
