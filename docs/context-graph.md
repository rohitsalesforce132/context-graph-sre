# SRE Context Graph — Living Document

> Copilot agent reads and writes this file during triage sessions.
> **Never delete entries. Only append.**
> Last updated: 2026-04-14 | Last DE: DE-002 | Last EP: EP-001

---

## Infrastructure Entity Map

### Clusters

| Cluster | Environment | Node Pools | Purpose |
|---------|-------------|------------|---------|
| prod-cluster | PROD | system (3), workloads (5) | Production APIs |
| staging-cluster | STAGING | system (1), workloads (2) | Pre-production |
| dev-cluster | DEV | system (1), workloads (1) | Development |

### Key Services

| Service | Cluster | Language | External Dependencies |
|---------|---------|----------|----------------------|
| payment-api | prod-cluster | Java | provider-a, provider-b |
| user-service | prod-cluster | Java | primary-database |
| notification-service | prod-cluster | Java | email-provider, sms-provider |

### Dependency Map

```
api-gateway
├── payment-api
│   ├── prod-cluster (workloads node pool)
│   ├── key-vault
│   ├── provider-a-gateway
│   └── primary-database
├── user-service
│   ├── prod-cluster (workloads node pool)
│   ├── key-vault
│   └── primary-database
└── notification-service
    ├── prod-cluster (workloads node pool)
    ├── email-provider
    └── sms-provider
```

---

## Exception Pattern Registry

### EP-001 | Node NotReady + Disk Pressure → Skip Runtime Restart

**Pattern:** When nodes go NotReady with DiskPressure, do NOT restart container runtime first. Clean disk.

**Evidence:** DEC-001

**Procedure:**
1. Confirm DiskPressure: `kubectl describe node <node> | grep -A5 Conditions`
2. Check disk: `ssh <node> "df -h /var/lib/kubelet"`
3. Clean images: `crictl rmi --prune` or `docker image prune -a`
4. Clean logs: `journalctl --vacuum-time=2d`
5. Wait 2 min, check status
6. Only restart runtime if STILL NotReady

**Confidence:** Medium (1 incident so far) | Needs 2 more to confirm

---

## Decision Event Log

---

### DE-002 | 2026-04-14 | prod-cluster | P2

**Alert:** API 502 errors for provider-a — 30s timeout, 40% failure rate
**Conditions:** 09:15 (morning peak), 45% CPU / 52% memory, no recent deploys
**Root Cause:** Provider-a TLS certificate expired
**Action Taken:** Added circuit breaker with 10s timeout, fail fast
**Precedent:** NEW — no prior precedent for provider timeout
**Exception:** Overrode IaC-configured 30s timeout to 10s via app config
**AI Reproducible:** Yes — circuit breaker is standard resilience pattern
**Outcome:** 502 rate dropped to 0% in 13 minutes. Provider renewed cert at 10:30.
**Follow-up:** Add cert expiry monitoring. Per-provider timeout in IaC.
**Tags:** circuit-breaker, provider-timeout, cert-expiry, p2

---

### DE-001 | 2026-04-12 | prod-cluster | P1

**Alert:** 3 nodes NotReady — pods CrashLoopBackOff
**Conditions:** 14:23 (afternoon), 78% CPU / 65% memory, payment-api v2.3.1 deployed 2h prior
**Root Cause:** Disk pressure — image layers from 90+ days, /var/lib/kubelet at 95%
**Action Taken:** Skipped runbook step 2 (runtime restart), went to disk cleanup
**Precedent:** NEW — first occurrence
**Exception:** Skipped runbook step 2
**AI Reproducible:** Yes — disk cleanup before runtime restart is defensible
**Outcome:** Resolved in 12 minutes. Zero pod evictions.
**Follow-up:** Update runbook. Add weekly image prune. Increase OS disk.
**Tags:** kubernetes, disk-pressure, node-notready, runbook-exception, p1

---

## Statistics

| Metric | Value |
|--------|-------|
| Total Decision Events | 2 |
| Exception Patterns | 1 |
| P1 Incidents | 1 |
| P2 Incidents | 1 |
| AI Reproducible | 2/2 (100%) |
| Avg MTTR | 12.5 min |
