"""
Domain-Specific Data Augmentation for Vedic Astrology

Augmentation techniques that understand Jyotiṣa terminology:
- Question paraphrasing with astrological context
- Answer expansion with domain knowledge
- Synonym replacement for Jyotiṣa terms
- Sanskrit/English term variations
"""

import re
import random
import logging
from typing import Dict, List, Optional, Tuple, Any
from copy import deepcopy
from dataclasses import dataclass

from vedic_astro_gen.knowledge_base import GRAHAS, RASHIS, BHAVAS, NAKSHATRAS

logger = logging.getLogger(__name__)


@dataclass
class AugmentedPair:
    """An augmented Q&A pair with metadata."""
    question: str
    answer: str
    original_id: str
    augmentation_type: str
    augmentation_details: str


class VedicAugmenter:
    """
    Domain-aware data augmentation for Vedic astrology Q&A.
    
    Augmentation strategies:
    1. Question paraphrasing using domain templates
    2. Sanskrit/English term swapping
    3. Synonym replacement for astrological terms
    4. Question type transformation
    5. Answer elaboration prompts
    """
    
    # Sanskrit-English term mappings
    SANSKRIT_ENGLISH_MAP = {
        # Grahas
        "sūrya": "Sun",
        "candra": "Moon",
        "maṅgala": "Mars",
        "kuja": "Mars",
        "budha": "Mercury",
        "guru": "Jupiter",
        "bṛhaspati": "Jupiter",
        "śukra": "Venus",
        "śani": "Saturn",
        "rāhu": "Rahu/North Node",
        "ketu": "Ketu/South Node",
        # Rashis
        "meṣa": "Aries",
        "vṛṣabha": "Taurus",
        "mithuna": "Gemini",
        "karkaṭa": "Cancer",
        "siṃha": "Leo",
        "kanyā": "Virgo",
        "tulā": "Libra",
        "vṛścika": "Scorpio",
        "dhanu": "Sagittarius",
        "makara": "Capricorn",
        "kumbha": "Aquarius",
        "mīna": "Pisces",
        # Concepts
        "graha": "planet",
        "rāśi": "sign",
        "bhāva": "house",
        "nakṣatra": "lunar mansion/nakshatra",
        "daśā": "planetary period/dasha",
        "lagna": "ascendant",
        "kāraka": "significator",
        "dṛṣṭi": "aspect",
        "yoga": "combination",
        "svāṃśa": "navamsha position of atmakaraka",
        "argalā": "intervention",
        "upapada": "marriage indicator lagna",
    }
    
    # Create reverse mapping
    ENGLISH_SANSKRIT_MAP = {v.lower(): k for k, v in SANSKRIT_ENGLISH_MAP.items()}
    
    # Question transformation patterns
    QUESTION_TRANSFORMS = {
        "what_is": [
            "Define {term}.",
            "Explain the concept of {term}.",
            "How would you describe {term}?",
            "What do you understand by {term}?",
            "Describe {term} in Vedic astrology.",
        ],
        "how_does": [
            "In what way does {subject} {action}?",
            "Explain how {subject} {action}.",
            "Describe the mechanism by which {subject} {action}.",
            "What is the process through which {subject} {action}?",
        ],
        "what_happens": [
            "What are the effects when {condition}?",
            "Describe the results of {condition}.",
            "What manifests when {condition}?",
            "Explain the outcomes when {condition}.",
        ],
        "interpretation": [
            "How should one interpret {element}?",
            "What does {element} indicate?",
            "Analyze the significance of {element}.",
            "What conclusions can be drawn from {element}?",
        ],
    }
    
    # Astrological synonyms
    ASTRO_SYNONYMS = {
        "effects": ["results", "outcomes", "manifestations", "influences"],
        "indicates": ["signifies", "suggests", "shows", "points to"],
        "native": ["person", "individual", "jatak", "chart owner"],
        "strong": ["powerful", "well-placed", "dignified", "fortified"],
        "weak": ["afflicted", "debilitated", "troubled", "challenged"],
        "benefic": ["favorable", "auspicious", "positive", "supportive"],
        "malefic": ["unfavorable", "challenging", "negative", "troublesome"],
        "house": ["bhāva", "place", "domain", "sector"],
        "sign": ["rāśi", "zodiac sign"],
        "aspect": ["dṛṣṭi", "glance", "influence"],
        "period": ["daśā", "time cycle", "planetary period"],
        "conjunction": ["yuti", "combination", "union"],
        "placed": ["posited", "situated", "located", "positioned"],
    }
    
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        
    def augment_pair(
        self,
        question: str,
        answer: str,
        original_id: str,
        num_augmentations: int = 2,
        methods: Optional[List[str]] = None,
    ) -> List[AugmentedPair]:
        """
        Generate augmented versions of a Q&A pair.
        
        Args:
            question: Original question.
            answer: Original answer.
            original_id: ID of original pair.
            num_augmentations: Number of augmented versions to create.
            methods: Specific augmentation methods to use.
            
        Returns:
            List of AugmentedPair objects.
        """
        if methods is None:
            methods = ["term_swap", "synonym", "paraphrase", "question_transform"]
        
        augmented = []
        used_questions = {question.lower()}
        
        for method in methods:
            if len(augmented) >= num_augmentations:
                break
            
            try:
                if method == "term_swap":
                    result = self._augment_term_swap(question, answer, original_id)
                elif method == "synonym":
                    result = self._augment_synonym(question, answer, original_id)
                elif method == "paraphrase":
                    result = self._augment_paraphrase(question, answer, original_id)
                elif method == "question_transform":
                    result = self._augment_question_transform(question, answer, original_id)
                else:
                    continue
                
                if result and result.question.lower() not in used_questions:
                    augmented.append(result)
                    used_questions.add(result.question.lower())
                    
            except Exception as e:
                logger.debug(f"Augmentation method {method} failed: {e}")
        
        return augmented
    
    def _augment_term_swap(
        self,
        question: str,
        answer: str,
        original_id: str,
    ) -> Optional[AugmentedPair]:
        """Swap Sanskrit terms with English or vice versa."""
        new_question = question
        new_answer = answer
        swapped_terms = []
        
        # Decide direction: Sanskrit to English or English to Sanskrit
        if self.rng.random() < 0.5:
            # Sanskrit to English
            for sanskrit, english in self.SANSKRIT_ENGLISH_MAP.items():
                if sanskrit.lower() in question.lower():
                    new_question = re.sub(
                        rf'\b{re.escape(sanskrit)}\b',
                        english,
                        new_question,
                        flags=re.IGNORECASE,
                    )
                    swapped_terms.append(f"{sanskrit}→{english}")
                    break
        else:
            # English to Sanskrit (use first word of English term)
            for english, sanskrit in self.ENGLISH_SANSKRIT_MAP.items():
                english_first = english.split('/')[0].split()[0]
                if english_first.lower() in question.lower():
                    new_question = re.sub(
                        rf'\b{re.escape(english_first)}\b',
                        sanskrit.capitalize(),
                        new_question,
                        flags=re.IGNORECASE,
                    )
                    swapped_terms.append(f"{english_first}→{sanskrit}")
                    break
        
        if not swapped_terms or new_question == question:
            return None
        
        return AugmentedPair(
            question=new_question,
            answer=new_answer,
            original_id=original_id,
            augmentation_type="term_swap",
            augmentation_details=", ".join(swapped_terms),
        )
    
    def _augment_synonym(
        self,
        question: str,
        answer: str,
        original_id: str,
    ) -> Optional[AugmentedPair]:
        """Replace words with astrological synonyms."""
        new_question = question
        new_answer = answer
        replaced_terms = []
        
        for word, synonyms in self.ASTRO_SYNONYMS.items():
            if word.lower() in question.lower():
                synonym = self.rng.choice(synonyms)
                new_question = re.sub(
                    rf'\b{re.escape(word)}\b',
                    synonym,
                    new_question,
                    flags=re.IGNORECASE,
                )
                replaced_terms.append(f"{word}→{synonym}")
                break  # Only one replacement per augmentation
        
        if not replaced_terms or new_question == question:
            return None
        
        return AugmentedPair(
            question=new_question,
            answer=new_answer,
            original_id=original_id,
            augmentation_type="synonym",
            augmentation_details=", ".join(replaced_terms),
        )
    
    def _augment_paraphrase(
        self,
        question: str,
        answer: str,
        original_id: str,
    ) -> Optional[AugmentedPair]:
        """Paraphrase question using templates."""
        q_lower = question.lower()
        
        # Detect question type and extract components
        if "what is" in q_lower or "what are" in q_lower:
            # Extract the term being asked about
            match = re.search(r'what (?:is|are) (?:the )?(.+?)[\?\.]?$', q_lower)
            if match:
                term = match.group(1).strip()
                templates = self.QUESTION_TRANSFORMS["what_is"]
                new_question = self.rng.choice(templates).format(term=term)
                
                return AugmentedPair(
                    question=new_question,
                    answer=answer,
                    original_id=original_id,
                    augmentation_type="paraphrase",
                    augmentation_details="what_is pattern",
                )
        
        elif "how does" in q_lower or "how do" in q_lower:
            # Extract subject and action
            match = re.search(r'how (?:does|do) (.+?) (.+?)[\?\.]?$', q_lower)
            if match:
                subject = match.group(1).strip()
                action = match.group(2).strip()
                templates = self.QUESTION_TRANSFORMS["how_does"]
                new_question = self.rng.choice(templates).format(
                    subject=subject, action=action
                )
                
                return AugmentedPair(
                    question=new_question,
                    answer=answer,
                    original_id=original_id,
                    augmentation_type="paraphrase",
                    augmentation_details="how_does pattern",
                )
        
        elif "interpret" in q_lower or "analyze" in q_lower:
            match = re.search(r'(?:interpret|analyze) (.+?)[\?\.]?$', q_lower)
            if match:
                element = match.group(1).strip()
                templates = self.QUESTION_TRANSFORMS["interpretation"]
                new_question = self.rng.choice(templates).format(element=element)
                
                return AugmentedPair(
                    question=new_question,
                    answer=answer,
                    original_id=original_id,
                    augmentation_type="paraphrase",
                    augmentation_details="interpretation pattern",
                )
        
        return None
    
    def _augment_question_transform(
        self,
        question: str,
        answer: str,
        original_id: str,
    ) -> Optional[AugmentedPair]:
        """Transform question structure."""
        q_lower = question.lower()
        
        # Transform "What is X" to "Explain X"
        if q_lower.startswith("what is "):
            content = question[8:].strip().rstrip("?.")
            transforms = [
                f"Explain {content}.",
                f"Describe {content}.",
                f"Define {content} in Jyotiṣa.",
                f"How is {content} understood in Vedic astrology?",
            ]
            new_question = self.rng.choice(transforms)
            
            return AugmentedPair(
                question=new_question,
                answer=answer,
                original_id=original_id,
                augmentation_type="question_transform",
                augmentation_details="what_is → explain",
            )
        
        # Transform "How does X" to "Explain how X"
        if q_lower.startswith("how does "):
            content = question[9:].strip().rstrip("?.")
            transforms = [
                f"Explain how {content}.",
                f"Describe the way {content}.",
                f"In what manner does {content}?",
            ]
            new_question = self.rng.choice(transforms)
            
            return AugmentedPair(
                question=new_question,
                answer=answer,
                original_id=original_id,
                augmentation_type="question_transform",
                augmentation_details="how_does → explain",
            )
        
        return None
    
    def augment_dataset(
        self,
        data: List[dict],
        question_field: str = "question",
        answer_field: str = "answer",
        id_field: str = "id",
        augmentations_per_item: int = 2,
        include_original: bool = True,
    ) -> List[dict]:
        """
        Augment an entire dataset.
        
        Args:
            data: List of Q&A dictionaries.
            question_field: Field name for questions.
            answer_field: Field name for answers.
            id_field: Field name for IDs.
            augmentations_per_item: Number of augmentations per original.
            include_original: Whether to include original items.
            
        Returns:
            Augmented dataset.
        """
        augmented_data = []
        
        if include_original:
            augmented_data.extend(deepcopy(data))
        
        for item in data:
            question = item.get(question_field, "")
            answer = item.get(answer_field, "")
            item_id = item.get(id_field, str(id(item)))
            
            augmented_pairs = self.augment_pair(
                question=question,
                answer=answer,
                original_id=item_id,
                num_augmentations=augmentations_per_item,
            )
            
            for aug_pair in augmented_pairs:
                new_item = deepcopy(item)
                new_item[question_field] = aug_pair.question
                new_item[answer_field] = aug_pair.answer
                new_item[id_field] = f"{item_id}_aug_{aug_pair.augmentation_type}"
                new_item["augmentation"] = {
                    "type": aug_pair.augmentation_type,
                    "details": aug_pair.augmentation_details,
                    "original_id": aug_pair.original_id,
                }
                augmented_data.append(new_item)
        
        logger.info(
            f"Augmented {len(data)} items to {len(augmented_data)} "
            f"(+{len(augmented_data) - len(data)} augmented)"
        )
        
        return augmented_data


class AnswerEnhancer:
    """
    Enhance answers with additional domain context.
    
    Adds relevant information based on detected entities.
    """
    
    def __init__(self):
        self.graha_info = GRAHAS
        self.rashi_info = RASHIS
        self.bhava_info = BHAVAS
    
    def enhance_answer(
        self,
        answer: str,
        question: str,
        max_addition: int = 100,
    ) -> str:
        """
        Enhance an answer with additional context if it's too short.
        
        Args:
            answer: Original answer.
            question: Related question (for context).
            max_addition: Maximum characters to add.
            
        Returns:
            Enhanced answer.
        """
        if len(answer) > 200:
            return answer  # Already long enough
        
        # Detect entities in Q&A
        entities = self._detect_entities(question + " " + answer)
        
        if not entities:
            return answer
        
        # Add relevant context
        additions = []
        
        for entity_type, entity_name in entities:
            if entity_type == "graha":
                info = self.graha_info.get(entity_name)
                if info:
                    additions.append(self._get_graha_context(info))
            elif entity_type == "rashi":
                info = self.rashi_info.get(entity_name)
                if info:
                    additions.append(self._get_rashi_context(info))
            elif entity_type == "bhava":
                info = self.bhava_info.get(entity_name)
                if info:
                    additions.append(self._get_bhava_context(info))
            
            if len(' '.join(additions)) > max_addition:
                break
        
        if additions:
            return answer + " " + ' '.join(additions)
        
        return answer
    
    def _detect_entities(self, text: str) -> List[Tuple[str, Any]]:
        """Detect astrological entities in text."""
        entities = []
        text_lower = text.lower()
        
        # Check for grahas
        for graha_key in self.graha_info:
            if graha_key in text_lower:
                entities.append(("graha", graha_key))
        
        # Check for rashis
        for rashi_key in self.rashi_info:
            if rashi_key in text_lower:
                entities.append(("rashi", rashi_key))
        
        # Check for bhavas (houses)
        for bhava_num in self.bhava_info:
            ordinal = self._ordinal(bhava_num)
            if f"{ordinal} house" in text_lower or f"{bhava_num}h" in text_lower:
                entities.append(("bhava", bhava_num))
        
        return entities
    
    def _get_graha_context(self, info: dict) -> str:
        """Get brief context about a graha."""
        nature = info.get("nature", "")
        significations = info.get("significations", [])[:3]
        return f"{info['sanskrit']} ({info['english']}) is a {nature} that signifies {', '.join(significations)}."
    
    def _get_rashi_context(self, info: dict) -> str:
        """Get brief context about a rashi."""
        return f"{info['sanskrit']} is a {info['element']} sign of {info['quality']} quality, ruled by {info['lord']}."
    
    def _get_bhava_context(self, info: dict) -> str:
        """Get brief context about a bhava."""
        significations = info.get("significations", [])[:3]
        return f"The {info['name']} signifies {', '.join(significations)}."
    
    def _ordinal(self, n: int) -> str:
        """Convert number to ordinal."""
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = suffixes.get(n % 10, 'th')
        return f"{n}{suffix}"


def augment_jsonl_file(
    input_path: str,
    output_path: str,
    augmentations_per_item: int = 2,
    question_field: str = "question",
    answer_field: str = "answer",
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Augment a JSONL file.
    
    Args:
        input_path: Path to input JSONL.
        output_path: Path to output JSONL.
        augmentations_per_item: Augmentations per original item.
        question_field: Field name for questions.
        answer_field: Field name for answers.
        seed: Random seed.
        
    Returns:
        Statistics about augmentation.
    """
    import json
    from pathlib import Path
    
    # Load data
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    
    logger.info(f"Loaded {len(data)} items from {input_path}")
    
    # Augment
    augmenter = VedicAugmenter(seed=seed)
    augmented = augmenter.augment_dataset(
        data,
        question_field=question_field,
        answer_field=answer_field,
        augmentations_per_item=augmentations_per_item,
    )
    
    # Save
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in augmented:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    logger.info(f"Saved {len(augmented)} items to {output_path}")
    
    return {
        "original_count": len(data),
        "augmented_count": len(augmented),
        "added_count": len(augmented) - len(data),
        "output_path": str(output_path),
    }
