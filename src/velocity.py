from dataclasses import dataclass, field

@dataclass
class Sprint:
    id: str
    planned_points: int
    completed_points: int
    start: str
    end: str

def velocity(sprints):
    if not sprints:
        return 0
    return round(sum(s.completed_points for s in sprints) / len(sprints), 1)

def velocity_trend(sprints):
    if len(sprints) < 2:
        return 0
    first = sprints[0].completed_points
    last = sprints[-1].completed_points
    return round((last - first) / max(first, 1) * 100, 1)

def predictability(sprints):
    if not sprints:
        return 0
    ratios = [min(s.completed_points / s.planned_points, 1.0)
              for s in sprints if s.planned_points > 0]
    return round(sum(ratios) / len(ratios) * 100, 1)

def committed_vs_done(sprints):
    return [{
        "sprint": s.id,
        "planned": s.planned_points,
        "done": s.completed_points,
        "ratio": round(s.completed_points / max(s.planned_points, 1) * 100, 1),
    } for s in sprints]
