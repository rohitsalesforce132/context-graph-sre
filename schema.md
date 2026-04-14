# Context Graph Schema

## Node Types

### 1. Incident Event (`incidents/`)
The core node — a moment where something happened that required a decision.

```yaml
id: INC-001
type: incident_event
title: "AKS PROD Node NotReady - camara-qod pods failing"
timestamp: "2026-04-12T14:23:00+05:30"
severity: P1
status: resolved

# What happened
symptom: "3 nodes in aks-prod-01 transitioned to NotReady state"
affected_services:
  - camara-qod-api
  - camara-nef-session
  - camara-turbo-live
blast_radius: "All CAMARA APIs in PROD region eastus2"

# Conditions at the time
conditions:
  time_of_day: "14:23 IST (peak traffic)"
  active_incidents: 0
  change_freeze: false
  on_call: "Rohit"
  recent_deploys: "camara-qod v2.3.1 deployed 2h prior"
  cluster_load: "78% CPU, 65% memory"

# Who was involved
actors:
  - role: on_call
    person: Rohit
  - role: escalation
    person: none_needed

# How long
ttk_minutes: 23  # time to know (detection)
ttm_minutes: 12  # time to mitigate
ttr_minutes: 35  # time to resolve

# Tags for graph traversal
tags: [aks, node-notready, camara, prod, disk-pressure, p1]
```

### 2. Decision Trace (`decisions/`)
The reasoning chain behind a specific action. This is the **core innovation**.

```yaml
id: DEC-001
type: decision_trace
title: "Skipped kubelet restart, went straight to disk cleanup"
timestamp: "2026-04-12T14:28:00+05:30"
incident_ref: INC-001

# The decision
decision: "Skip runbook step 2 (kubelet restart), go to step 4 (disk cleanup)"
rationale: "Kubelet restart caused 15-min outage in INC-004 (Mar 2026)"

# What was considered
options_considered:
  - option: "Follow runbook: restart kubelet first"
    rejected_because: "Precedent INC-004 showed this causes extended outage"
  - option: "Disk cleanup first, then kubelet restart if needed"
    chosen: true
    confidence: high

# Exceptions made
exceptions:
  - rule: "SRE runbook step 2: restart kubelet on NotReady"
    deviation: "Skipped step 2"
    justification: "Historical data shows kubelet restart on disk-pressure nodes causes cascading pod evictions"
    approved_by: "Rohit (on-call judgment)"

# Precedent chain
precedents:
  - ref: DEC-004
    similarity: "Same root cause (disk pressure), same skip rationale"
  - ref: DEC-007
    similarity: "Disk cleanup resolved without kubelet restart"

# What was the organizational state
organizational_state:
  other_p1s: 0
  team_availability: "Full team online (afternoon)"
  customer_impact: "CAMARA API latency > 500ms for 3 carriers"
  sla_breach_risk: "High if not resolved in 30 min"

# Outcome
outcome:
  result: "Resolved in 12 minutes (vs 35 min avg for similar incidents)"
  mttr_improvement: "66% faster than standard runbook"
  side_effects: "None"
  follow_up: "Update runbook to check disk pressure before kubelet restart"

# Tags
tags: [aks, disk-pressure, runbook-exception, fast-resolution, precedent-setting]
```

### 3. Precedent Chain (`precedents/`)
Links decisions across time, showing how patterns evolved.

```yaml
id: PRE-001
type: precedent_chain
title: "AKS Disk Pressure Response Pattern"

# The pattern
pattern: "When AKS nodes show NotReady + disk pressure, clean disk first, skip kubelet restart"

# Evolution over time
evolution:
  - date: "2026-01-15"
    incident: INC-002
    decision: DEC-002
    action: "Followed runbook exactly (kubelet restart first)"
    outcome: "15 min outage, pods evicted, extended recovery"
    lesson: "Kubelet restart on disk-pressure nodes is dangerous"

  - date: "2026-03-08"
    incident: INC-004
    decision: DEC-004
    action: "Tried partial skip — cleaned disk, then restarted kubelet"
    outcome: "8 min outage, but kubelet restart unnecessary"
    lesson: "Disk cleanup alone is sufficient in most cases"

  - date: "2026-04-12"
    incident: INC-001
    decision: DEC-001
    action: "Skipped kubelet entirely, disk cleanup only"
    outcome: "Resolved in 12 min, zero outage"
    lesson: "This is now the standard approach for disk-pressure NotReady"

# Current recommendation
recommendation: |
  For AKS node NotReady + disk pressure:
  1. Check disk usage: df -h /var/lib/kubelet
  2. Clean docker images: docker image prune -a --filter "until=48h"
  3. Clean logs: journalctl --vacuum-time=2d
  4. Wait 2 min, check node status
  5. Only restart kubelet if still NotReady after cleanup
  6. DO NOT restart kubelet as first step

# Confidence
confidence: high
based_on_incidents: 3
success_rate: "100% (3/3)"

tags: [aks, disk-pressure, runbook-override, pattern]
```

### 4. Entity (`entities/`)
Systems, services, people — the structural layer.

```yaml
# entities/systems/aks-prod-01.md
id: ENT-aks-prod-01
type: system
name: "aks-prod-01"
category: kubernetes_cluster
environment: production
region: eastus2
node_pools:
  - name: system
    count: 3
    vm_size: Standard_D4s_v3
  - name: camara
    count: 5
    vm_size: Standard_D8s_v3

# What depends on this
depends_on:
  - ENT-azure-eastus2
  - ENT-acr-att

# What depends on this
depended_upon_by:
  - ENT-camara-qod-api
  - ENT-camara-nef-session
  - ENT-camara-turbo-live

# Incident history (links to context graph)
incident_history:
  - INC-001
  - INC-002
  - INC-004
```

### 5. Behavioral Pattern (`patterns/`)
Aggregated patterns recognized across many decisions.

```yaml
id: PAT-001
type: behavioral_pattern
title: "On-Call Engineer Skips Runbook Steps Under Pressure"

# The pattern
pattern: |
  When MTTR pressure is high (>15 min elapsed), on-call engineers 
  tend to skip runbook steps they've personally found ineffective 
  in past incidents, even if the runbook doesn't explicitly allow it.

# Evidence
evidence:
  - decision: DEC-001
    note: "Skipped kubelet restart based on personal experience"
  - decision: DEC-004
    note: "Partial skip after learning from DEC-002"
  - decision: DEC-008
    note: "Skipped pipeline rollback, did manual fix"

# Implications
implications:
  - "Runbooks are not reflecting operational reality"
  - "Team has implicit knowledge not captured anywhere"
  - "New team members won't know which steps to skip"
  - "Agent without this context would follow runbook literally"

# Recommendation
recommendation: |
  1. Audit all runbooks against actual incident decisions
  2. Add "skip conditions" to each runbook step
  3. Create a "meta-runbook" that documents when to deviate
  4. Feed this pattern to any AI agent operating on this infrastructure

tags: [meta-pattern, runbook-deviation, implicit-knowledge]
```

---

## Edge Types

| Edge | From → To | Meaning |
|------|-----------|---------|
| `solved_by` | Incident → Decision | This incident was resolved by this decision |
| `sets_precedent` | Decision → Decision | This decision establishes a pattern for future ones |
| `references` | Decision → Precedent | This decision explicitly cited this precedent |
| `similar_to` | Incident → Incident | These incidents share root cause or pattern |
| `affects` | Incident → Entity | This incident impacted this system |
| `depends_on` | Entity → Entity | System dependency |
| `operated_by` | Decision → Entity (person) | Who made this decision |
| `deviates_from` | Decision → Entity (runbook) | This decision broke from standard procedure |
| `triggers` | Incident → Incident | One incident caused another |
| `pattern_instance` | Decision → Pattern | This decision is an instance of this pattern |

---

## Query Templates

### 1. Precedent Search
```
INPUT: "AKS node NotReady + disk pressure"
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
INPUT: "camara-qod-api"
FIND:  All entities that depend on this service
SHOW:  Historical incidents, precedents, and patterns
```

### 4. Decision Quality
```
INPUT: "Rohit"
FIND:  All decisions made by this actor
SHOW:  Success rate, average MTTR, common patterns, exceptions
```

### 5. Runbook Gaps
```
INPUT: "aks runbook"
FIND:  Decisions that deviated from this runbook
SHOW:  What was skipped, why, and whether it should be updated
```
