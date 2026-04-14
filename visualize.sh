#!/usr/bin/env bash
# Context Graph Visualizer
# Generates a text-based graph visualization of relationships

set -euo pipefail

GRAPH_DIR="$(cd "$(dirname "$0")" && pwd)/graph"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║         CONTEXT GRAPH — SRE Operations                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Count nodes
INCIDENTS=$(find "$GRAPH_DIR/incidents" -name "*.md" 2>/dev/null | wc -l)
DECISIONS=$(find "$GRAPH_DIR/decisions" -name "*.md" 2>/dev/null | wc -l)
PRECEDENTS=$(find "$GRAPH_DIR/precedents" -name "*.md" 2>/dev/null | wc -l)
ENTITIES=$(find "$GRAPH_DIR/entities" -name "*.md" 2>/dev/null | wc -l)
PATTERNS=$(find "$GRAPH_DIR/patterns" -name "*.md" 2>/dev/null | wc -l)

TOTAL=$((INCIDENTS + DECISIONS + PRECEDENTS + ENTITIES + PATTERNS))

echo "📊 Graph Statistics:"
echo "   Nodes: $TOTAL total"
echo "   ├── Incidents:  $INCIDENTS"
echo "   ├── Decisions:  $DECISIONS"
echo "   ├── Precedents: $PRECEDENTS"
echo "   ├── Entities:   $ENTITIES"
echo "   └── Patterns:   $PATTERNS"
echo ""

# Visualize relationships
echo "🔗 Relationship Map:"
echo ""

for inc_file in "$GRAPH_DIR/incidents"/*.md; do
    [ -f "$inc_file" ] || continue
    inc_id=$(basename "$inc_file" .md)
    inc_title=$(grep -oP 'title:\s*"\K[^"]+' "$inc_file" 2>/dev/null || echo "Unknown")
    inc_severity=$(grep -oP 'severity:\s*\K[A-Z0-9]+' "$inc_file" 2>/dev/null || echo "?")
    
    # Severity emoji
    case "$inc_severity" in
        P1) emoji="🔴" ;;
        P2) emoji="🟠" ;;
        P3) emoji="🟡" ;;
        P4) emoji="🟢" ;;
        *)  emoji="⚪" ;;
    esac
    
    echo "   $emoji $inc_id: $inc_title"
    
    # Find linked decisions
    for dec_file in "$GRAPH_DIR/decisions"/*.md; do
        [ -f "$dec_file" ] || continue
        if grep -q "incident_ref:\s*${inc_id}" "$dec_file" 2>/dev/null; then
            dec_id=$(basename "$dec_file" .md)
            dec_title=$(grep -oP 'title:\s*"\K[^"]+' "$dec_file" 2>/dev/null || echo "Unknown")
            ai_repro=$(grep -oP 'ai_reproducible:\s*\K\w+' "$dec_file" 2>/dev/null || echo "?")
            
            echo "   ├── ⚡ DECISION: $dec_id"
            echo "   │   $dec_title"
            echo "   │   AI Reproducible: $ai_repro"
            
            # Find linked precedents
            for pref in $(grep -oP 'ref:\s*\K[A-Z]+-[0-9]+' "$dec_file" 2>/dev/null | sort -u); do
                echo "   │   ├── 📎 Precedent: $pref"
            done
            
            # Find exceptions
            exc_count=$(grep -c "rule:" "$dec_file" 2>/dev/null || echo "0")
            if [ "$exc_count" -gt "0" ]; then
                echo "   │   └── ⚠️  Exceptions: $exc_count"
            fi
        fi
    done
    
    echo ""
done

# Show precedent chains
echo "📋 Precedent Chains:"
echo ""
for pre_file in "$GRAPH_DIR/precedents"/*.md; do
    [ -f "$pre_file" ] || continue
    pre_id=$(basename "$pre_file" .md)
    pre_title=$(grep -oP 'title:\s*"\K[^"]+' "$pre_file" 2>/dev/null || echo "Unknown")
    pre_confidence=$(grep -oP 'confidence:\s*\K\w+' "$pre_file" 2>/dev/null || echo "?")
    
    echo "   📌 $pre_id: $pre_title"
    echo "      Confidence: $pre_confidence"
    
    # Show evolution
    evo_count=$(grep -c "date:" "$pre_file" 2>/dev/null || echo "0")
    echo "      Evolution: $evo_count stages"
    echo ""
done

# Show patterns
echo "🧠 Behavioral Patterns:"
echo ""
for pat_file in "$GRAPH_DIR/patterns"/*.md; do
    [ -f "$pat_file" ] || continue
    pat_id=$(basename "$pat_file" .md)
    pat_title=$(grep -oP 'title:\s*"\K[^"]+' "$pat_file" 2>/dev/null || echo "Unknown")
    
    echo "   🧩 $pat_id: $pat_title"
done

echo ""
echo "══════════════════════════════════════════════════════════"
echo "Query with: python3 analyze.py \"<search term>\""
echo "══════════════════════════════════════════════════════════"
echo ""
