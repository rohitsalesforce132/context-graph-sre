#!/usr/bin/env python3
"""
Context Graph Query Engine for SRE Operations
==============================================
Queries the context graph to find precedents, decision traces, and patterns.

Usage:
    python3 analyze.py "AKS node NotReady"
    python3 analyze.py --type precedents "disk pressure"
    python3 analyze.py --type decisions --incident INC-001
    python3 analyze.py --type patterns
    python3 analyze.py --type blast-radius "camara-qod-api"
    python3 analyze.py --type exceptions --last 30d
"""

import os
import sys
import re
import yaml
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

GRAPH_DIR = Path(__file__).parent / "graph"

# ─── YAML Loading ───────────────────────────────────

def load_yaml_files(directory):
    """Load all YAML frontmatter from .md files in a directory."""
    results = []
    if not directory.exists():
        return results
    
    for md_file in sorted(directory.glob("*.md")):
        content = md_file.read_text()
        # Extract YAML between ``` markers or at start
        yaml_match = re.search(r'```yaml\n(.*?)```', content, re.DOTALL)
        if yaml_match:
            try:
                data = yaml.safe_load(yaml_match.group(1))
                if data:
                    data['_source_file'] = str(md_file.name)
                    results.append(data)
            except yaml.YAMLError:
                pass
    return results

def load_all_graph_data():
    """Load all nodes from the graph directory."""
    return {
        'incidents': load_yaml_files(GRAPH_DIR / "incidents"),
        'decisions': load_yaml_files(GRAPH_DIR / "decisions"),
        'precedents': load_yaml_files(GRAPH_DIR / "precedents"),
        'entities': load_yaml_files(GRAPH_DIR / "entities"),
        'patterns': load_yaml_files(GRAPH_DIR / "patterns"),
    }

# ─── Search Functions ───────────────────────────────

def search_by_text(data, query, fields=None):
    """Search across all nodes for text matches."""
    query_lower = query.lower()
    query_words = set(query_lower.split())
    results = []
    
    for node_type, nodes in data.items():
        for node in nodes:
            score = 0
            match_reasons = []
            
            # Search in all string fields
            text = json.dumps(node, default=str).lower()
            
            # Exact phrase match (highest score)
            if query_lower in text:
                score += 10
                match_reasons.append(f"exact phrase match")
            
            # Individual word matches
            for word in query_words:
                if word in text:
                    score += 2
                    match_reasons.append(f"word match: '{word}'")
            
            # Tag matches (high value)
            tags = node.get('tags', [])
            for tag in tags:
                if query_lower in tag.lower():
                    score += 5
                    match_reasons.append(f"tag match: '{tag}'")
            
            if score > 0:
                results.append({
                    'node': node,
                    'type': node_type,
                    'score': score,
                    'reasons': match_reasons,
                })
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

def find_precedents(data, query):
    """Find precedent chains related to a query."""
    results = []
    
    # First find relevant precedents
    for precedent in data.get('precedents', []):
        score = 0
        text = json.dumps(precedent, default=str).lower()
        query_lower = query.lower()
        
        if query_lower in text:
            score += 10
        
        for word in query_lower.split():
            if word in text:
                score += 3
        
        if score > 0:
            results.append({
                'type': 'precedent',
                'id': precedent.get('id'),
                'title': precedent.get('title'),
                'score': score,
                'recommendation': precedent.get('recommendation', ''),
                'confidence': precedent.get('confidence', ''),
                'evolution': precedent.get('evolution', []),
            })
    
    # Also find relevant decisions
    for decision in data.get('decisions', []):
        score = 0
        text = json.dumps(decision, default=str).lower()
        query_lower = query.lower()
        
        if query_lower in text:
            score += 8
        
        if score > 0:
            results.append({
                'type': 'decision',
                'id': decision.get('id'),
                'title': decision.get('title'),
                'score': score,
                'incident_ref': decision.get('incident_ref'),
                'outcome': decision.get('outcome', {}).get('result', ''),
                'ai_reproducible': decision.get('ai_reproducible', ''),
            })
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

def find_blast_radius(data, entity_name):
    """Find everything connected to an entity."""
    entity_name_lower = entity_name.lower()
    results = {
        'entity': None,
        'depends_on': [],
        'depended_upon_by': [],
        'incidents': [],
        'decisions': [],
        'patterns': [],
    }
    
    # Find the entity
    for entity in data.get('entities', []):
        if entity_name_lower in entity.get('name', '').lower() or \
           entity_name_lower in entity.get('id', '').lower():
            results['entity'] = entity
            results['depends_on'] = entity.get('depends_on', [])
            results['depended_upon_by'] = entity.get('depended_upon_by', [])
            break
    
    # Find related incidents
    for incident in data.get('incidents', []):
        services = [s.lower() for s in incident.get('affected_services', [])]
        if any(entity_name_lower in s for s in services) or \
           entity_name_lower in json.dumps(incident.get('entity_refs', [])).lower():
            results['incidents'].append({
                'id': incident.get('id'),
                'title': incident.get('title'),
                'severity': incident.get('severity'),
                'timestamp': incident.get('timestamp'),
                'root_cause': incident.get('root_cause', ''),
            })
    
    # Find related decisions
    for decision in data.get('decisions', []):
        text = json.dumps(decision, default=str).lower()
        if entity_name_lower in text:
            results['decisions'].append({
                'id': decision.get('id'),
                'title': decision.get('title'),
                'outcome': decision.get('outcome', {}).get('result', ''),
            })
    
    return results

def find_exceptions(data, last_n_days=None):
    """Find all decisions where exceptions were made."""
    results = []
    
    for decision in data.get('decisions', []):
        exceptions = decision.get('exceptions', [])
        if exceptions:
            # Time filter
            if last_n_days:
                ts = decision.get('timestamp', '')
                try:
                    dt = datetime.fromisoformat(ts.replace('+05:30', '+05:30'))
                    if dt < datetime.now().astimezone() - timedelta(days=last_n_days):
                        continue
                except (ValueError, TypeError):
                    pass
            
            results.append({
                'id': decision.get('id'),
                'title': decision.get('title'),
                'timestamp': decision.get('timestamp'),
                'incident_ref': decision.get('incident_ref'),
                'exceptions': exceptions,
                'actor': decision.get('actor', {}).get('name', ''),
                'outcome': decision.get('outcome', {}).get('result', ''),
            })
    
    return sorted(results, key=lambda x: x.get('timestamp', ''), reverse=True)

def find_runbook_gaps(data):
    """Find decisions that deviated from runbooks — these indicate runbook gaps."""
    gaps = defaultdict(list)
    
    for decision in data.get('decisions', []):
        for exc in decision.get('exceptions', []):
            rule = exc.get('rule', 'unknown')
            gaps[rule].append({
                'decision_id': decision.get('id'),
                'deviation': exc.get('deviation', ''),
                'justification': exc.get('justification', ''),
                'outcome': decision.get('outcome', {}).get('result', ''),
            })
    
    return dict(gaps)

# ─── Output Formatting ──────────────────────────────

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_precedent_results(results):
    if not results:
        print("No precedents found.")
        return
    
    for r in results:
        print(f"  [{r['type'].upper()}] {r.get('id', '?')}: {r.get('title', '')}")
        print(f"  Score: {r['score']} | Confidence: {r.get('confidence', 'N/A')}")
        if r.get('recommendation'):
            rec = r['recommendation'][:200]
            print(f"  Recommendation: {rec}...")
        if r.get('outcome'):
            print(f"  Outcome: {r['outcome'][:150]}")
        print()

def print_blast_radius(results):
    entity = results.get('entity')
    if not entity:
        print(f"  Entity not found.")
        return
    
    print(f"  System: {entity.get('name')} ({entity.get('category')})")
    print(f"  Environment: {entity.get('environment')} | Region: {entity.get('region')}")
    
    if results['depends_on']:
        print(f"\n  Depends on:")
        for dep in results['depends_on']:
            if isinstance(dep, dict):
                print(f"    → {dep.get('id')} ({dep.get('type')})")
            else:
                print(f"    → {dep}")
    
    if results['depended_upon_by']:
        print(f"\n  Depended upon by:")
        for dep in results['depended_upon_by']:
            if isinstance(dep, dict):
                print(f"    ← {dep.get('id')} ({dep.get('type')})")
            else:
                print(f"    ← {dep}")
    
    if results['incidents']:
        print(f"\n  Incident History ({len(results['incidents'])}):")
        for inc in results['incidents']:
            print(f"    🔴 {inc['id']}: {inc['title']} ({inc['severity']})")
    
    if results['decisions']:
        print(f"\n  Decision History ({len(results['decisions'])}):")
        for dec in results['decisions']:
            print(f"    ⚡ {dec['id']}: {dec['title']}")

def print_exceptions(results):
    if not results:
        print("No exceptions found.")
        return
    
    print(f"  Found {len(results)} decisions with exceptions:\n")
    for r in results:
        print(f"  {r['id']}: {r['title']}")
        print(f"  Date: {r['timestamp']} | Actor: {r['actor']}")
        for exc in r['exceptions']:
            print(f"    ⚠️  Rule: {exc['rule']}")
            print(f"       Deviation: {exc['deviation']}")
            print(f"       Why: {exc['justification']}")
        print()

def print_runbook_gaps(gaps):
    if not gaps:
        print("No runbook gaps found.")
        return
    
    print(f"  Found {len(gaps)} rules with deviations:\n")
    for rule, deviations in gaps.items():
        print(f"  📖 Rule: {rule}")
        print(f"     Deviations: {len(deviations)}")
        for d in deviations:
            print(f"     - {d['decision_id']}: {d['deviation'][:80]}...")
            print(f"       Why: {d['justification'][:100]}...")
        print()

# ─── Main ────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    args = sys.argv[1:]
    query_type = None
    query_parts = []
    
    # Parse args
    i = 0
    while i < len(args):
        if args[i] == '--type' and i + 1 < len(args):
            query_type = args[i + 1]
            i += 2
        elif args[i] == '--last' and i + 1 < len(args):
            # Parse duration like 30d, 7d
            dur = args[i + 1]
            i += 2
        else:
            query_parts.append(args[i])
            i += 1
    
    query = ' '.join(query_parts)
    data = load_all_graph_data()
    
    print(f"\n🔍 Context Graph Query Engine")
    print(f"   Query: {query or 'all'}")
    print(f"   Type: {query_type or 'general'}")
    print(f"   Graph: {sum(len(v) for v in data.values())} nodes loaded")
    
    if query_type == 'precedents':
        print_section("PRECEDENT SEARCH")
        results = find_precedents(data, query)
        print_precedent_results(results)
    
    elif query_type == 'blast-radius':
        print_section("BLAST RADIUS ANALYSIS")
        results = find_blast_radius(data, query)
        print_blast_radius(results)
    
    elif query_type == 'exceptions':
        print_section("EXCEPTION AUDIT")
        results = find_exceptions(data)
        print_exceptions(results)
    
    elif query_type == 'runbook-gaps':
        print_section("RUNBOOK GAP ANALYSIS")
        gaps = find_runbook_gaps(data)
        print_runbook_gaps(gaps)
    
    elif query_type == 'patterns':
        print_section("BEHAVIORAL PATTERNS")
        for pattern in data.get('patterns', []):
            print(f"  {pattern.get('id')}: {pattern.get('title')}")
            print(f"  Pattern: {pattern.get('pattern', '')[:200]}...")
            print(f"  Implications: {len(pattern.get('implications', []))}")
            print()
    
    elif query_type == 'decisions':
        print_section("DECISION HISTORY")
        for decision in data.get('decisions', []):
            text = json.dumps(decision, default=str).lower()
            if not query or query.lower() in text:
                print(f"  {decision.get('id')}: {decision.get('title')}")
                print(f"  Incident: {decision.get('incident_ref')}")
                print(f"  Decision: {decision.get('decision', '')[:100]}")
                print(f"  AI Reproducible: {decision.get('ai_reproducible', 'N/A')}")
                print()
    
    else:
        # General search
        print_section("GENERAL SEARCH")
        results = search_by_text(data, query)
        
        if not results:
            print("  No results found.")
        else:
            for r in results[:10]:
                node = r['node']
                print(f"  [{r['type'].upper()}] {node.get('id', '?')}: {node.get('title', '')}")
                print(f"  Score: {r['score']} | Matches: {', '.join(r['reasons'][:3])}")
                if r['type'] == 'decisions':
                    print(f"  Outcome: {node.get('outcome', {}).get('result', 'N/A')[:100]}")
                elif r['type'] == 'incidents':
                    print(f"  Severity: {node.get('severity')} | Root cause: {node.get('root_cause', 'N/A')[:80]}")
                print()
    
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
