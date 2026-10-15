from datetime import datetime, timedelta
from dataclasses import dataclass, field

@dataclass
class Deployment:
    id: str
    timestamp: str
    env: str
    success: bool
    lead_time_hours: float = 0.0
    changed_lines: int = 0

@dataclass
class Incident:
    id: str
    detected_at: str
    resolved_at: str
    severity: str

def deployment_frequency(deployments, days=30):
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    recent = [d for d in deployments if d.timestamp >= cutoff and d.success]
    return round(len(recent) / days, 2)

def lead_time_for_changes(deployments):
    successful = [d for d in deployments if d.success]
    if not successful:
        return 0
    return round(sum(d.lead_time_hours for d in successful) / len(successful), 2)

def change_failure_rate(deployments):
    total = len(deployments)
    if total == 0:
        return 0
    failed = sum(1 for d in deployments if not d.success)
    return round(failed / total * 100, 2)

def mttr(incidents):
    if not incidents:
        return 0
    durations = []
    for i in incidents:
        d1 = datetime.fromisoformat(i.detected_at)
        d2 = datetime.fromisoformat(i.resolved_at)
        durations.append((d2 - d1).total_seconds() / 3600)
    return round(sum(durations) / len(durations), 2)

def dora_score(deployments, incidents, days=30):
    return {
        "deployment_frequency_per_day": deployment_frequency(deployments, days),
        "lead_time_hours": lead_time_for_changes(deployments),
        "change_failure_rate_pct": change_failure_rate(deployments),
        "mttr_hours": mttr(incidents),
    }

def classify_dora(metrics):
    df = metrics["deployment_frequency_per_day"]
    lt = metrics["lead_time_hours"]
    cfr = metrics["change_failure_rate_pct"]
    mttr_h = metrics["mttr_hours"]

    def freq_level(v):
        if v >= 1: return "elite"
        if v >= 0.14: return "high"
        if v >= 0.03: return "medium"
        return "low"

    def lt_level(v):
        if v < 1: return "elite"
        if v < 24: return "high"
        if v < 168: return "medium"
        return "low"

    def cfr_level(v):
        if v < 5: return "elite"
        if v < 10: return "high"
        if v < 15: return "medium"
        return "low"

    def mttr_level(v):
        if v < 1: return "elite"
        if v < 24: return "high"
        if v < 168: return "medium"
        return "low"

    return {
        "deployment_frequency": freq_level(df),
        "lead_time": lt_level(lt),
        "change_failure_rate": cfr_level(cfr),
        "mttr": mttr_level(mttr_h),
    }
