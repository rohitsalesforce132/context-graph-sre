# Behavioral Observation Template

Use this to capture patterns you notice in how the team operates — even outside incidents.

```yaml
id: OBS-XXX
type: observation
title: ""
timestamp: ""
observer: ""

# What you noticed
pattern: ""

# Where you see it
evidence:
  - description: ""
    refs: []  # INC-XXX, DEC-XXX, etc.

# Why it matters
implications: []

# What should change
recommendation: ""

# Is this captured anywhere else?
currently_documented: true|false
if_yes_where: ""

tags: []
```

---

## Example

```yaml
id: OBS-001
type: observation
title: "Team checks chat history before official runbook during incidents"
timestamp: "2026-04-14T16:00:00+05:30"
observer: engineer-a

pattern: |
  During the last 4 P2 incidents, the on-call engineer first checked
  the team's chat history and personal notes before opening the
  official runbook. The runbook was consulted only after initial
  investigation failed.

evidence:
  - description: "INC-003: Engineer checked team chat first, then runbook"
    refs: [INC-003]
  - description: "INC-001: Engineer knew to skip runbook step from personal experience"
    refs: [INC-001, DEC-001]

implications:
  - "Runbooks are not the first source of truth during incidents"
  - "Institutional knowledge lives in chat, not documentation"
  - "New team members are at a disadvantage"
  - "AI agents relying only on runbooks will make suboptimal decisions"

recommendation: |
  1. Create a "living runbook" updated after every incident
  2. Embed context graph queries into incident response workflow
  3. Ensure AI agents have access to decision traces, not just runbooks

currently_documented: false

tags: [meta-pattern, information-source, runbook-gap, team-behavior]
```
