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
# This is critical: show what alternatives were evaluated
options_considered:
  - option: ""
    chosen: false
    rejected_because: ""
  - option: ""
    chosen: true
    confidence: high|medium|low

# ─── EXCEPTIONS MADE ────────────────────────────────
# Did this decision break any rules, policies, or runbooks?
exceptions:
  - rule: ""                    # What rule/policy/runbook step
    deviation: ""               # What was done differently
    justification: ""           # Why it was justified
    approved_by: ""             # Who approved (or "on-call judgment")

# ─── PRECEDENT CHAIN ────────────────────────────────
# What past decisions influenced this one?
precedents:
  - ref: DEC-XXX
    similarity: ""

# ─── ORGANIZATIONAL STATE ───────────────────────────
# What was happening in the organization at decision time?
organizational_state:
  other_active_incidents: 0
  team_availability: ""
  customer_impact: ""
  sla_breach_risk: low|medium|high|critical
  business_context: ""          # quarter end? major launch? holiday?

# ─── OUTCOME ────────────────────────────────────────
outcome:
  result: ""                    # What happened
  mttr_minutes: 0               # How long to resolve
  mttr_vs_average: ""           # Better/worse than usual?
  side_effects: ""              # Any unintended consequences?
  follow_up: ""                 # What should change because of this?

# ─── ACTOR ──────────────────────────────────────────
actor:
  name: ""
  role: ""
  experience_level: ""          # How familiar were they with this type of issue?

# ─── AI READINESS ───────────────────────────────────
# Could an AI agent have made this decision?
ai_reproducible: true|false
ai_reproducible_notes: ""       # Why or why not?

tags: []
```

---

## Example: Filled In

```yaml
id: DEC-003
type: decision_trace
title: "Added circuit breaker instead of increasing timeout for Aduna"
timestamp: "2026-04-14T09:22:00+05:30"
incident_ref: INC-003

decision: "Add circuit breaker with 10s timeout for Aduna carrier, fail fast instead of waiting 30s"
rationale: "Aduna cert expiry is their problem. Our API shouldn't hang for 30s waiting for them."

options_considered:
  - option: "Increase timeout from 30s to 60s"
    chosen: false
    rejected_because: "Just delays the 502, doesn't solve it. Also risks thread pool exhaustion."
  - option: "Add circuit breaker with 10s timeout, fail fast with meaningful error"
    chosen: true
    confidence: high
  - option: "Disable Aduna carrier entirely until they fix cert"
    chosen: false
    rejected_because: "Too aggressive, would impact legitimate requests that succeed within 5s"

exceptions:
  - rule: "Carrier timeout is configured at 30s in terraform module"
    deviation: "Overriding to 10s via app config, will update terraform later"
    justification: "30s is too long for cert-related failures. Circuit breaker pattern is more resilient."
    approved_by: "Rohit (on-call judgment, will retro in standup)"

precedents:
  - ref: DEC-005
    similarity: "Previous Aduna timeout — we increased timeout then, which didn't help"

organizational_state:
  other_active_incidents: 0
  team_availability: "Full team"
  customer_impact: "Aduna requests failing, ~15% of traffic"
  sla_breach_risk: medium
  business_context: "Normal operations"

outcome:
  result: "Circuit breaker deployed, Aduna requests fail fast (10s), other carriers unaffected"
  mttr_minutes: 13
  mttr_vs_average: "50% faster than INC-005 resolution"
  side_effects: "Aduna requests that would've succeeded in 10-30s now fail — acceptable tradeoff"
  follow_up: "Update terraform module to support per-carrier timeout config"

actor:
  name: Rohit
  role: on_call
  experience_level: "3 months experience with CAMARA carrier integrations"

ai_reproducible: true
ai_reproducible_notes: "Circuit breaker pattern is well-documented. Precedent DEC-005 shows timeout increase failed. An AI agent with access to DEC-005 could've made this same decision."

tags: [circuit-breaker, carrier-timeout, aduna, config-override, precedent-setting]
```
