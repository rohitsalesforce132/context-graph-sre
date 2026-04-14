# Context Graph Schema

## Node Types

### 1. Incident Event (`incidents/`)
The core node — a moment where something happened that required a decision.

```yaml
id: INC-001
type: incident_event
title: "Production Node NotReady - API pods failing"
timestamp: "2026-04-12T14:23:00+05:30"
severity: P1
status: resolved

symptom: "3 nodes in production cluster transitioned to NotReady state"
affected_services:
  - payment-api
  - user-service
  - notification-service
blast_radius: "All APIs in production region"

conditions:
  time_of_day: "14:23 (peak traffic)"
  active_incidents: 0
  change_freeze: false
  on_call: "engineer-a"
  recent_deploys: "payment-api v2.3.1 deployed 2h prior"
  cluster_load: "78% CPU, 65% memory"

actors:
  - role: on_call
    person: engineer-a

ttk_minutes: 23  # time to know
ttm_minutes: 12  # time to mitigate
ttr_minutes: 35  # time to resolve

decision_refs: [DEC-001]
entity_refs: [ENT-prod-cluster]
similar_incident_refs: []

root_cause: "Container runtime disk pressure — images accumulated over 90+ days"
root_cause_category: resource_exhaustion

follow_up:
  - "Update runbook: check disk pressure before runtime restart"
  - "Add cron: image prune weekly"

tags: [kubernetes, node-notready, disk-pressure, production, p1]
```

### 2. Decision Trace (`decisions/`)
The reasoning chain behind a specific action. This is the **core innovation**.

```yaml
id: DEC-001
type: decision_trace
title: "Skipped container runtime restart, went straight to disk cleanup"
timestamp: "2026-04-12T14:28:00+05:30"
incident_ref: INC-001

decision: "Skip runbook step 2 (runtime restart), go to step 4 (disk cleanup)"
rationale: "Runtime restart caused 15-min outage in INC-004 (Mar 2026)"

options_considered:
  - option: "Follow runbook: restart runtime first"
    rejected_because: "Precedent INC-004 showed this causes extended outage"
  - option: "Disk cleanup first, then runtime restart if needed"
    chosen: true
    confidence: high

exceptions:
  - rule: "SRE runbook step 2: restart container runtime on NotReady"
    deviation: "Skipped step 2"
    justification: "Historical data shows restart on disk-pressure nodes causes cascading pod evictions"
    approved_by: "on-call judgment"

precedents:
  - ref: DEC-004
    similarity: "Same root cause (disk pressure), same skip rationale"

organizational_state:
  other_p1s: 0
  team_availability: "Full team online"
  customer_impact: "API latency > 500ms"
  sla_breach_risk: "High"

outcome:
  result: "Resolved in 12 minutes (vs 35 min avg for similar incidents)"
  mttr_improvement: "66% faster than standard runbook"
  side_effects: "None"
  follow_up: "Update runbook to check disk pressure before runtime restart"

actor:
  name: engineer-a
  role: on_call
  experience_level: "Experienced with Kubernetes node issues"

ai_reproducible: true
ai_reproducible_notes: |
  An AI agent with access to DEC-004 (runtime restart failed) would have
  sufficient precedent to make this same decision.

tags: [kubernetes, disk-pressure, runbook-exception, fast-resolution, precedent-setting]
```

### 3. Precedent Chain (`precedents/`)
Links decisions across time, showing how patterns evolved.

```yaml
id: PRE-001
type: precedent_chain
title: "Node Disk Pressure Response Pattern"

pattern: "When nodes show NotReady + disk pressure, clean disk first, skip runtime restart"

evolution:
  - date: "2026-01-15"
    incident: INC-002
    decision: DEC-002
    action: "Followed runbook exactly (runtime restart first)"
    outcome: "15 min outage, pods evicted, extended recovery"
    lesson: "Runtime restart on disk-pressure nodes is dangerous"

  - date: "2026-04-12"
    incident: INC-001
    decision: DEC-001
    action: "Skipped runtime entirely, disk cleanup only"
    outcome: "Resolved in 12 min, zero outage"
    lesson: "This is now the standard approach"

recommendation: |
  For node NotReady + disk pressure:
  1. Check disk usage
  2. Clean container images
  3. Clean logs
  4. Wait 2 min, check node status
  5. Only restart runtime if still NotReady after cleanup

confidence: high
based_on_incidents: 3
success_rate: "100% (3/3)"
```

### 4. Entity (`entities/`)
Systems, services, people — the structural layer.

```yaml
id: ENT-prod-cluster
type: system
name: "prod-cluster"
category: kubernetes_cluster
environment: production
region: primary-region

node_pools:
  - name: system
    count: 3
  - name: workloads
    count: 5

depends_on:
  - ENT-container-registry
  - ENT-key-vault

depended_upon_by:
  - ENT-payment-api
  - ENT-user-service

incident_history: [INC-001, INC-002]
```

### 5. Behavioral Pattern (`patterns/`)
Aggregated patterns recognized across many decisions.

```yaml
id: PAT-001
type: behavioral_pattern
title: "On-Call Engineer Skips Runbook Steps Under Pressure"

pattern: |
  When MTTR pressure is high, on-call engineers skip runbook steps
  they've personally found ineffective in past incidents.

evidence:
  - decision: DEC-001
    note: "Skipped runtime restart based on personal experience"

implications:
  - "Runbooks are not reflecting operational reality"
  - "AI agents following runbooks literally will make worse decisions"

recommendation: |
  1. Audit all runbooks against actual decision traces
  2. Add "skip conditions" to each runbook step
  3. Feed context graph to AI agents as primary decision input
```

---

## Edge Types

| Edge | From → To | Meaning |
|------|-----------|---------|
| `solved_by` | Incident → Decision | Resolved by this decision |
| `sets_precedent` | Decision → Decision | Creates pattern for future |
| `references` | Decision → Precedent | Explicitly cited precedent |
| `similar_to` | Incident → Incident | Share root cause or pattern |
| `affects` | Incident → Entity | Incident impacted this system |
| `depends_on` | Entity → Entity | System dependency |
| `operated_by` | Decision → Entity (person) | Who made this decision |
| `deviates_from` | Decision → Entity (runbook) | Broke from standard procedure |
| `triggers` | Incident → Incident | One incident caused another |
| `pattern_instance` | Decision → Pattern | Instance of a recognized pattern |

---

## Query Templates

### 1. Precedent Search
```
INPUT: "node NotReady disk pressure"
FIND:  All decisions involving similar symptoms
SHOW:  What was tried, what worked, what precedent was set
```

### 2. Exception Audit
```
INPUT: "Last 30 days"
FIND:  All decisions where exceptions were made
SHOW:  What rules were bent, who approved, what justification
```

### 3. Blast Radius
```
INPUT: "payment-api"
FIND:  All entities that depend on this service
SHOW:  Historical incidents, precedents, and patterns
```

### 4. Decision Quality
```
INPUT: "engineer name"
FIND:  All decisions made by this actor
SHOW:  Success rate, average MTTR, common patterns
```

### 5. Runbook Gaps
```
INPUT: "node notready runbook"
FIND:  Decisions that deviated from this runbook
SHOW:  What was skipped, why, whether it should be updated
```
