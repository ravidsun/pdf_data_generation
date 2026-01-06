#!/usr/bin/env python3
"""
Analyze and improve existing Q&A datasets.

This script helps diagnose issues in existing datasets and provides
actionable recommendations for improvement.

Usage:
    python scripts/analyze_dataset.py input.jsonl [--fix output.jsonl]
"""

import argparse
import json
import logging
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    """Load JSONL file."""
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def analyze_question_patterns(data: List[Dict[str, Any]], q_field: str = "question") -> Dict[str, Any]:
    """Analyze question patterns for diversity issues."""
    
    # Question starters
    starters = Counter()
    for item in data:
        q = item.get(q_field, "").lower().strip()
        # Get first 3-4 words
        words = q.split()[:4]
        starter = ' '.join(words)
        starters[starter] += 1
    
    # Question types
    type_patterns = {
        "what_is": r'^what (?:is|are)',
        "what_does": r'^what does',
        "how_does": r'^how does',
        "how_is": r'^how is',
        "how_to": r'^how (?:to|do|can)',
        "why": r'^why',
        "when": r'^when',
        "where": r'^where',
        "which": r'^which',
        "compare": r'^compare|contrast|difference',
        "explain": r'^explain',
        "describe": r'^describe',
        "define": r'^define',
        "analyze": r'^analyze|interpret',
        "predict": r'^predict|forecast',
        "conditional": r'^if |given|suppose',
    }
    
    type_counts = Counter()
    for item in data:
        q = item.get(q_field, "").lower()
        matched = False
        for type_name, pattern in type_patterns.items():
            if re.match(pattern, q):
                type_counts[type_name] += 1
                matched = True
                break
        if not matched:
            type_counts["other"] += 1
    
    # Calculate diversity issues
    total = len(data)
    issues = []
    
    # Check for over-represented patterns
    for pattern, count in type_counts.most_common():
        ratio = count / total
        if ratio > 0.25:
            issues.append(f"HIGH: '{pattern}' is {ratio:.1%} of questions (should be <25%)")
        elif ratio > 0.15:
            issues.append(f"MEDIUM: '{pattern}' is {ratio:.1%} of questions (should be <15%)")
    
    # Check for under-represented patterns
    important_types = ["why", "how_does", "compare", "analyze", "predict", "conditional"]
    for type_name in important_types:
        ratio = type_counts.get(type_name, 0) / total
        if ratio < 0.02:
            issues.append(f"LOW: Need more '{type_name}' questions (currently {ratio:.1%})")
    
    return {
        "top_starters": starters.most_common(15),
        "type_distribution": dict(type_counts),
        "issues": issues,
    }


def analyze_answer_quality(data: List[Dict[str, Any]], a_field: str = "answer") -> Dict[str, Any]:
    """Analyze answer quality."""
    
    lengths = []
    word_counts = []
    short_answers = []
    
    for item in data:
        answer = item.get(a_field, "")
        length = len(answer)
        words = len(answer.split())
        
        lengths.append(length)
        word_counts.append(words)
        
        if words < 15:
            short_answers.append({
                "question": item.get("question", "")[:80],
                "answer": answer[:100],
                "words": words,
            })
    
    return {
        "length_stats": {
            "min": min(lengths),
            "max": max(lengths),
            "avg": sum(lengths) / len(lengths),
        },
        "word_stats": {
            "min": min(word_counts),
            "max": max(word_counts),
            "avg": sum(word_counts) / len(word_counts),
        },
        "short_answer_count": len(short_answers),
        "short_answers_sample": short_answers[:5],
    }


def detect_duplicates(data: List[Dict[str, Any]], q_field: str = "question") -> Dict[str, Any]:
    """Detect exact and near duplicates."""
    
    # Exact duplicates
    question_counts = Counter()
    for item in data:
        q = item.get(q_field, "").lower().strip()
        q_normalized = re.sub(r'\s+', ' ', q)
        question_counts[q_normalized] += 1
    
    exact_duplicates = [(q, c) for q, c in question_counts.items() if c > 1]
    
    # Near duplicates (same first 50 chars)
    prefix_groups = defaultdict(list)
    for i, item in enumerate(data):
        q = item.get(q_field, "").lower().strip()[:50]
        prefix_groups[q].append(i)
    
    near_duplicates = [(prefix, indices) for prefix, indices in prefix_groups.items() if len(indices) > 1]
    
    return {
        "exact_duplicate_count": len(exact_duplicates),
        "exact_duplicates": exact_duplicates[:10],
        "near_duplicate_groups": len(near_duplicates),
        "near_duplicates_sample": near_duplicates[:5],
    }


def check_domain_terms(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Check for Jyotiṣa terminology coverage."""
    
    jyotish_terms = {
        "grahas": ["sūrya", "sun", "candra", "moon", "maṅgala", "mars", "budha", "mercury",
                   "guru", "jupiter", "śukra", "venus", "śani", "saturn", "rāhu", "ketu"],
        "rashis": ["meṣa", "aries", "vṛṣabha", "taurus", "mithuna", "gemini", "karkaṭa", "cancer",
                   "siṃha", "leo", "kanyā", "virgo", "tulā", "libra", "vṛścika", "scorpio",
                   "dhanu", "sagittarius", "makara", "capricorn", "kumbha", "aquarius", "mīna", "pisces"],
        "bhavas": ["lagna", "ascendant", "bhāva", "house"],
        "concepts": ["daśā", "dasha", "yoga", "kāraka", "dṛṣṭi", "aspect", "nakṣatra", 
                     "navāṃśa", "navamsa", "varga", "argalā"],
        "jaimini": ["jaiminī", "sūtra", "ātmakāraka", "svāṃśa", "upapada", "cara", "sthira"],
    }
    
    combined_text = ' '.join(
        (item.get("question", "") + " " + item.get("answer", "")).lower()
        for item in data
    )
    
    coverage = {}
    for category, terms in jyotish_terms.items():
        found = sum(1 for term in terms if term in combined_text)
        coverage[category] = {
            "found": found,
            "total": len(terms),
            "percentage": found / len(terms) * 100,
        }
    
    return coverage


def generate_recommendations(analysis: Dict[str, Any]) -> List[str]:
    """Generate actionable recommendations based on analysis."""
    
    recommendations = []
    
    # Question diversity
    if analysis.get("question_patterns", {}).get("issues"):
        for issue in analysis["question_patterns"]["issues"]:
            if issue.startswith("HIGH"):
                recommendations.append(f"CRITICAL: {issue}")
            elif issue.startswith("MEDIUM"):
                recommendations.append(f"IMPORTANT: {issue}")
            else:
                recommendations.append(f"SUGGESTED: {issue}")
    
    # Answer quality
    answer_stats = analysis.get("answer_quality", {}).get("word_stats", {})
    if answer_stats.get("avg", 0) < 25:
        recommendations.append(
            f"IMPORTANT: Average answer is only {answer_stats['avg']:.0f} words. "
            "Consider regenerating with longer, more detailed answers."
        )
    
    if analysis.get("answer_quality", {}).get("short_answer_count", 0) > len(analysis.get("data", [])) * 0.1:
        recommendations.append(
            "IMPORTANT: More than 10% of answers are too short (<15 words). "
            "Filter or regenerate these."
        )
    
    # Duplicates
    if analysis.get("duplicates", {}).get("exact_duplicate_count", 0) > 0:
        count = analysis["duplicates"]["exact_duplicate_count"]
        recommendations.append(
            f"CRITICAL: Found {count} exact duplicate questions. Remove these."
        )
    
    # Domain coverage
    coverage = analysis.get("domain_coverage", {})
    for category, stats in coverage.items():
        if stats.get("percentage", 100) < 50:
            recommendations.append(
                f"SUGGESTED: Low coverage of {category} terms ({stats['percentage']:.0f}%). "
                "Consider adding more content about this area."
            )
    
    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Analyze Q&A dataset quality")
    parser.add_argument("input", help="Input JSONL file")
    parser.add_argument("--fix", "-f", help="Output fixed dataset to this path")
    parser.add_argument("--q-field", default="question", help="Question field name")
    parser.add_argument("--a-field", default="answer", help="Answer field name")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Load data
    logger.info(f"Loading: {args.input}")
    data = load_jsonl(args.input)
    logger.info(f"Loaded {len(data)} items\n")
    
    # Run analysis
    analysis = {
        "total_items": len(data),
        "question_patterns": analyze_question_patterns(data, args.q_field),
        "answer_quality": analyze_answer_quality(data, args.a_field),
        "duplicates": detect_duplicates(data, args.q_field),
        "domain_coverage": check_domain_terms(data),
    }
    
    # Generate recommendations
    analysis["recommendations"] = generate_recommendations(analysis)
    
    if args.json:
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
        return
    
    # Print report
    print("=" * 60)
    print("VEDIC ASTROLOGY Q&A DATASET ANALYSIS")
    print("=" * 60)
    
    print(f"\nTotal items: {analysis['total_items']}")
    
    # Question patterns
    print("\n" + "-" * 40)
    print("QUESTION PATTERN ANALYSIS")
    print("-" * 40)
    
    print("\nTop 10 question starters:")
    for starter, count in analysis["question_patterns"]["top_starters"][:10]:
        print(f"  '{starter}...': {count} ({count/len(data)*100:.1f}%)")
    
    print("\nQuestion type distribution:")
    for qtype, count in sorted(analysis["question_patterns"]["type_distribution"].items(), key=lambda x: -x[1]):
        print(f"  {qtype}: {count} ({count/len(data)*100:.1f}%)")
    
    # Answer quality
    print("\n" + "-" * 40)
    print("ANSWER QUALITY ANALYSIS")
    print("-" * 40)
    
    ws = analysis["answer_quality"]["word_stats"]
    print(f"\nWord count: min={ws['min']}, max={ws['max']}, avg={ws['avg']:.1f}")
    print(f"Short answers (<15 words): {analysis['answer_quality']['short_answer_count']}")
    
    # Duplicates
    print("\n" + "-" * 40)
    print("DUPLICATE ANALYSIS")
    print("-" * 40)
    
    print(f"\nExact duplicates: {analysis['duplicates']['exact_duplicate_count']}")
    print(f"Near-duplicate groups: {analysis['duplicates']['near_duplicate_groups']}")
    
    # Domain coverage
    print("\n" + "-" * 40)
    print("DOMAIN COVERAGE")
    print("-" * 40)
    
    for category, stats in analysis["domain_coverage"].items():
        print(f"\n{category}: {stats['found']}/{stats['total']} ({stats['percentage']:.0f}%)")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    for rec in analysis["recommendations"]:
        print(f"\n• {rec}")
    
    if not analysis["recommendations"]:
        print("\n✓ Dataset looks good! No critical issues found.")


if __name__ == "__main__":
    main()
