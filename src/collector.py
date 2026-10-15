import random
from datetime import datetime, timedelta
from src.dora import Deployment, Incident
from src.velocity import Sprint
from src.code_churn import Commit
from src.bug_rate import Bug
from src.load import Task

def generate_dora_data(n_days=30, seed=42):
    random.seed(seed)
    deployments = []
    incidents = []
    now = datetime.utcnow()
    for i in range(n_days):
        for _ in range(random.randint(1, 5)):
            ts = now - timedelta(days=i, hours=random.randint(0, 23))
            deployments.append(Deployment(
                id=f"d{i}_{_}",
                timestamp=ts.isoformat(),
                env=random.choice(["dev", "test", "prod"]),
                success=random.random() > 0.08,
                lead_time_hours=random.uniform(0.5, 48),
                changed_lines=random.randint(50, 2000)))
    for i in range(random.randint(3, 10)):
        detected = now - timedelta(days=random.randint(0, 30))
        resolved = detected + timedelta(hours=random.uniform(1, 48))
        incidents.append(Incident(
            id=f"inc{i}", detected_at=detected.isoformat(),
            resolved_at=resolved.isoformat(),
            severity=random.choice(["minor", "major", "critical"])))
    return deployments, incidents

def generate_sprints(n=6, seed=42):
    random.seed(seed)
    sprints = []
    for i in range(n):
        planned = random.randint(40, 80)
        completed = int(planned * random.uniform(0.7, 1.1))
        sprints.append(Sprint(
            id=f"S{i+1}",
            planned_points=planned,
            completed_points=completed,
            start=f"2025-0{(i%9)+1}-01",
            end=f"2025-0{(i%9)+1}-14"))
    return sprints

def generate_commits(n=500, authors=6, seed=42):
    random.seed(seed)
    authors_list = [f"dev{i+1}" for i in range(authors)]
    modules = ["справочники", "документы", "отчёты", "обработки", "общие_модули", "формы"]
    commits = []
    for i in range(n):
        add = random.randint(5, 300)
        commits.append(Commit(
            hash=f"abc{i:04d}",
            author=random.choice(authors_list),
            date=(datetime.utcnow() - timedelta(days=random.randint(0, 90))).isoformat(),
            files_changed=random.randint(1, 10),
            additions=add,
            deletions=random.randint(0, int(add * 0.5)),
            module_type=random.choice(modules)))
    return commits

def generate_bugs(n=80, seed=42):
    random.seed(seed)
    modules = ["продажи", "склад", "финансы", "интеграция", "отчёты"]
    bugs = []
    for i in range(n):
        created = datetime.utcnow() - timedelta(days=random.randint(0, 90))
        resolved = created + timedelta(days=random.randint(1, 14))
        bugs.append(Bug(
            id=f"BUG-{i+1}",
            created_at=created.isoformat(),
            resolved_at=resolved.isoformat(),
            severity=random.choice(["minor", "major", "critical"]),
            reopened=random.random() < 0.12,
            module=random.choice(modules)))
    return bugs

def generate_tasks(n=200, devs=6, sprints=6, seed=42):
    random.seed(seed)
    dev_list = [f"dev{i+1}" for i in range(devs)]
    tasks = []
    for i in range(n):
        est = random.uniform(2, 40)
        tasks.append(Task(
            id=f"TASK-{i+1}",
            assignee=random.choice(dev_list),
            type=random.choice(["feature", "bugfix", "refactor", "docs"]),
            estimate_hours=round(est, 1),
            actual_hours=round(est * random.uniform(0.5, 1.8), 1),
            sprint=f"S{random.randint(1, sprints)}",
            status=random.choice(["done", "in_progress", "todo"])))
    return tasks
