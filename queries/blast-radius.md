# Query: Blast Radius Analysis

## "If X goes down, what else is affected?"

### How to Query
```bash
# Blast radius of a service
python3 analyze.py --type blast-radius "payment-api"

# Blast radius of infrastructure
python3 analyze.py --type blast-radius "prod-cluster"
```

### What the Context Graph Returns

For query: `"payment-api"`

**Entity:** payment-api (service, production)
**Cluster:** prod-cluster, primary region

**Depends on:**
- prod-cluster (Kubernetes cluster)
- key-vault (Secrets)
- provider-a-gateway (External API)
- primary-database (Database)

**Depended upon by:**
- api-gateway
- customer-dashboard

**Incident History:**
- 🔴 INC-001: Node NotReady — OOMKilled
- 🟠 INC-002: Provider timeout — 502s

**Decision History:**
- ⚡ DEC-001: Skip runtime restart (resolved INC-001)
- ⚡ DEC-002: Circuit breaker for provider (resolved INC-002)

### Why This Matters for Incident Response

When you get paged for `payment-api` errors:

1. **Check dependencies** — is it the service, or something it depends on?
2. **Check precedents** — has this happened before? What worked?
3. **Check patterns** — are there recurring issues?

The context graph gives you ALL of this in one query.

### vs Static Documentation

| Context Graph | Static Documentation |
|---------------|---------------------|
| "payment-api depends on provider-a which had a cert issue in INC-002" | "payment-api connects to external providers" |
| Shows precedent: circuit breaker worked | No precedent data |
| Shows temporal pattern: provider has recurring issues | No pattern recognition |
