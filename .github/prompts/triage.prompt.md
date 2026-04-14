---
name: triage
description: "Run incident triage — analyze events, cross-reference context graph, recommend fix, record decision"
---

# SRE Incident Triage Session

## Instructions

### Step 1: Read Context Graph
Read `docs/context-graph.md` in full. Note the last DE number and all active Exception Patterns.

### Step 2: Analyze Input
Analyze the event data below. Identify alert type, severity, affected resources, symptoms, temporal pattern.

### Step 3: Cross-Reference
Search the context graph for similar past DEs, matching EPs, and relevant entity dependencies.

### Step 4: Diagnose
Determine root cause (with confidence), whether it matches a known pattern (cite EP/DE), whether a runbook exception is needed.

### Step 5: Recommend
Provide immediate action, confidence level, precedent cited, any exceptions to standard procedure.

### Step 6: Record
Append a new Decision Event to `docs/context-graph.md`. Increment the DE number.

### Step 7: Pattern Check
If 3rd+ occurrence of same alert+action pattern, add to Exception Pattern Registry.

---

## Event Data

<!-- PASTE YOUR EVENT DATA BELOW -->
<!-- Supported: CSV, JSON, kubectl output, or plain text -->

<!-- Example:
Alert: Kubernetes Node NotReady
Cluster: prod-cluster
Node Pool: workloads
Nodes: node-abc123, node-def456
Time: 2026-04-14T09:15:00Z
Severity: P1
Symptom: 3 nodes NotReady, pods CrashLoopBackOff
-->

<!-- PASTE ABOVE -->

---

## Output Format

```
## 🔍 Triage Result

**Alert:** [type]
**Severity:** [P1/P2/P3/P4]
**Root Cause:** [diagnosis]
**Confidence:** [high/medium/low]
**Precedent:** [EP-XXX / DE-XXX / "NEW"]

### Recommendation
[action]

### Exception Required?
[Yes/No + details]

### Context Graph Updated
[Yes — DE-XXX appended]
```
