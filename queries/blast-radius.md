# Query: Blast Radius Analysis

## "If X goes down, what else is affected?"

### How to Query
```bash
# Blast radius of a service
python3 analyze.py --type blast-radius "camara-qod-api"

# Blast radius of infrastructure
python3 analyze.py --type blast-radius "aks-prod-01"
```

### What the Context Graph Returns

For query: `"camara-qod-api"`

**Entity:** camara-qod-api (service, production)
**Cluster:** aks-prod-01, eastus2

**Depends on:**
- aks-prod-01 (Kubernetes cluster)
- kv-camara (Key Vault)
- aduna-carrier-gateway (Carrier API)
- azure-db-camara (Database)

**Depended upon by:**
- camara-api-gateway
- carrier-dashboard

**Incident History:**
- 🔴 INC-001: AKS node NotReady — OOMKilled
- 🟠 INC-003: Aduna carrier timeout — 502s

**Decision History:**
- ⚡ DEC-001: Skip kubelet restart (resolved INC-001)
- ⚡ DEC-003: Circuit breaker for Aduna (resolved INC-003)

### Why This Matters for Incident Response

When you get paged for `camara-qod-api` errors:

1. **Check dependencies** — is it the service, or something it depends on?
2. **Check precedents** — has this happened before? What worked?
3. **Check patterns** — are there recurring issues?

The context graph gives you ALL of this in one query. No digging through Slack, runbooks, and post-mortems.

### vs Static Documentation

| Context Graph | Static Documentation |
|---------------|---------------------|
| "camara-qod-api depends on Aduna which had a cert issue in INC-003" | "camara-qod-api connects to carrier gateways" |
| Shows precedent: circuit breaker worked | No precedent data |
| Shows temporal pattern: Aduna has recurring issues | No pattern recognition |
