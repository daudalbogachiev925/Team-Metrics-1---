from dataclasses import dataclass

@dataclass
class Commit:
    hash: str
    author: str
    date: str
    files_changed: int
    additions: int
    deletions: int
    module_type: str

def churn_rate(commits):
    if not commits:
        return 0
    total_add = sum(c.additions for c in commits)
    total_del = sum(c.deletions for c in commits)
    return round(total_del / max(total_add, 1) * 100, 1)

def reverted_changes_ratio(commits, reverts):
    if not commits:
        return 0
    return round(len(reverts) / len(commits) * 100, 1)

def author_churn(commits):
    by_author = {}
    for c in commits:
        if c.author not in by_author:
            by_author[c.author] = {"additions": 0, "deletions": 0, "commits": 0}
        by_author[c.author]["additions"] += c.additions
        by_author[c.author]["deletions"] += c.deletions
        by_author[c.author]["commits"] += 1
    for a, data in by_author.items():
        data["churn_pct"] = round(
            data["deletions"] / max(data["additions"], 1) * 100, 1)
    return by_author

def hotspot_analysis(commits, top_n=10):
    by_file = {}
    for c in commits:
        key = c.module_type
        by_file.setdefault(key, {"additions": 0, "deletions": 0, "changes": 0})
        by_file[key]["additions"] += c.additions
        by_file[key]["deletions"] += c.deletions
        by_file[key]["changes"] += 1
    sorted_items = sorted(by_file.items(),
                          key=lambda x: x[1]["changes"], reverse=True)
    return [{"module": k, **v} for k, v in sorted_items[:top_n]]
