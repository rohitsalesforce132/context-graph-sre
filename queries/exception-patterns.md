# Query: Exception Audit

## "What rules have been bent, by whom, and why?"

### How to Query
```bash
# All exceptions
python3 analyze.py --type exceptions

# Exceptions in last 30 days
python3 analyze.py --type exceptions --last 30d
```

### Why This Query Matters

Exceptions reveal **institutional intelligence** — the gap between how documentation says things should work, and how they actually work.

Every exception is:
- A rule that's too rigid for reality
- A judgment call that experienced people make naturally
- Knowledge that would be LOST if the person left

### What You Find

**Decision DEC-001:**
- Rule: "SRE Runbook: Step 2 — restart kubelet"
- Deviation: Skipped entirely
- Why: "Precedent shows kubelet restart causes cascading evictions"
- Who: Rohit (on-call judgment)
- Outcome: ✅ Resolved 66% faster

**Decision DEC-003:**
- Rule: "Carrier timeout configured at 30s in terraform"
- Deviation: Overridden to 10s via app config
- Why: "Circuit breaker pattern is more resilient than long timeout"
- Who: Rohit (on-call judgment)
- Outcome: ✅ 50% faster MTTR

### The Pattern

Every exception tells a story:
1. The rule was written for a general case
2. Reality demanded a specific deviation
3. The deviation worked better than the rule
4. **The rule should be updated** — but it probably won't be

This is the gap that context graphs fill.
