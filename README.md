# 🧠 Context Graph for SRE Operations

> **Not a knowledge graph. A decision graph.**
>
> Capture HOW your team makes decisions during incidents — not just what happened, but WHY, by WHOM, under WHAT conditions, and what PRECEDENT it set.

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-green.svg)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Copilot Agent Ready](https://img.shields.io/badge/copilot-agent%20mode-purple.svg)](https://docs.github.com/en/copilot)

---

## The Problem

Every on-call team has invisible institutional knowledge:

```
🔴  Incident fires at 3AM
📖  Junior engineer opens runbook
⚙️  Follows every step exactly
💥  Makes things WORSE (step 2 is wrong for this case)
😤  Senior engineer wakes up: "Skip step 2, that broke things last time"
✅  Resolved in 5 minutes
📝  Post-mortem: "Follow runbook" (nobody mentions step 2 was skipped)
🔄  Next month: different junior engineer hits the same issue
```

**The senior engineer's judgment was invisible.** The runbook didn't capture it. The post-mortem didn't mention it.

Context graphs make that knowledge visible, queryable, and available to AI agents.

---

## What is a Context Graph?

A **context graph** captures **decision events** — the full reasoning chain behind each action during incidents:

| Field | What It Records |
|-------|----------------|
| **What was decided** | The specific action taken |
| **Options considered** | What alternatives were evaluated (and rejected) |
| **Exceptions** | What rules/runbooks were bent, and why |
| **Precedents** | What past decisions influenced this one |
| **Conditions** | What was true at decision time (load, time, recent deploys) |
| **Outcome** | Did it work? How fast vs. average? |
| **AI Reproducible** | Could an autonomous agent make this same call? |

Over time, these compound into a **queryable record of institutional intelligence**.

---

## Quick Start (5 minutes)

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/context-graph-sre.git
cd context-graph-sre

# Search the graph
python3 analyze.py "disk pressure"

# Find precedents for an incident
python3 analyze.py --type precedents "node NotReady"

# See blast radius of a service
python3 analyze.py --type blast-radius "payment-api"

# Audit all exceptions (where runbooks don't match reality)
python3 analyze.py --type exceptions

# Visualize the graph
bash visualize.sh
```

---

## How It Works

```
INCIDENT → TRIAGE → CROSS-REF GRAPH → DECIDE → ACT → RECORD → PROMOTE
              │              │             │        │       │        │
          Analyze       Find         Choose    Execute  Append   If 3x same
          event data    precedents   action    fix      DE to    pattern,
                         & patterns  (cite     → done   graph    add to
                                      EP/DE)                    Exception
                                                                Registry
```

**The graph compounds.** Every incident makes future decisions faster.

---

## Context Graph vs Knowledge Graph vs Runbook

| Question | Runbook | Knowledge Graph | Context Graph |
|----------|---------|----------------|---------------|
| How do I restart a node? | ✅ Steps | ✅ Link | ✅ + when NOT to |
| What depends on service X? | ❌ | ✅ | ✅ + incident history |
| Why did someone skip step 2? | ❌ | ❌ | ✅ Full rationale |
| What precedent exists for this? | ❌ | ❌ | ✅ Searchable chain |
| What exceptions keep getting made? | ❌ | ❌ | ✅ Pattern detected |
| Can an AI agent decide this? | ❌ | ❌ | ✅ Explicitly marked |

**You need all three.** Runbooks provide procedure. Knowledge graphs provide structure. Context graphs provide judgment.

---

## Folder Structure

```
context-graph-sre/
├── README.md                           ← You are here
├── schema.md                           ← Graph schema reference
├── LICENSE                             ← MIT
│
├── graph/                              ← THE GRAPH DATA
│   ├── incidents/                      ← What happened
│   │   └── INC-001.md                  ← Example: Node disk pressure
│   ├── decisions/                      ← Why it was handled this way
│   │   └── DEC-001.md                  ← Example: Skip kubelet restart
│   ├── precedents/                     ← How patterns evolved over time
│   │   └── PRE-001.md                  ← Example: Disk pressure response
│   ├── entities/                       ← Systems, services, infrastructure
│   │   └── ENT-prod-cluster.md         ← Example: Production cluster
│   └── patterns/                       ← Behavioral meta-patterns
│       └── PAT-001.md                  ← Example: Engineers skip runbook steps
│
├── ingest/                             ← Templates for new entries
│   ├── incident-template.md
│   ├── decision-template.md
│   └── observation-template.md
│
├── queries/                            ← Query guides
│   ├── incident-precedents.md
│   ├── exception-patterns.md
│   ├── blast-radius.md
│   └── decision-history.md
│
├── analyze.py                          ← Query engine
├── visualize.sh                        ← Graph visualizer
│
├── .github/                            ← Copilot Agent integration
│   ├── copilot-instructions.md
│   └── prompts/
│       └── triage.prompt.md
│
└── docs/
    └── context-graph.md                ← Living file for Copilot
```

**22 files. Zero dependencies. No database. No server.**

---

## The 5 Node Types

### 1. Incident Event
What happened — symptoms, affected services, timeline, conditions at the time.

### 2. Decision Trace
**The core innovation.** Full reasoning chain: options considered, exceptions made, precedents cited, outcome measured, AI reproducibility assessed.

### 3. Precedent Chain
How a response pattern EVOLVED over time. Multiple decisions stitched into a learning timeline.

### 4. Entity
Systems, services, people — the structural knowledge graph layer with dependency mapping.

### 5. Behavioral Pattern
Meta-patterns recognized across many decisions. Captures organizational intelligence.

---

## Query Engine

```bash
# General search
python3 analyze.py "OOMKilled"

# Precedent search (use during incidents)
python3 analyze.py --type precedents "node NotReady"

# Blast radius analysis
python3 analyze.py --type blast-radius "payment-api"

# Exception audit (where docs don't match reality)
python3 analyze.py --type exceptions

# Runbook gap analysis
python3 analyze.py --type runbook-gaps

# Behavioral patterns
python3 analyze.py --type patterns

# Decision history
python3 analyze.py --type decisions "timeout"
```

---

## GitHub Copilot Integration

This project includes **Copilot Agent Mode** integration:

1. Enable in VS Code settings:
   ```json
   {
     "github.copilot.chat.agent.enabled": true,
     "chat.promptFiles": true
   }
   ```

2. Switch Copilot Chat to **Agent mode**

3. Type `/triage` + paste your event data

4. Copilot will:
   - Read the context graph
   - Cross-reference for precedents
   - Diagnose and recommend
   - **Automatically append a new Decision Event**
   - Promote patterns after 3 occurrences

---

## Real Example: Decision Trace

```yaml
id: DEC-001
type: decision_trace
title: "Skipped kubelet restart, went straight to disk cleanup"

decision: "Skip runbook step 2, go to disk cleanup"
rationale: "Kubelet restart caused 15-min outage last time (DEC-002)"

options_considered:
  - option: "Follow runbook: restart kubelet first"
    rejected_because: "Precedent DEC-002: caused cascading pod evictions"
  - option: "Disk cleanup first, skip kubelet"
    chosen: true
    confidence: high

exceptions:
  - rule: "Runbook step 2: restart kubelet"
    deviation: "Skipped entirely"
    justification: "DEC-002 proved restart causes extended outage"

precedents:
  - ref: DEC-002
  - ref: DEC-007

outcome:
  result: "Resolved in 12 minutes (vs 35 min with runbook)"
  mttr_improvement: "66%"

ai_reproducible: true
ai_reproducible_notes: "Agent with DEC-002 access would make same call"
```

**This is institutional memory, queryable by any engineer or AI agent.**

---

## Why This Matters

- **MTTR reduction:** 66% faster when engineers use precedent-based decisions vs. blind runbook following
- **Onboarding:** New engineers get years of institutional knowledge on day one
- **AI readiness:** Agents make better decisions when they have context, not just rules
- **Compliance:** Every decision is traceable, auditable, justified
- **Compounding:** The graph gets more valuable with every entry

---

## Scaling

| Stage | Entries | Strategy |
|-------|---------|----------|
| Startup | 0-50 | Single files, `analyze.py` queries |
| Growth | 50-200 | Split by year, add tags |
| Scale | 200-500 | Add SQLite index layer |
| Enterprise | 500+ | Archive old entries, keep active graph lean |

---

## Contributing

1. Fork the repo
2. Add your own sample data (use templates in `ingest/`)
3. Submit a PR with new query types, visualizations, or integrations

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Credits

Built on the **Context Graph** concept from [Foundation Capital's research](https://foundationcap.com) on agentic AI infrastructure.

> *"Context graphs are not a feature. They are a foundation."*

---

## License

[MIT](LICENSE) — use it, fork it, build on it.

---

*Built for SREs who are tired of 3 AM incidents where the answer was "we figured this out last time but nobody wrote it down."*
