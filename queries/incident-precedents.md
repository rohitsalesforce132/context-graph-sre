# Query: Incident Precedents

## "What happened before like this?"

### How to Query
```bash
# Find precedents for a specific symptom
python3 analyze.py --type precedents "AKS node NotReady disk pressure"

# Find all decisions related to an incident
python3 analyze.py --type decisions --incident INC-001

# General search across all nodes
python3 analyze.py "OOMKilled camara"
```

### What the Context Graph Returns

For query: `"AKS node NotReady disk pressure"`

1. **Precedent PRE-001** (score: 25)
   - Pattern: Skip kubelet restart, clean disk first
   - Confidence: high
   - Based on: 3 incidents, 100% success rate
   - Recommendation: [full step-by-step procedure]

2. **Decision DEC-001** (score: 16)
   - Skipped kubelet restart → resolved in 12 min
   - AI Reproducible: YES
   - Precedent chain: DEC-002 → DEC-004 → DEC-001

3. **Decision DEC-002** (score: 12)
   - Followed runbook (kubelet restart) → 15 min extended outage
   - Lesson: Kubelet restart on disk-pressure nodes is dangerous

### vs Knowledge Graph Response

| Context Graph | Knowledge Graph |
|---------------|-----------------|
| "Skip kubelet restart based on DEC-002 failure pattern" | "AKS node NotReady runbook: Step 1, Step 2 (restart kubelet)..." |
| Returns PRECEDENT + REASONING | Returns DOCUMENTATION only |
| Includes temporal evolution (3 decisions over 3 months) | Static snapshot |
| Shows what NOT to do + why | Only shows what to do |
