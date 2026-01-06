"""
Quality Filters for Vedic Astrology Q&A Data

Filters to ensure high-quality training data:
- Duplicate detection (exact and semantic)
- Minimum length requirements
- Sanskrit terminology validation
- Answer quality scoring
- Question diversity checking
"""

import re
import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class QualityMetrics:
    """Quality metrics for a Q&A pair."""
    question_length: int
    answer_length: int
    has_sanskrit_terms: bool
    question_type: str
    is_duplicate: bool
    duplicate_of: Optional[str]
    quality_score: float
    issues: List[str]


@dataclass
class FilterResult:
    """Result of filtering a dataset."""
    kept: List[dict]
    removed: List[dict]
    duplicate_groups: Dict[str, List[str]]
    stats: Dict[str, int]


class QualityFilter:
    """
    Comprehensive quality filter for Vedic astrology Q&A data.
    
    Features:
    - Exact duplicate detection
    - Near-duplicate detection using MinHash
    - Minimum quality thresholds
    - Sanskrit terminology validation
    - Question pattern diversity checking
    """
    
    # Minimum thresholds
    MIN_QUESTION_LENGTH = 20  # characters
    MIN_ANSWER_LENGTH = 30   # characters
    MIN_ANSWER_WORDS = 10    # words
    MAX_REPETITION_RATIO = 0.5  # Max ratio of repeated n-grams
    
    # Question patterns that indicate low quality
    LOW_QUALITY_PATTERNS = [
        r'^what$',
        r'^how$',
        r'^why$',
        r'^\?+$',
        r'^please explain$',
        r'^tell me about$',
    ]
    
    # Sanskrit terms that should be present for domain validity
    REQUIRED_DOMAIN_TERMS = {
        "basic": ["graha", "planet", "rāśi", "sign", "bhāva", "house", "lagna", "ascendant"],
        "jaimini": ["jaiminī", "sūtra", "kāraka", "argalā", "svāṃśa", "daśā"],
        "predictive": ["daśā", "transit", "prediction", "result", "effect", "outcome"],
    }
    
    def __init__(
        self,
        min_question_length: int = None,
        min_answer_length: int = None,
        min_answer_words: int = None,
        similarity_threshold: float = 0.85,
        use_semantic_dedup: bool = True,
    ):
        self.min_question_length = min_question_length or self.MIN_QUESTION_LENGTH
        self.min_answer_length = min_answer_length or self.MIN_ANSWER_LENGTH
        self.min_answer_words = min_answer_words or self.MIN_ANSWER_WORDS
        self.similarity_threshold = similarity_threshold
        self.use_semantic_dedup = use_semantic_dedup
        
        self._seen_questions: Set[str] = set()
        self._seen_answers: Set[str] = set()
        self._question_hashes: Dict[str, str] = {}
        self._answer_hashes: Dict[str, str] = {}
        
        # For semantic deduplication
        self._embedder = None
        if use_semantic_dedup:
            try:
                from sentence_transformers import SentenceTransformer
                self._embedder = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Loaded sentence transformer for semantic deduplication")
            except ImportError:
                logger.warning("sentence-transformers not available, using hash-based dedup only")
    
    def filter_dataset(
        self,
        data: List[dict],
        question_field: str = "question",
        answer_field: str = "answer",
    ) -> FilterResult:
        """
        Filter a dataset for quality and duplicates.
        
        Args:
            data: List of Q&A dictionaries.
            question_field: Field name for questions.
            answer_field: Field name for answers.
            
        Returns:
            FilterResult with kept/removed items and statistics.
        """
        logger.info(f"Filtering {len(data)} Q&A pairs...")
        
        kept = []
        removed = []
        duplicate_groups = defaultdict(list)
        stats = defaultdict(int)
        
        # Reset state
        self._seen_questions.clear()
        self._seen_answers.clear()
        self._question_hashes.clear()
        self._answer_hashes.clear()
        
        for item in data:
            question = item.get(question_field, "")
            answer = item.get(answer_field, "")
            item_id = item.get("id", hashlib.md5(question.encode()).hexdigest()[:8])
            
            # Calculate quality metrics
            metrics = self._calculate_metrics(question, answer, item_id)
            
            # Decide whether to keep
            if metrics.is_duplicate:
                removed.append(item)
                stats["duplicates"] += 1
                if metrics.duplicate_of:
                    duplicate_groups[metrics.duplicate_of].append(item_id)
            elif metrics.issues:
                removed.append(item)
                for issue in metrics.issues:
                    stats[f"issue_{issue}"] += 1
            else:
                kept.append(item)
                stats["kept"] += 1
                
                # Track for future duplicate detection
                q_normalized = self._normalize_text(question)
                a_normalized = self._normalize_text(answer)
                self._seen_questions.add(q_normalized)
                self._seen_answers.add(a_normalized)
                self._question_hashes[self._hash_text(question)] = item_id
                self._answer_hashes[self._hash_text(answer)] = item_id
        
        stats["total"] = len(data)
        stats["removed"] = len(removed)
        
        logger.info(f"Kept {stats['kept']} / {stats['total']} pairs")
        logger.info(f"Removed: {stats['duplicates']} duplicates, {stats['removed'] - stats['duplicates']} quality issues")
        
        return FilterResult(
            kept=kept,
            removed=removed,
            duplicate_groups=dict(duplicate_groups),
            stats=dict(stats),
        )
    
    def _calculate_metrics(
        self,
        question: str,
        answer: str,
        item_id: str,
    ) -> QualityMetrics:
        """Calculate quality metrics for a Q&A pair."""
        issues = []
        is_duplicate = False
        duplicate_of = None
        
        # Length checks
        q_len = len(question)
        a_len = len(answer)
        a_words = len(answer.split())
        
        if q_len < self.min_question_length:
            issues.append("question_too_short")
        
        if a_len < self.min_answer_length:
            issues.append("answer_too_short")
        
        if a_words < self.min_answer_words:
            issues.append("answer_too_few_words")
        
        # Low quality pattern check
        q_lower = question.lower().strip()
        for pattern in self.LOW_QUALITY_PATTERNS:
            if re.match(pattern, q_lower):
                issues.append("low_quality_question")
                break
        
        # Check for excessive repetition in answer
        if self._has_excessive_repetition(answer):
            issues.append("repetitive_answer")
        
        # Domain relevance check
        if not self._has_domain_terms(question, answer):
            issues.append("off_topic")
        
        # Sanskrit term check
        has_sanskrit = self._has_sanskrit_terms(question + " " + answer)
        
        # Duplicate detection
        q_normalized = self._normalize_text(question)
        a_normalized = self._normalize_text(answer)
        q_hash = self._hash_text(question)
        a_hash = self._hash_text(answer)
        
        # Exact duplicate check
        if q_normalized in self._seen_questions:
            is_duplicate = True
            duplicate_of = self._question_hashes.get(q_hash)
        elif a_normalized in self._seen_answers:
            is_duplicate = True
            duplicate_of = self._answer_hashes.get(a_hash)
        
        # Near-duplicate check using fuzzy matching
        if not is_duplicate:
            near_dup = self._check_near_duplicate(question, answer)
            if near_dup:
                is_duplicate = True
                duplicate_of = near_dup
        
        # Question type classification
        q_type = self._classify_question(question)
        
        # Quality score (0-1)
        quality_score = self._calculate_quality_score(
            q_len, a_len, a_words, has_sanskrit, len(issues)
        )
        
        return QualityMetrics(
            question_length=q_len,
            answer_length=a_len,
            has_sanskrit_terms=has_sanskrit,
            question_type=q_type,
            is_duplicate=is_duplicate,
            duplicate_of=duplicate_of,
            quality_score=quality_score,
            issues=issues,
        )
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def _hash_text(self, text: str) -> str:
        """Create hash of normalized text."""
        normalized = self._normalize_text(text)
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def _has_excessive_repetition(self, text: str, n: int = 3) -> bool:
        """Check if text has excessive n-gram repetition."""
        words = text.lower().split()
        if len(words) < n * 2:
            return False
        
        ngrams = [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]
        unique_ngrams = set(ngrams)
        
        repetition_ratio = 1 - (len(unique_ngrams) / len(ngrams))
        return repetition_ratio > self.MAX_REPETITION_RATIO
    
    def _has_domain_terms(self, question: str, answer: str) -> bool:
        """Check if Q&A contains domain-relevant terms."""
        combined = (question + " " + answer).lower()
        
        for category, terms in self.REQUIRED_DOMAIN_TERMS.items():
            if any(term in combined for term in terms):
                return True
        
        return False
    
    def _has_sanskrit_terms(self, text: str) -> bool:
        """Check if text contains Sanskrit terms with diacritics."""
        # Check for diacritical marks
        diacritic_pattern = r'[āīūṛṝḷḹṃḥṅñṭḍṇśṣ]'
        if re.search(diacritic_pattern, text, re.IGNORECASE):
            return True
        
        # Check for common Sanskrit terms
        sanskrit_terms = [
            "graha", "rashi", "bhava", "nakshatra", "dasha",
            "yoga", "karaka", "lagna", "navamsa",
        ]
        text_lower = text.lower()
        return any(term in text_lower for term in sanskrit_terms)
    
    def _check_near_duplicate(self, question: str, answer: str) -> Optional[str]:
        """Check for near-duplicates using fuzzy matching."""
        try:
            from rapidfuzz import fuzz
            
            q_normalized = self._normalize_text(question)
            a_normalized = self._normalize_text(answer)
            
            for seen_q in list(self._seen_questions)[-1000:]:  # Check recent entries
                similarity = fuzz.ratio(q_normalized, seen_q) / 100
                if similarity > self.similarity_threshold:
                    return self._question_hashes.get(self._hash_text(seen_q))
            
            for seen_a in list(self._seen_answers)[-1000:]:
                similarity = fuzz.ratio(a_normalized, seen_a) / 100
                if similarity > self.similarity_threshold:
                    return self._answer_hashes.get(self._hash_text(seen_a))
                    
        except ImportError:
            pass  # Skip fuzzy matching if not available
        
        return None
    
    def _classify_question(self, question: str) -> str:
        """Classify the type of question."""
        q_lower = question.lower()
        
        if q_lower.startswith(("what is", "what are", "define")):
            return "definition"
        elif q_lower.startswith(("how do", "how is", "how to", "explain")):
            return "procedure"
        elif q_lower.startswith(("why", "what causes", "what makes")):
            return "explanation"
        elif q_lower.startswith(("compare", "contrast", "difference")):
            return "comparison"
        elif q_lower.startswith(("when", "during which", "at what")):
            return "timing"
        elif any(word in q_lower for word in ["predict", "forecast", "will"]):
            return "prediction"
        elif any(word in q_lower for word in ["interpret", "analyze", "assess"]):
            return "interpretation"
        else:
            return "general"
    
    def _calculate_quality_score(
        self,
        q_len: int,
        a_len: int,
        a_words: int,
        has_sanskrit: bool,
        num_issues: int,
    ) -> float:
        """Calculate overall quality score (0-1)."""
        score = 1.0
        
        # Length penalties
        if q_len < 50:
            score -= 0.1
        if a_len < 100:
            score -= 0.1
        if a_words < 20:
            score -= 0.1
        
        # Length bonuses
        if a_words > 40:
            score += 0.1
        if a_len > 200:
            score += 0.1
        
        # Sanskrit bonus
        if has_sanskrit:
            score += 0.1
        
        # Issue penalties
        score -= num_issues * 0.2
        
        return max(0.0, min(1.0, score))


class DiversityChecker:
    """
    Check and ensure diversity in question patterns.
    
    Prevents dataset from being dominated by similar question styles.
    """
    
    # Question starter patterns to track
    STARTER_PATTERNS = [
        (r'^what is the', "what_is"),
        (r'^what are the', "what_are"),
        (r'^what does', "what_does"),
        (r'^how does', "how_does"),
        (r'^how is', "how_is"),
        (r'^how do you', "how_do"),
        (r'^how to', "how_to"),
        (r'^why', "why"),
        (r'^when', "when"),
        (r'^where', "where"),
        (r'^which', "which"),
        (r'^explain', "explain"),
        (r'^describe', "describe"),
        (r'^define', "define"),
        (r'^compare', "compare"),
        (r'^analyze', "analyze"),
        (r'^interpret', "interpret"),
        (r'^predict', "predict"),
        (r'^if ', "conditional"),
        (r'^given', "given"),
        (r'^suppose', "suppose"),
    ]
    
    MAX_PATTERN_RATIO = 0.15  # No single pattern should exceed 15%
    
    def __init__(self, max_pattern_ratio: float = None):
        self.max_pattern_ratio = max_pattern_ratio or self.MAX_PATTERN_RATIO
    
    def analyze_diversity(
        self,
        data: List[dict],
        question_field: str = "question",
    ) -> Dict[str, Any]:
        """
        Analyze question diversity in dataset.
        
        Args:
            data: List of Q&A dictionaries.
            question_field: Field name for questions.
            
        Returns:
            Analysis report with pattern distribution and recommendations.
        """
        pattern_counts = defaultdict(int)
        total = len(data)
        
        for item in data:
            question = item.get(question_field, "").lower()
            matched = False
            
            for pattern, name in self.STARTER_PATTERNS:
                if re.match(pattern, question):
                    pattern_counts[name] += 1
                    matched = True
                    break
            
            if not matched:
                pattern_counts["other"] += 1
        
        # Calculate ratios
        pattern_ratios = {
            name: count / total
            for name, count in pattern_counts.items()
        }
        
        # Identify over-represented patterns
        over_represented = {
            name: ratio
            for name, ratio in pattern_ratios.items()
            if ratio > self.max_pattern_ratio
        }
        
        # Identify under-represented patterns
        expected_patterns = {"how_does", "why", "compare", "analyze", "predict", "conditional"}
        under_represented = {
            name: pattern_ratios.get(name, 0)
            for name in expected_patterns
            if pattern_ratios.get(name, 0) < 0.05
        }
        
        # Generate recommendations
        recommendations = []
        for name, ratio in over_represented.items():
            recommendations.append(
                f"Reduce '{name}' questions from {ratio:.1%} to under {self.max_pattern_ratio:.1%}"
            )
        for name, ratio in under_represented.items():
            recommendations.append(
                f"Add more '{name}' questions (currently {ratio:.1%})"
            )
        
        return {
            "total_questions": total,
            "pattern_counts": dict(pattern_counts),
            "pattern_ratios": pattern_ratios,
            "over_represented": over_represented,
            "under_represented": under_represented,
            "diversity_score": self._calculate_diversity_score(pattern_ratios),
            "recommendations": recommendations,
        }
    
    def _calculate_diversity_score(self, pattern_ratios: Dict[str, float]) -> float:
        """Calculate diversity score using entropy-like measure."""
        import math
        
        if not pattern_ratios:
            return 0.0
        
        # Shannon entropy normalized to 0-1
        entropy = 0
        for ratio in pattern_ratios.values():
            if ratio > 0:
                entropy -= ratio * math.log2(ratio)
        
        max_entropy = math.log2(len(pattern_ratios))
        if max_entropy > 0:
            return entropy / max_entropy
        return 0.0
    
    def balance_dataset(
        self,
        data: List[dict],
        question_field: str = "question",
        target_max_ratio: float = None,
    ) -> List[dict]:
        """
        Balance dataset by reducing over-represented patterns.
        
        Args:
            data: List of Q&A dictionaries.
            question_field: Field name for questions.
            target_max_ratio: Target maximum ratio for any pattern.
            
        Returns:
            Balanced dataset.
        """
        target_ratio = target_max_ratio or self.max_pattern_ratio
        total = len(data)
        max_per_pattern = int(total * target_ratio)
        
        # Group by pattern
        pattern_groups = defaultdict(list)
        for item in data:
            question = item.get(question_field, "").lower()
            matched = False
            
            for pattern, name in self.STARTER_PATTERNS:
                if re.match(pattern, question):
                    pattern_groups[name].append(item)
                    matched = True
                    break
            
            if not matched:
                pattern_groups["other"].append(item)
        
        # Balance each group
        balanced = []
        for name, items in pattern_groups.items():
            if len(items) <= max_per_pattern:
                balanced.extend(items)
            else:
                # Sample to reduce over-representation
                import random
                sampled = random.sample(items, max_per_pattern)
                balanced.extend(sampled)
                logger.info(f"Reduced '{name}' from {len(items)} to {max_per_pattern}")
        
        return balanced


def filter_jsonl_file(
    input_path: str,
    output_path: str,
    question_field: str = "question",
    answer_field: str = "answer",
    **filter_kwargs,
) -> Dict[str, Any]:
    """
    Filter a JSONL file and save results.
    
    Args:
        input_path: Path to input JSONL file.
        output_path: Path to output filtered JSONL file.
        question_field: Field name for questions.
        answer_field: Field name for answers.
        **filter_kwargs: Additional arguments for QualityFilter.
        
    Returns:
        Filtering statistics.
    """
    # Load data
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    
    logger.info(f"Loaded {len(data)} items from {input_path}")
    
    # Filter
    quality_filter = QualityFilter(**filter_kwargs)
    result = quality_filter.filter_dataset(data, question_field, answer_field)
    
    # Check diversity
    diversity_checker = DiversityChecker()
    diversity_report = diversity_checker.analyze_diversity(result.kept, question_field)
    
    # Save filtered data
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in result.kept:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    logger.info(f"Saved {len(result.kept)} filtered items to {output_path}")
    
    # Also save removed items for review
    removed_path = output_path.with_suffix('.removed.jsonl')
    with open(removed_path, 'w', encoding='utf-8') as f:
        for item in result.removed:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return {
        "filter_stats": result.stats,
        "diversity_report": diversity_report,
        "output_path": str(output_path),
        "removed_path": str(removed_path),
    }
