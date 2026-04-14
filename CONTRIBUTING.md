# Contributing to Context Graph for SRE

## Quick Start

1. Fork the repo
2. Create a feature branch: `git checkout -b my-feature`
3. Make changes
4. Test: `python3 analyze.py "test query"`
5. Submit PR

## What We're Looking For

### 🎯 High Priority
- **New query types** in `analyze.py` (e.g., trend analysis, anomaly detection)
- **Auto-ingest connectors** (PagerDuty webhook, Azure Monitor, Datadog, etc.)
- **Visualizations** (Mermaid graphs, HTML dashboards, Grafana panels)
- **Real-world sample data** (sanitized, no company-specific references)

### 🔄 Medium Priority
- Schema improvements
- Copilot prompt enhancements
- Shell completions
- CI/CD integration examples

### 💡 Ideas Welcome
- Multi-team graph federation
- Compliance/audit reporting
- Slack/Teams bot integration
- GraphQL API layer

## Guidelines

- **Zero external dependencies** — keep it portable. Python stdlib + yaml only.
- **Generic by default** — no company-specific references in sample data
- **Markdown-first** — all data as Markdown + YAML frontmatter
- **Append-only** — never delete context graph entries, only archive
- **Tags for search** — every node should have meaningful tags

## Adding Sample Data

Use the templates in `ingest/`:

1. Copy the appropriate template
2. Fill in with **generic, sanitized** data (no real hostnames, IPs, or company names)
3. Place in the correct `graph/` subdirectory
4. Test with `python3 analyze.py "<your tags>"`

## Reporting Issues

- Bug reports: include Python version, OS, and the query you ran
- Feature requests: describe the use case, not just the solution

## Code of Conduct

Be respectful. Be constructive. Be excellent to each other.
