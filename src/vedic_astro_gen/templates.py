"""
Question Templates for Vedic Astrology Q&A Generation

Provides diverse question patterns to avoid repetitive "What is..." style questions.
Templates are organized by prediction category and question type.
"""

import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from vedic_astro_gen.knowledge_base import (
    GRAHAS, RASHIS, BHAVAS, NAKSHATRAS, YOGAS,
    PREDICTION_TEMPLATES, PredictionCategory
)


@dataclass
class QuestionTemplate:
    """A question template with metadata."""
    template: str
    answer_guidance: str
    qa_type: str
    difficulty: str
    requires_context: bool = False
    category: Optional[str] = None


# =============================================================================
# DIVERSE QUESTION PATTERNS
# Avoiding repetitive "What is/are/does" patterns
# =============================================================================

QUESTION_STARTERS = {
    "definition": [
        "Define {term} in Jyotiṣa.",
        "Explain the concept of {term}.",
        "How is {term} understood in Vedic astrology?",
        "Describe {term} and its significance.",
        "What role does {term} play in chart analysis?",
        "Elaborate on {term} as used in Jyotiṣa.",
    ],
    "interpretation": [
        "How should one interpret {condition}?",
        "Analyze the effects of {condition}.",
        "What results manifest when {condition}?",
        "Describe the implications of {condition}.",
        "How does {condition} influence the native?",
        "Explain the astrological significance of {condition}.",
        "What predictions can be made from {condition}?",
    ],
    "comparison": [
        "Compare {item1} and {item2} in terms of {aspect}.",
        "How do {item1} and {item2} differ in their effects?",
        "Contrast the significations of {item1} versus {item2}.",
        "What distinguishes {item1} from {item2}?",
        "Between {item1} and {item2}, which is stronger for {purpose}?",
    ],
    "timing": [
        "When does {event} typically occur based on {factors}?",
        "How to time {event} using daśā analysis?",
        "During which planetary period does {event} manifest?",
        "What transit triggers {event}?",
        "At what age might {event} occur given {condition}?",
    ],
    "prediction": [
        "Predict the outcome when {condition} is present.",
        "What can be expected during {period} for {matter}?",
        "How will {planet} daśā affect {area_of_life}?",
        "Forecast {area_of_life} based on {indicators}.",
        "What are the likely results of {combination}?",
    ],
    "procedure": [
        "How do you calculate {calculation}?",
        "Explain the steps to determine {determination}.",
        "What is the method for finding {finding}?",
        "Describe the procedure to assess {assessment}.",
        "Walk through the process of analyzing {analysis}.",
    ],
    "application": [
        "Apply {principle} to analyze {situation}.",
        "Using {technique}, evaluate {chart_element}.",
        "How would you use {method} for {purpose}?",
        "Demonstrate {concept} with a practical example.",
        "In practice, how is {rule} applied?",
    ],
    "conditional": [
        "If {condition1}, what happens to {outcome}?",
        "When {condition1} combines with {condition2}, what results?",
        "Given {scenario}, how would {aspect} be affected?",
        "Suppose {condition} — what predictions follow?",
        "In the case of {situation}, how does {factor} influence the result?",
    ],
    "why": [
        "Why does {planet} give {result} in {position}?",
        "What is the reason {combination} produces {effect}?",
        "Explain why {condition} leads to {outcome}.",
        "What makes {placement} significant for {matter}?",
        "Why is {factor} important in assessing {area}?",
    ],
    "remedial": [
        "What remedies help when {affliction} is present?",
        "How can one mitigate the effects of {malefic_condition}?",
        "Suggest upāyas for {problem}.",
        "What gemstone or mantra helps with {planetary_issue}?",
        "How to strengthen a weak {planet}?",
    ],
}


# =============================================================================
# GRAHA (PLANET) TEMPLATES
# =============================================================================

GRAHA_TEMPLATES = {
    "basic": [
        QuestionTemplate(
            template="Describe the nature and significations of {graha_sanskrit} ({graha_english}).",
            answer_guidance="Include: nature (benefic/malefic), element, guna, primary significations, body parts, diseases, karakatva",
            qa_type="definition",
            difficulty="easy",
        ),
        QuestionTemplate(
            template="What does {graha_sanskrit} represent as a kāraka in Vedic astrology?",
            answer_guidance="Focus on karakatva - primary, relationships, profession significations",
            qa_type="concept",
            difficulty="easy",
        ),
        QuestionTemplate(
            template="List the friends, enemies, and neutral planets for {graha_sanskrit}.",
            answer_guidance="Provide natural relationships: friends, enemies, neutral planets",
            qa_type="definition",
            difficulty="easy",
        ),
    ],
    "placement": [
        QuestionTemplate(
            template="Interpret {graha_sanskrit} placed in the {bhava_ordinal} house ({bhava_name}).",
            answer_guidance="Combine graha significations with bhava significations, give practical results",
            qa_type="interpretation",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="How does {graha_sanskrit} behave when placed in {rashi_sanskrit} ({rashi_english})?",
            answer_guidance="Consider dignity (exaltation/debilitation/own/friend/enemy), element compatibility, specific results",
            qa_type="interpretation",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="What career indications arise from {graha_sanskrit} in the 10th house?",
            answer_guidance="Link graha's profession significations with 10th house career themes",
            qa_type="prediction",
            difficulty="medium",
            category="career",
        ),
        QuestionTemplate(
            template="Analyze {graha_sanskrit} as the 7th lord in the {bhava_ordinal} house for marriage.",
            answer_guidance="Assess marriage timing, spouse nature, marital harmony based on placement",
            qa_type="interpretation",
            difficulty="hard",
            category="marriage",
        ),
    ],
    "dignity": [
        QuestionTemplate(
            template="Explain the effects of exalted {graha_sanskrit} in a birth chart.",
            answer_guidance="Include: exaltation sign, degree, enhanced positive significations, potential issues from over-strength",
            qa_type="interpretation",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="What happens when {graha_sanskrit} is debilitated? Can it give good results?",
            answer_guidance="Debilitation sign, degree, neecha bhanga conditions, contextual analysis",
            qa_type="interpretation",
            difficulty="hard",
        ),
        QuestionTemplate(
            template="Compare {graha_sanskrit} in its own sign versus its exaltation sign.",
            answer_guidance="Contrast svakshetra vs uccha effects, which is stronger for what purposes",
            qa_type="comparison",
            difficulty="hard",
        ),
    ],
    "dasha": [
        QuestionTemplate(
            template="What general results occur during {graha_sanskrit} Mahādaśā?",
            answer_guidance="Include: dasha duration, general themes, what areas of life are activated",
            qa_type="prediction",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="How does {graha_sanskrit} Mahādaśā affect career prospects?",
            answer_guidance="Link graha nature to career changes, promotions, or challenges during its period",
            qa_type="prediction",
            difficulty="medium",
            category="career",
        ),
        QuestionTemplate(
            template="Predict health during {graha_sanskrit} Mahādaśā based on its significations.",
            answer_guidance="Connect graha's body parts and diseases to potential health issues during its period",
            qa_type="prediction",
            difficulty="hard",
            category="health",
        ),
        QuestionTemplate(
            template="When {graha_sanskrit} is the daśā lord and also the 7th lord, what marriage events occur?",
            answer_guidance="Timing of marriage, spouse-related events during this dasha",
            qa_type="prediction",
            difficulty="hard",
            category="marriage",
        ),
    ],
    "aspects": [
        QuestionTemplate(
            template="Which houses does {graha_sanskrit} aspect and what is the significance of each aspect?",
            answer_guidance="List aspects (7th for all, special for Mars/Jupiter/Saturn), describe what each aspect does",
            qa_type="rule",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="How does {graha1_sanskrit}'s aspect on {graha2_sanskrit} modify the latter's results?",
            answer_guidance="Benefic/malefic influence, enhancement or affliction, specific combinations",
            qa_type="interpretation",
            difficulty="hard",
        ),
    ],
    "conjunction": [
        QuestionTemplate(
            template="Analyze the conjunction of {graha1_sanskrit} and {graha2_sanskrit}.",
            answer_guidance="Natural relationship, combined significations, yoga formation if any, practical results",
            qa_type="interpretation",
            difficulty="hard",
        ),
        QuestionTemplate(
            template="When {graha1_sanskrit} and {graha2_sanskrit} are conjunct in the {bhava_ordinal} house, what manifests?",
            answer_guidance="Combine both grahas' natures with bhava significations for specific predictions",
            qa_type="interpretation",
            difficulty="hard",
        ),
    ],
}


# =============================================================================
# BHAVA (HOUSE) TEMPLATES  
# =============================================================================

BHAVA_TEMPLATES = {
    "basic": [
        QuestionTemplate(
            template="What are the primary significations of the {bhava_ordinal} house ({bhava_name})?",
            answer_guidance="List all major significations, karaka, natural sign, category",
            qa_type="definition",
            difficulty="easy",
        ),
        QuestionTemplate(
            template="Which planet is the natural significator (kāraka) of the {bhava_ordinal} house?",
            answer_guidance="Name the karaka and explain why it signifies this house",
            qa_type="definition",
            difficulty="easy",
        ),
    ],
    "lordship": [
        QuestionTemplate(
            template="How to analyze the {bhava_ordinal} lord's placement for predictions?",
            answer_guidance="Explain house lord analysis methodology, what to look for",
            qa_type="procedure",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="When the {bhava_ordinal} lord is in the {target_bhava_ordinal} house, what results?",
            answer_guidance="Combine source house themes going to target house, practical predictions",
            qa_type="interpretation",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="The {bhava_ordinal} lord is debilitated. How does this affect {prediction_area}?",
            answer_guidance="Explain weakened house matters, timing of difficulties, remedial considerations",
            qa_type="prediction",
            difficulty="hard",
        ),
    ],
    "prediction_areas": [
        QuestionTemplate(
            template="Using the {bhava_ordinal} house, how do you predict {prediction_area}?",
            answer_guidance="Step-by-step analysis: sign, lord, planets in house, aspects, karaka",
            qa_type="procedure",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="What factors in the {bhava_ordinal} house indicate success in {prediction_area}?",
            answer_guidance="Benefic placements, strong lord, positive aspects, yoga formations",
            qa_type="interpretation",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="What combinations in the {bhava_ordinal} house cause problems for {prediction_area}?",
            answer_guidance="Malefic influences, weak lord, negative aspects, dosha formations",
            qa_type="interpretation",
            difficulty="medium",
        ),
    ],
}


# =============================================================================
# RASHI (SIGN) TEMPLATES
# =============================================================================

RASHI_TEMPLATES = {
    "basic": [
        QuestionTemplate(
            template="Describe the characteristics of {rashi_sanskrit} ({rashi_english}) rāśi.",
            answer_guidance="Element, quality, lord, gender, direction, nature, key traits",
            qa_type="definition",
            difficulty="easy",
        ),
        QuestionTemplate(
            template="What body part is associated with {rashi_sanskrit} and how is this used in medical astrology?",
            answer_guidance="Body part, related health issues, diagnostic applications",
            qa_type="concept",
            difficulty="medium",
        ),
    ],
    "lagna": [
        QuestionTemplate(
            template="What are the personality traits of a {rashi_sanskrit} ascendant native?",
            answer_guidance="Physical appearance, personality, strengths, weaknesses, life themes",
            qa_type="interpretation",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="For {rashi_sanskrit} Lagna, which planets are functional benefics and malefics?",
            answer_guidance="List benefics (trikona lords), malefics (trik lords), neutrals based on lordship",
            qa_type="rule",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="What career suits a {rashi_sanskrit} ascendant based on the 10th house lord?",
            answer_guidance="Identify 10th house sign, its lord, suitable professions",
            qa_type="prediction",
            difficulty="medium",
            category="career",
        ),
    ],
}


# =============================================================================
# YOGA (COMBINATION) TEMPLATES
# =============================================================================

YOGA_TEMPLATES = {
    "definition": [
        QuestionTemplate(
            template="Define {yoga_name} and explain how it forms.",
            answer_guidance="Formation conditions, planets involved, requirements",
            qa_type="definition",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="What are the effects of {yoga_name} when fully formed?",
            answer_guidance="Positive/negative results, areas of life affected, strength variations",
            qa_type="interpretation",
            difficulty="medium",
        ),
    ],
    "application": [
        QuestionTemplate(
            template="How do you verify if {yoga_name} is actually present and strong in a chart?",
            answer_guidance="Verification steps, strength assessment, cancellation factors",
            qa_type="procedure",
            difficulty="hard",
        ),
        QuestionTemplate(
            template="During which daśā period does {yoga_name} give its results?",
            answer_guidance="Which planet's dasha activates the yoga, timing principles",
            qa_type="prediction",
            difficulty="hard",
        ),
        QuestionTemplate(
            template="Can {yoga_name} be cancelled? If so, how?",
            answer_guidance="Cancellation conditions, bhanga yogas, mitigating factors",
            qa_type="rule",
            difficulty="hard",
        ),
    ],
}


# =============================================================================
# TIMING & PREDICTION TEMPLATES
# =============================================================================

TIMING_TEMPLATES = {
    "dasha": [
        QuestionTemplate(
            template="How to predict {event} using Vimśottarī Daśā?",
            answer_guidance="Which dasha lords to check, bhukti combinations, triggering factors",
            qa_type="procedure",
            difficulty="hard",
            category="{category}",
        ),
        QuestionTemplate(
            template="When will {event} happen if the relevant house lord is in {placement}?",
            answer_guidance="Dasha timing, transit triggers, age calculation",
            qa_type="prediction",
            difficulty="hard",
            category="{category}",
        ),
    ],
    "transit": [
        QuestionTemplate(
            template="How does {graha_sanskrit} transit over the natal {bhava_ordinal} house affect {area}?",
            answer_guidance="Transit duration, effects, whether benefic or challenging",
            qa_type="prediction",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="What happens when transiting Saturn aspects natal {graha_sanskrit}?",
            answer_guidance="Saḍe-sātī like effects, duration, what life areas are challenged",
            qa_type="prediction",
            difficulty="hard",
        ),
    ],
}


# =============================================================================
# JAIMINI SPECIFIC TEMPLATES
# =============================================================================

JAIMINI_TEMPLATES = {
    "karaka": [
        QuestionTemplate(
            template="How is the Ātmakāraka determined and what does it signify?",
            answer_guidance="Calculation method (highest degree), significance for soul's purpose",
            qa_type="procedure",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="Explain the role of {karaka_name} in Jaiminī astrology.",
            answer_guidance="Which planet becomes this karaka, what it signifies, prediction applications",
            qa_type="concept",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="How does the placement of Ātmakāraka in the Navāṃśa (Svāṃśa) indicate spirituality?",
            answer_guidance="Svamsha analysis, spiritual path indicators, moksha considerations",
            qa_type="interpretation",
            difficulty="hard",
        ),
    ],
    "dasha": [
        QuestionTemplate(
            template="Explain Cara Daśā calculation and its application.",
            answer_guidance="Starting point, direction, duration calculation, usage",
            qa_type="procedure",
            difficulty="hard",
        ),
        QuestionTemplate(
            template="How does Nārāyaṇa Daśā differ from Cara Daśā in application?",
            answer_guidance="Different purposes, calculation differences, when to use which",
            qa_type="comparison",
            difficulty="hard",
        ),
    ],
    "aspects": [
        QuestionTemplate(
            template="How do Rāśi Dṛṣṭi (sign aspects) work in Jaiminī system?",
            answer_guidance="Sign-based aspects, dual/movable/fixed sign aspect rules",
            qa_type="rule",
            difficulty="medium",
        ),
        QuestionTemplate(
            template="Explain Argalā and its role in chart interpretation.",
            answer_guidance="Definition, which houses create argala, obstruction (virodhargala)",
            qa_type="concept",
            difficulty="medium",
        ),
    ],
}


# =============================================================================
# PREDICTIVE SCENARIO TEMPLATES
# =============================================================================

SCENARIO_TEMPLATES = {
    "career": [
        QuestionTemplate(
            template="A native has {graha1} in 10th house and {graha2} aspecting it. Predict career.",
            answer_guidance="Combine both planet significations, profession type, success level",
            qa_type="prediction",
            difficulty="hard",
            category="career",
            requires_context=True,
        ),
        QuestionTemplate(
            template="The 10th lord is in the 12th house. Will the native work abroad?",
            answer_guidance="12th house = foreign lands, analyze 10th lord strength, supporting factors",
            qa_type="prediction",
            difficulty="medium",
            category="career",
        ),
        QuestionTemplate(
            template="Saturn is in the 10th house for a {rashi_sanskrit} ascendant. Analyze career prospects.",
            answer_guidance="Saturn's functional nature for this lagna, delays, eventual success",
            qa_type="interpretation",
            difficulty="hard",
            category="career",
        ),
    ],
    "marriage": [
        QuestionTemplate(
            template="The 7th house has no planets but its lord is exalted. How is the marriage?",
            answer_guidance="Empty house + strong lord analysis, spouse quality, timing",
            qa_type="prediction",
            difficulty="medium",
            category="marriage",
        ),
        QuestionTemplate(
            template="Venus is combust in the 7th house. What does this indicate for marriage?",
            answer_guidance="Combustion effects on marriage karaka, remedies, spouse characteristics",
            qa_type="interpretation",
            difficulty="hard",
            category="marriage",
        ),
        QuestionTemplate(
            template="Both malefics (Saturn and Mars) aspect the 7th house. Will marriage be delayed?",
            answer_guidance="Double malefic influence, delay factors, timing after obstacles clear",
            qa_type="prediction",
            difficulty="hard",
            category="marriage",
        ),
    ],
    "health": [
        QuestionTemplate(
            template="The Lagna lord is in the 6th house and afflicted. What health issues arise?",
            answer_guidance="6th house diseases, lagna lord = vitality, specific ailments based on planets",
            qa_type="prediction",
            difficulty="hard",
            category="health",
        ),
        QuestionTemplate(
            template="Moon is in Scorpio aspected by Saturn. Analyze mental health implications.",
            answer_guidance="Moon = mind, Scorpio = intensity, Saturn = depression/anxiety patterns",
            qa_type="interpretation",
            difficulty="hard",
            category="health",
        ),
    ],
    "wealth": [
        QuestionTemplate(
            template="Jupiter aspects both the 2nd and 11th houses. What are the wealth prospects?",
            answer_guidance="Jupiter as wealth giver, double wealth house aspect, abundance indicators",
            qa_type="prediction",
            difficulty="medium",
            category="wealth",
        ),
        QuestionTemplate(
            template="The 2nd lord is in the 8th house. Is this good or bad for wealth?",
            answer_guidance="8th house inheritance angle, 2nd-8th axis, sudden gains vs losses",
            qa_type="interpretation",
            difficulty="hard",
            category="wealth",
        ),
    ],
    "children": [
        QuestionTemplate(
            template="Jupiter is retrograde in the 5th house. How does this affect children?",
            answer_guidance="Retrograde effects, delayed but eventual results, quality of children",
            qa_type="prediction",
            difficulty="medium",
            category="children",
        ),
        QuestionTemplate(
            template="The 5th house has Ketu. Will the native have children?",
            answer_guidance="Ketu's detachment effect, conditions for children, adoption possibilities",
            qa_type="prediction",
            difficulty="hard",
            category="children",
        ),
    ],
}


# =============================================================================
# TEMPLATE SELECTION AND GENERATION
# =============================================================================

class TemplateManager:
    """Manages question templates and generates diverse Q&A pairs."""
    
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.used_templates = set()
        
    def get_random_starter(self, qa_type: str) -> str:
        """Get a random question starter for the given type."""
        starters = QUESTION_STARTERS.get(qa_type, QUESTION_STARTERS["definition"])
        return self.rng.choice(starters)
    
    def get_graha_templates(self, category: Optional[str] = None) -> List[QuestionTemplate]:
        """Get all graha templates, optionally filtered by category."""
        templates = []
        for template_list in GRAHA_TEMPLATES.values():
            for t in template_list:
                if category is None or t.category == category or t.category is None:
                    templates.append(t)
        return templates
    
    def get_bhava_templates(self, category: Optional[str] = None) -> List[QuestionTemplate]:
        """Get all bhava templates."""
        templates = []
        for template_list in BHAVA_TEMPLATES.values():
            for t in template_list:
                if category is None or t.category == category or t.category is None:
                    templates.append(t)
        return templates
    
    def get_scenario_templates(self, category: str) -> List[QuestionTemplate]:
        """Get scenario templates for a specific prediction category."""
        return SCENARIO_TEMPLATES.get(category, [])
    
    def get_jaimini_templates(self) -> List[QuestionTemplate]:
        """Get all Jaimini-specific templates."""
        templates = []
        for template_list in JAIMINI_TEMPLATES.values():
            templates.extend(template_list)
        return templates
    
    def fill_template(self, template: QuestionTemplate, **kwargs) -> Tuple[str, str]:
        """Fill a template with provided values, return (question, answer_guidance)."""
        question = template.template.format(**kwargs)
        answer_guidance = template.answer_guidance.format(**kwargs)
        return question, answer_guidance
    
    def generate_graha_combinations(self) -> List[dict]:
        """Generate all meaningful graha-based Q&A combinations."""
        combinations = []
        
        for graha_key, graha_data in GRAHAS.items():
            graha_sanskrit = graha_data["sanskrit"]
            graha_english = graha_data["english"]
            
            # Basic templates for each graha
            for template in GRAHA_TEMPLATES["basic"]:
                combinations.append({
                    "template": template,
                    "params": {
                        "graha_sanskrit": graha_sanskrit,
                        "graha_english": graha_english,
                    },
                    "graha": graha_key,
                })
            
            # Placement templates: graha in each bhava
            for bhava_num, bhava_data in BHAVAS.items():
                for template in GRAHA_TEMPLATES["placement"]:
                    if "bhava" in template.template:
                        combinations.append({
                            "template": template,
                            "params": {
                                "graha_sanskrit": graha_sanskrit,
                                "graha_english": graha_english,
                                "bhava_ordinal": self._ordinal(bhava_num),
                                "bhava_name": bhava_data["name"],
                            },
                            "graha": graha_key,
                            "bhava": bhava_num,
                        })
            
            # Placement templates: graha in each rashi
            for rashi_key, rashi_data in RASHIS.items():
                for template in GRAHA_TEMPLATES["placement"]:
                    if "rashi" in template.template:
                        combinations.append({
                            "template": template,
                            "params": {
                                "graha_sanskrit": graha_sanskrit,
                                "graha_english": graha_english,
                                "rashi_sanskrit": rashi_data["sanskrit"],
                                "rashi_english": rashi_data["english"],
                            },
                            "graha": graha_key,
                            "rashi": rashi_key,
                        })
            
            # Dasha templates
            for template in GRAHA_TEMPLATES["dasha"]:
                combinations.append({
                    "template": template,
                    "params": {
                        "graha_sanskrit": graha_sanskrit,
                        "graha_english": graha_english,
                    },
                    "graha": graha_key,
                })
        
        return combinations
    
    def generate_bhava_combinations(self) -> List[dict]:
        """Generate all meaningful bhava-based Q&A combinations."""
        combinations = []
        
        for bhava_num, bhava_data in BHAVAS.items():
            # Basic templates
            for template in BHAVA_TEMPLATES["basic"]:
                combinations.append({
                    "template": template,
                    "params": {
                        "bhava_ordinal": self._ordinal(bhava_num),
                        "bhava_name": bhava_data["name"],
                    },
                    "bhava": bhava_num,
                })
            
            # Lordship templates: lord in each other house
            for target_bhava in range(1, 13):
                if target_bhava != bhava_num:
                    for template in BHAVA_TEMPLATES["lordship"]:
                        if "target_bhava" in template.template:
                            combinations.append({
                                "template": template,
                                "params": {
                                    "bhava_ordinal": self._ordinal(bhava_num),
                                    "bhava_name": bhava_data["name"],
                                    "target_bhava_ordinal": self._ordinal(target_bhava),
                                },
                                "bhava": bhava_num,
                                "target_bhava": target_bhava,
                            })
            
            # Prediction area templates
            for pred_area in bhava_data.get("prediction_areas", []):
                for template in BHAVA_TEMPLATES["prediction_areas"]:
                    combinations.append({
                        "template": template,
                        "params": {
                            "bhava_ordinal": self._ordinal(bhava_num),
                            "bhava_name": bhava_data["name"],
                            "prediction_area": pred_area,
                        },
                        "bhava": bhava_num,
                        "prediction_area": pred_area,
                    })
        
        return combinations
    
    def generate_conjunction_combinations(self) -> List[dict]:
        """Generate graha conjunction combinations."""
        combinations = []
        graha_list = list(GRAHAS.keys())
        
        for i, graha1_key in enumerate(graha_list):
            for graha2_key in graha_list[i+1:]:
                graha1_data = GRAHAS[graha1_key]
                graha2_data = GRAHAS[graha2_key]
                
                for template in GRAHA_TEMPLATES["conjunction"]:
                    combinations.append({
                        "template": template,
                        "params": {
                            "graha1_sanskrit": graha1_data["sanskrit"],
                            "graha2_sanskrit": graha2_data["sanskrit"],
                        },
                        "graha1": graha1_key,
                        "graha2": graha2_key,
                    })
        
        return combinations
    
    def _ordinal(self, n: int) -> str:
        """Convert number to ordinal string."""
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = suffixes.get(n % 10, 'th')
        return f"{n}{suffix}"
    
    def get_all_template_types(self) -> Dict[str, int]:
        """Get count of available templates by type."""
        return {
            "graha_basic": len(GRAHA_TEMPLATES["basic"]),
            "graha_placement": len(GRAHA_TEMPLATES["placement"]),
            "graha_dignity": len(GRAHA_TEMPLATES["dignity"]),
            "graha_dasha": len(GRAHA_TEMPLATES["dasha"]),
            "graha_aspects": len(GRAHA_TEMPLATES["aspects"]),
            "graha_conjunction": len(GRAHA_TEMPLATES["conjunction"]),
            "bhava_basic": len(BHAVA_TEMPLATES["basic"]),
            "bhava_lordship": len(BHAVA_TEMPLATES["lordship"]),
            "bhava_prediction": len(BHAVA_TEMPLATES["prediction_areas"]),
            "rashi_basic": len(RASHI_TEMPLATES["basic"]),
            "rashi_lagna": len(RASHI_TEMPLATES["lagna"]),
            "yoga_definition": len(YOGA_TEMPLATES["definition"]),
            "yoga_application": len(YOGA_TEMPLATES["application"]),
            "jaimini_karaka": len(JAIMINI_TEMPLATES["karaka"]),
            "jaimini_dasha": len(JAIMINI_TEMPLATES["dasha"]),
            "jaimini_aspects": len(JAIMINI_TEMPLATES["aspects"]),
            "scenario_career": len(SCENARIO_TEMPLATES["career"]),
            "scenario_marriage": len(SCENARIO_TEMPLATES["marriage"]),
            "scenario_health": len(SCENARIO_TEMPLATES["health"]),
            "scenario_wealth": len(SCENARIO_TEMPLATES["wealth"]),
            "scenario_children": len(SCENARIO_TEMPLATES["children"]),
        }
