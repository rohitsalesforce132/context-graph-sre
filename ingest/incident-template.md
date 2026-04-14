# Incident Event Template

```yaml
id: INC-XXX                    # Sequential ID
type: incident_event
title: ""                       # Short description
timestamp: ""                   # ISO 8601
severity: P1|P2|P3|P4
status: open|investigating|mitigated|resolved

# What happened
symptom: ""
affected_services: []
blast_radius: ""

# Conditions at the time (THIS IS THE KEY — what was true when it happened)
conditions:
  time_of_day: ""
  active_incidents: 0
  change_freeze: false
  on_call: ""
  recent_deploys: ""
  cluster_load: ""
  weather: ""                   # yes, even weather matters sometimes
  team_availability: ""         # holiday? skeleton crew?

# Who was involved
actors:
  - role: on_call|escalation|manager|vendor
    person: ""

# Timeline
detected_at: ""
mitigated_at: ""
resolved_at: ""
ttk_minutes: 0                  # time to know
ttm_minutes: 0                  # time to mitigate
ttr_minutes: 0                  # time to resolve

# Links to decisions made during this incident
decision_refs: []
  # - DEC-XXX

# Links to entities affected
entity_refs: []
  # - ENT-xxx

# Links to similar past incidents
similar_incident_refs: []
  # - INC-XXX

# Root cause (filled in post-incident)
root_cause: ""
root_cause_category: ""         # config_error|resource_exhaustion|bug|dependency|human_error|unknown

# Follow-up actions
follow_up: []

# Tags for graph traversal
tags: []
```

---

## Example: Filled In

```yaml
id: INC-003
type: incident_event
title: "CAMARA QOD API 502 errors - carrier Aduna timeout"
timestamp: "2026-04-14T09:15:00+05:30"
severity: P2
status: resolved

symptom: "Aduna carrier requests to QOD API returning 502 after 30s timeout"
affected_services:
  - camara-qod-api
  - aduna-carrier-gateway
blast_radius: "Aduna carrier only, PROD region, ~15% of QOD traffic"

conditions:
  time_of_day: "09:15 IST (morning peak, Europe coming online)"
  active_incidents: 0
  change_freeze: false
  on_call: "Rohit"
  recent_deploys: "None in last 24h"
  cluster_load: "45% CPU, 52% memory"
  team_availability: "Full team"

actors:
  - role: on_call
    person: Rohit
  - role: vendor
    person: "Aduna NOC (escalated)"

detected_at: "2026-04-14T09:15:00+05:30"
mitigated_at: "2026-04-14T09:28:00+05:30"
resolved_at: "2026-04-14T10:45:00+05:30"
ttk_minutes: 0
ttm_minutes: 13
ttr_minutes: 90

decision_refs:
  - DEC-003

entity_refs:
  - ENT-camara-qod-api
  - ENT-aduna-carrier-gateway

similar_incident_refs:
  - INC-005  # Previous Aduna timeout in Feb

root_cause: "Aduna carrier gateway certificate expired, their NOC confirmed"
root_cause_category: dependency

follow_up:
  - "Add cert expiry monitoring for carrier gateways"
  - "Create alert: carrier response time > 10s for 5 min"

tags: [camara, qod, aduna, carrier-timeout, cert-expiry, p2]
```
