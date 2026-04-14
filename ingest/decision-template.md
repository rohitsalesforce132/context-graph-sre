# Decision Trace Template

```yaml
id: DEC-XXX
type: decision_trace
title: ""
timestamp: ""                   # ISO 8601
incident_ref: INC-XXX           # Which incident triggered this decision

# ─── THE DECISION ───────────────────────────────────
decision: ""                    # What was decided
rationale: ""                   # Why this option was chosen

# ─── OPTIONS CONSIDERED ─────────────────────────────
options_considered:
  - option: ""
    chosen: false
    rejected_because: ""
  - option: ""
    chosen: true
    confidence: high|medium|low

# ─── EXCEPTIONS MADE ────────────────────────────────
exceptions:
  - rule: ""                    # What rule/policy/runbook step
    deviation: ""               # What was done differently
    justification: ""           # Why it was justified
    approved_by: ""             # Who approved (or "on-call judgment")

# ─── PRECEDENT CHAIN ────────────────────────────────
precedents:
  - ref: DEC-XXX
    similarity: ""

# ─── ORGANIZATIONAL STATE ───────────────────────────
organizational_state:
  other_active_incidents: 0
  team_availability: ""
  customer_impact: ""
  sla_breach_risk: low|medium|high|critical
  business_context: ""

# ─── OUTCOME ────────────────────────────────────────
outcome:
  result: ""
  mttr_minutes: 0
  mttr_vs_average: ""
  side_effects: ""
  follow_up: ""

# ─── ACTOR ──────────────────────────────────────────
actor:
  name: ""
  role: ""
  experience_level: ""

# ─── AI READINESS ───────────────────────────────────
ai_reproducible: true|false
ai_reproducible_notes: ""

tags: []
```

---

## Example: Filled In

```yaml
id: DEC-003
type: decision_trace
title: "Added circuit breaker instead of increasing upstream timeout"
timestamp: "2026-04-14T09:22:00+05:30"
incident_ref: INC-003

decision: "Add circuit breaker with 10s timeout, fail fast instead of waiting 30s"
rationale: "Provider cert expiry is their problem. Our API shouldn't hang consuming resources."

options_considered:
  - option: "Increase timeout from 30s to 60s"
    chosen: false
    rejected_because: "Just delays the 502, risks thread pool exhaustion."
  - option: "Add circuit breaker with 10s timeout, fail fast with meaningful error"
    chosen: true
    confidence: high
  - option: "Disable provider entirely until they fix cert"
    chosen: false
    rejected_because: "Too aggressive, some requests still succeed within 5s."

exceptions:
  - rule: "Upstream timeout configured at 30s in infrastructure module"
    deviation: "Overriding to 10s via app config"
    justification: "Circuit breaker is standard resilience pattern. IaC update will follow."
    approved_by: "on-call judgment (will retro in standup)"

precedents:
  - ref: DEC-005
    similarity: "Previous provider timeout — timeout increase failed"

organizational_state:
  other_active_incidents: 0
  team_availability: "Full team"
  customer_impact: "~15% of traffic affected"
  sla_breach_risk: medium
  business_context: "Normal operations"

outcome:
  result: "Circuit breaker deployed, requests fail fast (10s)"
  mttr_minutes: 13
  mttr_vs_average: "50% faster than previous similar incident"
  side_effects: "Requests in 10-30s window now fail — acceptable tradeoff"
  follow_up: "Update IaC module to support per-provider timeout config"

actor:
  name: engineer-a
  role: on_call
  experience_level: "Familiar with provider integration patterns"

ai_reproducible: true
ai_reproducible_notes: "Circuit breaker is standard SRE pattern. Agent with resilience knowledge could make same call."

tags: [circuit-breaker, provider-timeout, config-override, precedent-setting]
```
