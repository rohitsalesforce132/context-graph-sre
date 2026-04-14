# Query: Runbook Gap Analysis

## "Where do runbooks not match reality?"

### How to Query
```bash
python3 analyze.py --type runbook-gaps
```

### What It Finds

Every decision that deviated from a runbook is a **runbook gap** — a place where the documentation doesn't match how experienced engineers actually work.

### Sample Output

**Rule: "SRE Runbook: aks-node-notready.md — Step 2: restart kubelet"**
- Deviations: 2
- DEC-001: Skipped step 2 (kubelet restart)
  - Why: DEC-002 proved kubelet restart causes cascading evictions
  - Outcome: ✅ 12-min resolution
- DEC-004: Partial skip (disk cleanup first, kubelet restart as backup)
  - Why: Growing evidence that disk cleanup alone is sufficient
  - Outcome: ✅ 18-min resolution

**Recommendation:** Rewrite step 2 to check disk pressure first. Move kubelet restart to step 6.

### The Meta Pattern

Runbook gaps are the MOST valuable data in the context graph because they:
1. Reveal implicit knowledge
2. Show where documentation is actively harmful
3. Identify where AI agents would make wrong decisions
4. Provide actionable improvements

Every gap is an opportunity to:
- Update the runbook
- Capture the implicit knowledge
- Make AI agents smarter
