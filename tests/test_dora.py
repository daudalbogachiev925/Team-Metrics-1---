from src.dora import (
    deployment_frequency, lead_time_for_changes, change_failure_rate,
    mttr, classify_dora, Deployment, Incident)
from datetime import datetime, timedelta

def test_deployment_frequency():
    now = datetime.utcnow().isoformat()
    deploys = [Deployment(f"d{i}", now, "prod", True) for i in range(10)]
    assert deployment_frequency(deploys, 30) > 0

def test_change_failure_rate():
    now = datetime.utcnow().isoformat()
    deploys = [Deployment("d1", now, "prod", True),
               Deployment("d2", now, "prod", False),
               Deployment("d3", now, "prod", True),
               Deployment("d4", now, "prod", True)]
    assert change_failure_rate(deploys) == 25.0

def test_mttr():
    t1 = datetime.utcnow()
    t2 = t1 + timedelta(hours=4)
    incidents = [Incident("i1", t1.isoformat(), t2.isoformat(), "major")]
    assert mttr(incidents) == 4.0
