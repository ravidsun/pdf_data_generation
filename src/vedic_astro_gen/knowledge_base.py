"""
Vedic Astrology Knowledge Base

Comprehensive definitions of all astrological entities, their relationships,
and significations. This serves as the foundation for generating diverse Q&A pairs.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class PredictionCategory(Enum):
    """Categories of astrological prediction."""
    CAREER = "career"
    MARRIAGE = "marriage"
    HEALTH = "health"
    WEALTH = "wealth"
    CHILDREN = "children"
    EDUCATION = "education"
    SPIRITUALITY = "spirituality"
    LONGEVITY = "longevity"
    FOREIGN_TRAVEL = "foreign_travel"
    LITIGATION = "litigation"
    PROPERTY = "property"
    VEHICLES = "vehicles"
    GENERAL = "general"


# =============================================================================
# GRAHAS (PLANETS)
# =============================================================================

GRAHAS = {
    "surya": {
        "sanskrit": "Sūrya",
        "english": "Sun",
        "nature": "natural malefic",
        "gender": "masculine",
        "element": "fire",
        "guna": "sattvic",
        "caste": "kshatriya",
        "day": "Sunday",
        "direction": "East",
        "color": "copper/red",
        "gemstone": "Ruby (Māṇikya)",
        "metal": "gold",
        "deity": "Agni/Śiva",
        "avatar": "Rāma",
        "body_parts": ["heart", "bones", "right eye", "spine"],
        "diseases": ["heart disease", "eye problems", "fever", "bone disorders"],
        "significations": [
            "soul", "father", "king", "government", "authority", "ego", "vitality",
            "health", "fame", "honor", "leadership", "self-confidence", "willpower"
        ],
        "karakatva": {
            "primary": "Ātmakāraka (soul)",
            "relationships": "father, paternal figures, authority",
            "profession": "government, politics, medicine, administration"
        },
        "exaltation": {"sign": "Meṣa (Aries)", "degree": 10},
        "debilitation": {"sign": "Tulā (Libra)", "degree": 10},
        "own_signs": ["Siṃha (Leo)"],
        "moolatrikona": {"sign": "Siṃha (Leo)", "degrees": "0-20"},
        "friends": ["Moon", "Mars", "Jupiter"],
        "enemies": ["Venus", "Saturn"],
        "neutral": ["Mercury"],
        "aspects": [7],
        "dasha_years": 6,
        "mahadasha_order": 1,
    },
    "chandra": {
        "sanskrit": "Candra",
        "english": "Moon",
        "nature": "benefic when waxing, malefic when waning",
        "gender": "feminine",
        "element": "water",
        "guna": "sattvic",
        "caste": "vaishya",
        "day": "Monday",
        "direction": "Northwest",
        "color": "white",
        "gemstone": "Pearl (Muktā)",
        "metal": "silver",
        "deity": "Pārvatī/Durgā",
        "avatar": "Kṛṣṇa",
        "body_parts": ["mind", "blood", "left eye", "breasts", "stomach"],
        "diseases": ["mental disorders", "cold", "cough", "water retention"],
        "significations": [
            "mind", "mother", "emotions", "feelings", "public", "popularity",
            "nurturing", "memory", "imagination", "fertility", "travel"
        ],
        "karakatva": {
            "primary": "Manas (mind), Mātṛkāraka (mother)",
            "relationships": "mother, maternal figures, women",
            "profession": "nursing, hospitality, liquids, agriculture"
        },
        "exaltation": {"sign": "Vṛṣabha (Taurus)", "degree": 3},
        "debilitation": {"sign": "Vṛścika (Scorpio)", "degree": 3},
        "own_signs": ["Karkaṭa (Cancer)"],
        "moolatrikona": {"sign": "Vṛṣabha (Taurus)", "degrees": "4-30"},
        "friends": ["Sun", "Mercury"],
        "enemies": ["none"],
        "neutral": ["Mars", "Jupiter", "Venus", "Saturn"],
        "aspects": [7],
        "dasha_years": 10,
        "mahadasha_order": 2,
    },
    "mangala": {
        "sanskrit": "Maṅgala/Kuja",
        "english": "Mars",
        "nature": "natural malefic",
        "gender": "masculine",
        "element": "fire",
        "guna": "tamasic",
        "caste": "kshatriya",
        "day": "Tuesday",
        "direction": "South",
        "color": "red",
        "gemstone": "Red Coral (Pravāla)",
        "metal": "copper",
        "deity": "Subrahmaṇya/Kārttikeya",
        "avatar": "Narasiṃha",
        "body_parts": ["muscles", "blood", "marrow", "head"],
        "diseases": ["accidents", "surgery", "burns", "blood disorders", "fever"],
        "significations": [
            "courage", "energy", "brothers", "land", "property", "warfare",
            "aggression", "passion", "sports", "engineering", "surgery"
        ],
        "karakatva": {
            "primary": "Bhrātṛkāraka (siblings)",
            "relationships": "younger siblings, brothers",
            "profession": "military, police, surgery, engineering, sports"
        },
        "exaltation": {"sign": "Makara (Capricorn)", "degree": 28},
        "debilitation": {"sign": "Karkaṭa (Cancer)", "degree": 28},
        "own_signs": ["Meṣa (Aries)", "Vṛścika (Scorpio)"],
        "moolatrikona": {"sign": "Meṣa (Aries)", "degrees": "0-12"},
        "friends": ["Sun", "Moon", "Jupiter"],
        "enemies": ["Mercury"],
        "neutral": ["Venus", "Saturn"],
        "aspects": [4, 7, 8],
        "dasha_years": 7,
        "mahadasha_order": 3,
    },
    "budha": {
        "sanskrit": "Budha",
        "english": "Mercury",
        "nature": "benefic with benefics, malefic with malefics",
        "gender": "neuter",
        "element": "earth",
        "guna": "rajasic",
        "caste": "vaishya",
        "day": "Wednesday",
        "direction": "North",
        "color": "green",
        "gemstone": "Emerald (Marakata)",
        "metal": "bronze",
        "deity": "Viṣṇu",
        "avatar": "Buddha",
        "body_parts": ["nervous system", "skin", "tongue", "arms", "lungs"],
        "diseases": ["nervous disorders", "skin diseases", "speech problems"],
        "significations": [
            "intelligence", "communication", "commerce", "writing", "mathematics",
            "education", "siblings", "friends", "adaptability", "youth"
        ],
        "karakatva": {
            "primary": "Buddhikāraka (intellect)",
            "relationships": "maternal uncle, adopted children",
            "profession": "writing, accounting, teaching, astrology, trade"
        },
        "exaltation": {"sign": "Kanyā (Virgo)", "degree": 15},
        "debilitation": {"sign": "Mīna (Pisces)", "degree": 15},
        "own_signs": ["Mithuna (Gemini)", "Kanyā (Virgo)"],
        "moolatrikona": {"sign": "Kanyā (Virgo)", "degrees": "16-20"},
        "friends": ["Sun", "Venus"],
        "enemies": ["Moon"],
        "neutral": ["Mars", "Jupiter", "Saturn"],
        "aspects": [7],
        "dasha_years": 17,
        "mahadasha_order": 4,
    },
    "guru": {
        "sanskrit": "Guru/Bṛhaspati",
        "english": "Jupiter",
        "nature": "greatest natural benefic",
        "gender": "masculine",
        "element": "ether/space",
        "guna": "sattvic",
        "caste": "brahmin",
        "day": "Thursday",
        "direction": "Northeast",
        "color": "yellow",
        "gemstone": "Yellow Sapphire (Puṣparāga)",
        "metal": "gold",
        "deity": "Indra/Dakṣiṇāmūrti",
        "avatar": "Vāmana",
        "body_parts": ["liver", "fat", "thighs", "ears"],
        "diseases": ["liver problems", "diabetes", "obesity", "tumors"],
        "significations": [
            "wisdom", "knowledge", "dharma", "teacher", "children", "wealth",
            "expansion", "optimism", "husband (for women)", "religion", "fortune"
        ],
        "karakatva": {
            "primary": "Putrakāraka (children), Dhana (wealth)",
            "relationships": "husband (female chart), children, teachers",
            "profession": "teaching, law, finance, priesthood, counseling"
        },
        "exaltation": {"sign": "Karkaṭa (Cancer)", "degree": 5},
        "debilitation": {"sign": "Makara (Capricorn)", "degree": 5},
        "own_signs": ["Dhanu (Sagittarius)", "Mīna (Pisces)"],
        "moolatrikona": {"sign": "Dhanu (Sagittarius)", "degrees": "0-10"},
        "friends": ["Sun", "Moon", "Mars"],
        "enemies": ["Mercury", "Venus"],
        "neutral": ["Saturn"],
        "aspects": [5, 7, 9],
        "dasha_years": 16,
        "mahadasha_order": 5,
    },
    "shukra": {
        "sanskrit": "Śukra",
        "english": "Venus",
        "nature": "natural benefic",
        "gender": "feminine",
        "element": "water",
        "guna": "rajasic",
        "caste": "brahmin",
        "day": "Friday",
        "direction": "Southeast",
        "color": "white/variegated",
        "gemstone": "Diamond (Vajra)",
        "metal": "silver",
        "deity": "Lakṣmī",
        "avatar": "Paraśurāma",
        "body_parts": ["reproductive organs", "face", "eyes", "kidneys"],
        "diseases": ["venereal diseases", "kidney problems", "diabetes"],
        "significations": [
            "love", "beauty", "art", "music", "luxury", "vehicles", "wife",
            "marriage", "pleasure", "romance", "creativity", "comforts"
        ],
        "karakatva": {
            "primary": "Kalatrākāraka (spouse)",
            "relationships": "wife (male chart), lovers, artists",
            "profession": "arts, fashion, entertainment, luxury goods"
        },
        "exaltation": {"sign": "Mīna (Pisces)", "degree": 27},
        "debilitation": {"sign": "Kanyā (Virgo)", "degree": 27},
        "own_signs": ["Vṛṣabha (Taurus)", "Tulā (Libra)"],
        "moolatrikona": {"sign": "Tulā (Libra)", "degrees": "0-15"},
        "friends": ["Mercury", "Saturn"],
        "enemies": ["Sun", "Moon"],
        "neutral": ["Mars", "Jupiter"],
        "aspects": [7],
        "dasha_years": 20,
        "mahadasha_order": 6,
    },
    "shani": {
        "sanskrit": "Śani",
        "english": "Saturn",
        "nature": "greatest natural malefic",
        "gender": "neuter",
        "element": "air",
        "guna": "tamasic",
        "caste": "shudra",
        "day": "Saturday",
        "direction": "West",
        "color": "black/dark blue",
        "gemstone": "Blue Sapphire (Nīlam)",
        "metal": "iron",
        "deity": "Brahma/Yama",
        "avatar": "Kūrma",
        "body_parts": ["legs", "nerves", "teeth", "bones", "joints"],
        "diseases": ["chronic diseases", "paralysis", "arthritis", "depression"],
        "significations": [
            "karma", "discipline", "longevity", "delays", "obstacles",
            "servants", "old age", "sorrow", "persistence", "hard work", "detachment"
        ],
        "karakatva": {
            "primary": "Āyuṣkāraka (longevity)",
            "relationships": "servants, elderly, laborers",
            "profession": "labor, mining, agriculture, judiciary, real estate"
        },
        "exaltation": {"sign": "Tulā (Libra)", "degree": 20},
        "debilitation": {"sign": "Meṣa (Aries)", "degree": 20},
        "own_signs": ["Makara (Capricorn)", "Kumbha (Aquarius)"],
        "moolatrikona": {"sign": "Kumbha (Aquarius)", "degrees": "0-20"},
        "friends": ["Mercury", "Venus"],
        "enemies": ["Sun", "Moon", "Mars"],
        "neutral": ["Jupiter"],
        "aspects": [3, 7, 10],
        "dasha_years": 19,
        "mahadasha_order": 7,
    },
    "rahu": {
        "sanskrit": "Rāhu",
        "english": "North Node",
        "nature": "malefic (like Saturn)",
        "gender": "feminine",
        "element": "air",
        "guna": "tamasic",
        "day": "Saturday",
        "direction": "Southwest",
        "color": "smoky/dark",
        "gemstone": "Hessonite (Gomed)",
        "metal": "lead",
        "deity": "Durgā",
        "body_parts": ["skin", "breathing"],
        "diseases": ["mysterious diseases", "poison", "psychological disorders"],
        "significations": [
            "illusion", "foreign", "unconventional", "obsession", "ambition",
            "technology", "outcasts", "sudden events", "material desires"
        ],
        "karakatva": {
            "primary": "Māyā (illusion), foreign matters",
            "relationships": "foreigners, outcasts, paternal grandparents",
            "profession": "technology, foreign trade, research, speculation"
        },
        "exaltation": {"sign": "Vṛṣabha (Taurus)", "degree": None},
        "debilitation": {"sign": "Vṛścika (Scorpio)", "degree": None},
        "own_signs": ["Kumbha (Aquarius)"],
        "friends": ["Mercury", "Venus", "Saturn"],
        "enemies": ["Sun", "Moon", "Mars"],
        "neutral": ["Jupiter"],
        "aspects": [5, 7, 9],
        "dasha_years": 18,
        "mahadasha_order": 8,
    },
    "ketu": {
        "sanskrit": "Ketu",
        "english": "South Node",
        "nature": "malefic (like Mars)",
        "gender": "neuter",
        "element": "fire",
        "guna": "tamasic",
        "day": "Tuesday",
        "direction": "Northeast",
        "color": "smoky/multicolored",
        "gemstone": "Cat's Eye (Vaidūrya)",
        "metal": "lead",
        "deity": "Gaṇeśa",
        "body_parts": ["spine", "nervous system"],
        "diseases": ["mysterious diseases", "surgery", "accidents"],
        "significations": [
            "moksha", "liberation", "spirituality", "past life karma",
            "detachment", "isolation", "occult", "psychic abilities", "losses"
        ],
        "karakatva": {
            "primary": "Mokṣa (liberation)",
            "relationships": "maternal grandparents, spiritual teachers",
            "profession": "occult, research, mathematics, programming"
        },
        "exaltation": {"sign": "Vṛścika (Scorpio)", "degree": None},
        "debilitation": {"sign": "Vṛṣabha (Taurus)", "degree": None},
        "own_signs": ["Vṛścika (Scorpio)"],
        "friends": ["Mercury", "Venus", "Saturn"],
        "enemies": ["Sun", "Moon", "Mars"],
        "neutral": ["Jupiter"],
        "aspects": [5, 7, 9],
        "dasha_years": 7,
        "mahadasha_order": 9,
    },
}


# =============================================================================
# RASHIS (SIGNS)
# =============================================================================

RASHIS = {
    "mesha": {
        "sanskrit": "Meṣa",
        "english": "Aries",
        "number": 1,
        "element": "fire",
        "quality": "movable (cara)",
        "gender": "masculine",
        "direction": "East",
        "lord": "Mars",
        "body_part": "head",
        "nature": "aggressive, pioneering, independent",
        "characteristics": [
            "leadership", "initiative", "courage", "impulsiveness",
            "competitive", "energetic", "direct", "self-assertive"
        ],
    },
    "vrishabha": {
        "sanskrit": "Vṛṣabha",
        "english": "Taurus",
        "number": 2,
        "element": "earth",
        "quality": "fixed (sthira)",
        "gender": "feminine",
        "direction": "South",
        "lord": "Venus",
        "body_part": "face, throat",
        "nature": "stable, sensual, materialistic",
        "characteristics": [
            "patience", "reliability", "determination", "possessiveness",
            "artistic", "comfort-loving", "practical", "stubborn"
        ],
    },
    "mithuna": {
        "sanskrit": "Mithuna",
        "english": "Gemini",
        "number": 3,
        "element": "air",
        "quality": "dual (dvisvabhāva)",
        "gender": "masculine",
        "direction": "West",
        "lord": "Mercury",
        "body_part": "shoulders, arms",
        "nature": "communicative, intellectual, versatile",
        "characteristics": [
            "adaptability", "curiosity", "wit", "restlessness",
            "duality", "communication", "learning", "superficiality"
        ],
    },
    "karkata": {
        "sanskrit": "Karkaṭa",
        "english": "Cancer",
        "number": 4,
        "element": "water",
        "quality": "movable (cara)",
        "gender": "feminine",
        "direction": "North",
        "lord": "Moon",
        "body_part": "chest, breasts",
        "nature": "emotional, nurturing, protective",
        "characteristics": [
            "sensitivity", "domesticity", "intuition", "moodiness",
            "caring", "tenacity", "patriotism", "insecurity"
        ],
    },
    "simha": {
        "sanskrit": "Siṃha",
        "english": "Leo",
        "number": 5,
        "element": "fire",
        "quality": "fixed (sthira)",
        "gender": "masculine",
        "direction": "East",
        "lord": "Sun",
        "body_part": "heart, stomach",
        "nature": "royal, creative, dramatic",
        "characteristics": [
            "leadership", "generosity", "pride", "creativity",
            "confidence", "warmth", "arrogance", "loyalty"
        ],
    },
    "kanya": {
        "sanskrit": "Kanyā",
        "english": "Virgo",
        "number": 6,
        "element": "earth",
        "quality": "dual (dvisvabhāva)",
        "gender": "feminine",
        "direction": "South",
        "lord": "Mercury",
        "body_part": "intestines, waist",
        "nature": "analytical, practical, service-oriented",
        "characteristics": [
            "discrimination", "precision", "criticism", "modesty",
            "health-conscious", "perfectionism", "worry", "helpfulness"
        ],
    },
    "tula": {
        "sanskrit": "Tulā",
        "english": "Libra",
        "number": 7,
        "element": "air",
        "quality": "movable (cara)",
        "gender": "masculine",
        "direction": "West",
        "lord": "Venus",
        "body_part": "lower abdomen, kidneys",
        "nature": "balanced, harmonious, partnership-oriented",
        "characteristics": [
            "diplomacy", "justice", "partnership", "indecision",
            "charm", "refinement", "balance", "dependency"
        ],
    },
    "vrishchika": {
        "sanskrit": "Vṛścika",
        "english": "Scorpio",
        "number": 8,
        "element": "water",
        "quality": "fixed (sthira)",
        "gender": "feminine",
        "direction": "North",
        "lord": "Mars",
        "co_lord": "Ketu",
        "body_part": "genitals, reproductive organs",
        "nature": "intense, transformative, secretive",
        "characteristics": [
            "intensity", "passion", "secrecy", "jealousy",
            "transformation", "research", "occult", "vengeance"
        ],
    },
    "dhanu": {
        "sanskrit": "Dhanu",
        "english": "Sagittarius",
        "number": 9,
        "element": "fire",
        "quality": "dual (dvisvabhāva)",
        "gender": "masculine",
        "direction": "East",
        "lord": "Jupiter",
        "body_part": "thighs, hips",
        "nature": "philosophical, adventurous, optimistic",
        "characteristics": [
            "optimism", "philosophy", "travel", "restlessness",
            "honesty", "higher learning", "preaching", "exaggeration"
        ],
    },
    "makara": {
        "sanskrit": "Makara",
        "english": "Capricorn",
        "number": 10,
        "element": "earth",
        "quality": "movable (cara)",
        "gender": "feminine",
        "direction": "South",
        "lord": "Saturn",
        "body_part": "knees",
        "nature": "ambitious, disciplined, practical",
        "characteristics": [
            "ambition", "discipline", "responsibility", "pessimism",
            "status", "authority", "tradition", "coldness"
        ],
    },
    "kumbha": {
        "sanskrit": "Kumbha",
        "english": "Aquarius",
        "number": 11,
        "element": "air",
        "quality": "fixed (sthira)",
        "gender": "masculine",
        "direction": "West",
        "lord": "Saturn",
        "co_lord": "Rahu",
        "body_part": "ankles, calves",
        "nature": "humanitarian, innovative, detached",
        "characteristics": [
            "originality", "humanitarianism", "detachment", "eccentricity",
            "independence", "innovation", "rebellion", "aloofness"
        ],
    },
    "meena": {
        "sanskrit": "Mīna",
        "english": "Pisces",
        "number": 12,
        "element": "water",
        "quality": "dual (dvisvabhāva)",
        "gender": "feminine",
        "direction": "North",
        "lord": "Jupiter",
        "co_lord": "Ketu",
        "body_part": "feet",
        "nature": "spiritual, intuitive, compassionate",
        "characteristics": [
            "spirituality", "compassion", "imagination", "escapism",
            "psychic", "sacrifice", "illusion", "transcendence"
        ],
    },
}


# =============================================================================
# BHAVAS (HOUSES)
# =============================================================================

BHAVAS = {
    1: {
        "name": "Lagna/Tanu Bhāva",
        "english": "Ascendant/First House",
        "natural_sign": "Aries",
        "karaka": "Sun",
        "category": "kendra (angle), trikona (trine)",
        "significations": [
            "self", "body", "personality", "appearance", "health", "vitality",
            "birth", "head", "brain", "general fortune", "beginning of life"
        ],
        "prediction_areas": [
            "physical constitution", "personality traits", "general health",
            "life direction", "fame", "success", "longevity indicators"
        ],
    },
    2: {
        "name": "Dhana Bhāva",
        "english": "Second House",
        "natural_sign": "Taurus",
        "karaka": "Jupiter",
        "category": "maraka (death-inflicting)",
        "significations": [
            "wealth", "family", "speech", "food", "face", "right eye",
            "accumulated wealth", "values", "early childhood", "death"
        ],
        "prediction_areas": [
            "financial status", "family relations", "speech patterns",
            "food habits", "savings", "facial features", "early education"
        ],
    },
    3: {
        "name": "Sahaja/Parākrama Bhāva",
        "english": "Third House",
        "natural_sign": "Gemini",
        "karaka": "Mars",
        "category": "upachaya (growing)",
        "significations": [
            "siblings", "courage", "communication", "short journeys",
            "arms", "shoulders", "neighbors", "skills", "hobbies", "efforts"
        ],
        "prediction_areas": [
            "sibling relations", "courage and valor", "communication skills",
            "short travels", "writing ability", "artistic talents"
        ],
    },
    4: {
        "name": "Sukha/Bandhu Bhāva",
        "english": "Fourth House",
        "natural_sign": "Cancer",
        "karaka": "Moon, Mercury",
        "category": "kendra (angle)",
        "significations": [
            "mother", "home", "property", "vehicles", "education", "happiness",
            "chest", "heart", "comfort", "land", "domestic peace", "emotions"
        ],
        "prediction_areas": [
            "mother's health", "property ownership", "vehicle acquisition",
            "domestic happiness", "formal education", "emotional well-being"
        ],
    },
    5: {
        "name": "Putra/Suta Bhāva",
        "english": "Fifth House",
        "natural_sign": "Leo",
        "karaka": "Jupiter",
        "category": "trikona (trine)",
        "significations": [
            "children", "creativity", "intelligence", "romance", "speculation",
            "past life merit", "mantras", "stomach", "higher education", "fame"
        ],
        "prediction_areas": [
            "childbirth timing", "children's welfare", "creative pursuits",
            "speculative gains", "romantic affairs", "spiritual practices"
        ],
    },
    6: {
        "name": "Ripu/Ari Bhāva",
        "english": "Sixth House",
        "natural_sign": "Virgo",
        "karaka": "Mars, Saturn",
        "category": "trik (evil), upachaya (growing)",
        "significations": [
            "enemies", "diseases", "debts", "service", "obstacles", "pets",
            "maternal uncle", "theft", "accidents", "intestines", "competition"
        ],
        "prediction_areas": [
            "health issues", "legal disputes", "debts", "employment",
            "enemies and competitors", "daily work", "service to others"
        ],
    },
    7: {
        "name": "Kalatrā/Jāyā Bhāva",
        "english": "Seventh House",
        "natural_sign": "Libra",
        "karaka": "Venus",
        "category": "kendra (angle), maraka (death-inflicting)",
        "significations": [
            "spouse", "marriage", "partnerships", "business", "foreign travel",
            "public dealings", "lower abdomen", "kidneys", "contracts", "desires"
        ],
        "prediction_areas": [
            "marriage timing", "spouse characteristics", "marital harmony",
            "business partnerships", "foreign settlement", "public image"
        ],
    },
    8: {
        "name": "Āyu/Mṛtyu Bhāva",
        "english": "Eighth House",
        "natural_sign": "Scorpio",
        "karaka": "Saturn",
        "category": "trik (evil)",
        "significations": [
            "longevity", "death", "transformation", "inheritance", "occult",
            "research", "accidents", "chronic disease", "hidden matters", "obstacles"
        ],
        "prediction_areas": [
            "longevity calculation", "mode of death", "inheritance",
            "sudden events", "chronic diseases", "occult abilities", "research"
        ],
    },
    9: {
        "name": "Dharma/Bhāgya Bhāva",
        "english": "Ninth House",
        "natural_sign": "Sagittarius",
        "karaka": "Jupiter, Sun",
        "category": "trikona (trine)",
        "significations": [
            "father", "fortune", "religion", "dharma", "guru", "long journeys",
            "higher education", "philosophy", "law", "grandchildren", "thighs"
        ],
        "prediction_areas": [
            "father's welfare", "fortune and luck", "religious inclination",
            "foreign travel", "higher learning", "spiritual guru", "legal matters"
        ],
    },
    10: {
        "name": "Karma/Rājya Bhāva",
        "english": "Tenth House",
        "natural_sign": "Capricorn",
        "karaka": "Sun, Saturn, Mercury, Jupiter",
        "category": "kendra (angle), upachaya (growing)",
        "significations": [
            "career", "profession", "status", "authority", "government",
            "fame", "karma", "father (alternate)", "knees", "achievement"
        ],
        "prediction_areas": [
            "career success", "professional growth", "public recognition",
            "government relations", "authority positions", "achievements"
        ],
    },
    11: {
        "name": "Lābha Bhāva",
        "english": "Eleventh House",
        "natural_sign": "Aquarius",
        "karaka": "Jupiter",
        "category": "upachaya (growing)",
        "significations": [
            "gains", "income", "elder siblings", "friends", "desires fulfilled",
            "ankles", "social network", "achievements", "aspirations"
        ],
        "prediction_areas": [
            "financial gains", "elder sibling relations", "friendships",
            "wish fulfillment", "networking", "income sources"
        ],
    },
    12: {
        "name": "Vyaya/Mokṣa Bhāva",
        "english": "Twelfth House",
        "natural_sign": "Pisces",
        "karaka": "Saturn, Ketu",
        "category": "trik (evil)",
        "significations": [
            "losses", "expenses", "foreign lands", "moksha", "hospitalization",
            "isolation", "bed pleasures", "feet", "left eye", "subconscious"
        ],
        "prediction_areas": [
            "foreign settlement", "spiritual liberation", "expenses",
            "hospitalization", "sleep patterns", "subconscious tendencies"
        ],
    },
}


# =============================================================================
# NAKSHATRAS (LUNAR MANSIONS)
# =============================================================================

NAKSHATRAS = {
    1: {"name": "Aśvinī", "lord": "Ketu", "deity": "Aśvini Kumāras", "symbol": "Horse head", "nature": "Light/Swift", "gana": "Deva"},
    2: {"name": "Bharaṇī", "lord": "Venus", "deity": "Yama", "symbol": "Yoni", "nature": "Fierce", "gana": "Manushya"},
    3: {"name": "Kṛttikā", "lord": "Sun", "deity": "Agni", "symbol": "Razor/Flame", "nature": "Mixed", "gana": "Rakshasa"},
    4: {"name": "Rohiṇī", "lord": "Moon", "deity": "Brahmā", "symbol": "Cart/Chariot", "nature": "Fixed", "gana": "Manushya"},
    5: {"name": "Mṛgaśirā", "lord": "Mars", "deity": "Soma", "symbol": "Deer head", "nature": "Soft", "gana": "Deva"},
    6: {"name": "Ārdrā", "lord": "Rahu", "deity": "Rudra", "symbol": "Teardrop", "nature": "Sharp", "gana": "Manushya"},
    7: {"name": "Punarvasu", "lord": "Jupiter", "deity": "Aditi", "symbol": "Bow/Quiver", "nature": "Movable", "gana": "Deva"},
    8: {"name": "Puṣya", "lord": "Saturn", "deity": "Bṛhaspati", "symbol": "Flower/Udder", "nature": "Light", "gana": "Deva"},
    9: {"name": "Āśleṣā", "lord": "Mercury", "deity": "Sarpas", "symbol": "Serpent", "nature": "Sharp", "gana": "Rakshasa"},
    10: {"name": "Maghā", "lord": "Ketu", "deity": "Pitṛs", "symbol": "Throne", "nature": "Fierce", "gana": "Rakshasa"},
    11: {"name": "Pūrva Phālgunī", "lord": "Venus", "deity": "Bhaga", "symbol": "Hammock", "nature": "Fierce", "gana": "Manushya"},
    12: {"name": "Uttara Phālgunī", "lord": "Sun", "deity": "Aryaman", "symbol": "Bed", "nature": "Fixed", "gana": "Manushya"},
    13: {"name": "Hasta", "lord": "Moon", "deity": "Savitṛ", "symbol": "Hand", "nature": "Light", "gana": "Deva"},
    14: {"name": "Citrā", "lord": "Mars", "deity": "Tvaṣṭṛ", "symbol": "Pearl", "nature": "Soft", "gana": "Rakshasa"},
    15: {"name": "Svātī", "lord": "Rahu", "deity": "Vāyu", "symbol": "Coral/Sword", "nature": "Movable", "gana": "Deva"},
    16: {"name": "Viśākhā", "lord": "Jupiter", "deity": "Indra-Agni", "symbol": "Archway", "nature": "Mixed", "gana": "Rakshasa"},
    17: {"name": "Anurādhā", "lord": "Saturn", "deity": "Mitra", "symbol": "Lotus", "nature": "Soft", "gana": "Deva"},
    18: {"name": "Jyeṣṭhā", "lord": "Mercury", "deity": "Indra", "symbol": "Earring", "nature": "Sharp", "gana": "Rakshasa"},
    19: {"name": "Mūla", "lord": "Ketu", "deity": "Nirṛti", "symbol": "Roots", "nature": "Sharp", "gana": "Rakshasa"},
    20: {"name": "Pūrvāṣāḍhā", "lord": "Venus", "deity": "Āpas", "symbol": "Fan/Tusk", "nature": "Fierce", "gana": "Manushya"},
    21: {"name": "Uttarāṣāḍhā", "lord": "Sun", "deity": "Viśvedevas", "symbol": "Tusk", "nature": "Fixed", "gana": "Manushya"},
    22: {"name": "Śravaṇa", "lord": "Moon", "deity": "Viṣṇu", "symbol": "Ear/Trident", "nature": "Movable", "gana": "Deva"},
    23: {"name": "Dhaniṣṭhā", "lord": "Mars", "deity": "Vasus", "symbol": "Drum", "nature": "Movable", "gana": "Rakshasa"},
    24: {"name": "Śatabhiṣā", "lord": "Rahu", "deity": "Varuṇa", "symbol": "Circle", "nature": "Movable", "gana": "Rakshasa"},
    25: {"name": "Pūrva Bhādrapadā", "lord": "Jupiter", "deity": "Aja Ekapāda", "symbol": "Sword/Legs", "nature": "Fierce", "gana": "Manushya"},
    26: {"name": "Uttara Bhādrapadā", "lord": "Saturn", "deity": "Ahir Budhnya", "symbol": "Twins", "nature": "Fixed", "gana": "Manushya"},
    27: {"name": "Revatī", "lord": "Mercury", "deity": "Pūṣan", "symbol": "Fish/Drum", "nature": "Soft", "gana": "Deva"},
}


# =============================================================================
# YOGAS (PLANETARY COMBINATIONS)
# =============================================================================

YOGAS = {
    # Pancha Mahapurusha Yogas
    "ruchaka": {
        "name": "Ruchaka Yoga",
        "planets": ["Mars"],
        "condition": "Mars in own sign or exaltation in kendra",
        "effects": "Courage, commander, powerful, successful in battles",
        "category": "pancha_mahapurusha"
    },
    "bhadra": {
        "name": "Bhadra Yoga",
        "planets": ["Mercury"],
        "condition": "Mercury in own sign or exaltation in kendra",
        "effects": "Intelligence, eloquence, learned, good in business",
        "category": "pancha_mahapurusha"
    },
    "hamsa": {
        "name": "Hamsa Yoga",
        "planets": ["Jupiter"],
        "condition": "Jupiter in own sign or exaltation in kendra",
        "effects": "Righteous, religious, respected, blessed with good fortune",
        "category": "pancha_mahapurusha"
    },
    "malavya": {
        "name": "Malavya Yoga",
        "planets": ["Venus"],
        "condition": "Venus in own sign or exaltation in kendra",
        "effects": "Prosperous, beautiful spouse, artistic, luxurious life",
        "category": "pancha_mahapurusha"
    },
    "shasha": {
        "name": "Śaśa Yoga",
        "planets": ["Saturn"],
        "condition": "Saturn in own sign or exaltation in kendra",
        "effects": "Leader, commands servants, successful late in life",
        "category": "pancha_mahapurusha"
    },
    
    # Wealth Yogas
    "dhana": {
        "name": "Dhana Yoga",
        "planets": ["various"],
        "condition": "Lords of 1, 2, 5, 9, 11 in mutual connection",
        "effects": "Wealth accumulation, financial prosperity",
        "category": "wealth"
    },
    "lakshmi": {
        "name": "Lakshmi Yoga",
        "planets": ["Venus", "9th lord"],
        "condition": "9th lord strong in kendra/trikona with Venus",
        "effects": "Great wealth, prosperity, blessed by Lakshmi",
        "category": "wealth"
    },
    
    # Raja Yogas
    "raja": {
        "name": "Rāja Yoga",
        "planets": ["kendra/trikona lords"],
        "condition": "Kendra lord conjunct trikona lord",
        "effects": "Power, authority, success, recognition",
        "category": "raja"
    },
    "dharma_karmadhipati": {
        "name": "Dharma-Karmādhipati Yoga",
        "planets": ["9th lord", "10th lord"],
        "condition": "9th and 10th lords conjunct or in mutual aspect",
        "effects": "Fortune through career, righteous success",
        "category": "raja"
    },
    
    # Negative Yogas
    "kemadruma": {
        "name": "Kemadruma Yoga",
        "planets": ["Moon"],
        "condition": "No planets in 2nd or 12th from Moon",
        "effects": "Poverty, struggles, lack of support (cancelled by various factors)",
        "category": "negative"
    },
    "kala_sarpa": {
        "name": "Kālasarpa Yoga",
        "planets": ["all grahas", "Rahu", "Ketu"],
        "condition": "All planets between Rahu-Ketu axis",
        "effects": "Karmic struggles, delays, ultimate transformation",
        "category": "negative"
    },
    
    # Jaimini Yogas
    "svamsha": {
        "name": "Svāṃśa analysis",
        "planets": ["Ātmakāraka"],
        "condition": "Ātmakāraka's navāṃśa position",
        "effects": "Soul's journey and spiritual path",
        "category": "jaimini"
    },
    "argala": {
        "name": "Argalā",
        "planets": ["various"],
        "condition": "Planets in 2nd, 4th, 11th, 5th from a house",
        "effects": "Intervention/influence on the house matters",
        "category": "jaimini"
    },
}


# =============================================================================
# DASHAS (PLANETARY PERIODS)
# =============================================================================

VIMSHOTTARI_DASHA = {
    "order": ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"],
    "years": {
        "Ketu": 7,
        "Venus": 20,
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17,
    },
    "total_years": 120,
}

JAIMINI_DASHAS = {
    "chara_dasha": {
        "name": "Cara Daśā",
        "type": "rashi_based",
        "usage": "General life events, timing",
    },
    "sthira_dasha": {
        "name": "Sthira Daśā",
        "type": "rashi_based",
        "usage": "Longevity, death timing",
    },
    "narayana_dasha": {
        "name": "Nārāyaṇa Daśā",
        "type": "rashi_based",
        "usage": "Material prosperity, worldly affairs",
    },
    "shoola_dasha": {
        "name": "Śūla Daśā",
        "type": "rashi_based",
        "usage": "Death timing, dangers",
    },
}


# =============================================================================
# KRISHNAMURTI PADDHATI (KP SYSTEM)
# =============================================================================

KP_SUB_LORDS = {
    "concept": "Sub-lord is the most important significator in KP System",
    "subdivision": "Each nakshatra is divided into 9 sub-divisions ruled by 9 planets",
    "importance": "Sub-lord determines the final result of any house or planet",
    "hierarchy": "Sign Lord → Star Lord → Sub Lord (most important)",
}

KP_CUSPAL_INTERLINKS = {
    "concept": "Relationship between house cusps and their sub-lords",
    "rule": "The sub-lord of a cusp determines whether the house signification will manifest",
    "application": "Used for precise timing and yes/no predictions",
}

KP_SIGNIFICATORS = {
    "planet_significator": {
        "definition": "Planets that have connection to a particular house",
        "types": [
            "Planets posited in the house",
            "Planets aspecting the house",
            "Planets posited in the star of occupant",
            "Planets posited in the star of lord",
            "Planet as house lord",
            "Planets in the star of aspecting planets"
        ],
        "priority_order": "Occupant → Star of occupant → Lord → Star of lord → Aspects"
    },
    "house_grouping": {
        "1-5-9": "Dharma trikona (Dharma, education, luck)",
        "2-6-10": "Artha trikona (Wealth, service, career)",
        "3-7-11": "Kama trikona (Courage, partnership, gains)",
        "4-8-12": "Moksha trikona (Property, longevity, liberation)"
    }
}

KP_RULING_PLANETS = {
    "concept": "Planets ruling at the moment of judgment/query",
    "components": [
        "Day lord (weekday)",
        "Lagna lord (ascendant sign)",
        "Lagna star lord (ascendant nakshatra)",
        "Lagna sub lord (ascendant sub)",
        "Moon sign lord",
        "Moon star lord",
        "Moon sub lord"
    ],
    "usage": "Used for horary astrology and precise timing"
}

KP_HOUSES_SIGNIFICATION = {
    "marriage": {
        "houses": [2, 7, 11],
        "negative_houses": [1, 6, 10],
        "rule": "2-7-11 connected for marriage; avoid 1-6-10"
    },
    "career": {
        "houses": [2, 6, 10, 11],
        "rule": "2-6-10-11 for career and profession"
    },
    "education": {
        "houses": [4, 9, 11],
        "negative_houses": [3, 8],
        "rule": "4-9-11 for education; 3-8 cause breaks"
    },
    "children": {
        "houses": [2, 5, 11],
        "negative_houses": [1, 4, 10],
        "rule": "2-5-11 for children; avoid 1-4-10"
    },
    "foreign_travel": {
        "houses": [3, 9, 12],
        "rule": "3-9-12 for foreign travel and settlement"
    },
    "moksha": {
        "houses": [4, 8, 12],
        "rule": "4-8-12 for spiritual liberation"
    }
}

KP_TIMING_METHODS = {
    "dasha_system": {
        "name": "Viṃśottarī Daśā (KP Style)",
        "calculation": "Based on Moon's longitude in nakshatra",
        "levels": ["Mahādaśā", "Antardaśā", "Pratyantardaśā", "Sūkṣmadaśā", "Prāṇadaśā"],
        "key_principle": "Event happens in dasha of planet connected to relevant houses"
    },
    "transit": {
        "importance": "Transits activate natal promises",
        "rule": "Transit planet must be significator of the event",
        "timing": "Day when slow-moving planets transit sensitive cuspal degrees"
    },
    "progression": {
        "secondary": "1 day = 1 year progression",
        "usage": "Refines timing within dasha-bhukti periods"
    }
}

KP_STELLAR_ASTROLOGY = {
    "concept": "Each planet gives results of its star lord, not its own",
    "nakshatra_division": {
        "total": 27,
        "each_spans": "13°20' of zodiac",
        "sub_divisions": 9,
        "ruling_order": ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    },
    "prediction_rule": "Planet in a star gives results of star lord's house significations"
}

KP_YOGAS = {
    "kp_raja_yoga": {
        "rule": "Significators of 1-2-6-10-11 houses together",
        "result": "Power, authority, and success"
    },
    "kp_dhana_yoga": {
        "rule": "Significators of 2-6-10-11 houses connected",
        "result": "Wealth and prosperity"
    },
    "negative_combinations": {
        "maraka": "Strong connection to 2 and 7 (death inflicting)",
        "disease": "6-8-12 connections without benefics",
        "obstacles": "Sub-lord of 11th in 6-8-12 denies gains"
    }
}

KP_HORARY_RULES = {
    "number_selection": {
        "range": "1 to 249",
        "calculation": "Number determines ascendant for the horary chart",
        "alternative": "Use time of question"
    },
    "judgment": {
        "key_factor": "11th cusp sub-lord is crucial",
        "promise": "If sub-lord is favorable significator, answer is YES",
        "denial": "If sub-lord is negative significator, answer is NO"
    },
    "ruling_planets_role": {
        "timing": "Ruling planets at time of query indicate when event happens",
        "confirmation": "Common ruling planets between query and natal chart confirm event"
    }
}

KP_CUSPAL_SUB_LORD_RULES = {
    "principle": "Sub-lord of a house cusp determines the result of that house",
    "examples": {
        "7th_cusp_sublord": {
            "positive": "In 2-7-11 stars = marriage happens",
            "negative": "In 1-6-10 stars = marriage delayed/denied"
        },
        "10th_cusp_sublord": {
            "positive": "In 2-6-10-11 stars = career success",
            "negative": "In 8-12 stars = career obstacles"
        },
        "5th_cusp_sublord": {
            "positive": "In 2-5-11 stars = children",
            "negative": "In 1-4-10 stars = no children/delays"
        }
    }
}

KP_AYANAMSA = {
    "name": "Krishnamurti Ayanāṃśa",
    "value_1900": "22°27'38\"",
    "rate": "50.2388475\" per year",
    "difference": "Slightly different from Lahiri Ayanāṃśa",
    "importance": "Critical for accurate sub-lord calculation"
}


# =============================================================================
# PREDICTION TEMPLATES
# =============================================================================

PREDICTION_TEMPLATES = {
    "career": {
        "factors": ["10th house", "10th lord", "Sun", "Saturn", "Mercury", "Jupiter"],
        "dashas": ["10th lord dasha", "Saturn dasha", "Sun dasha"],
        "transits": ["Saturn over 10th", "Jupiter over 10th"],
        "questions": [
            "What career is suitable based on the 10th house and its lord?",
            "When will career success come based on dasha periods?",
            "What are the indicators for government job in this chart?",
            "Will there be job changes during {dasha} period?",
        ],
    },
    "marriage": {
        "factors": ["7th house", "7th lord", "Venus", "Jupiter", "Upapada"],
        "dashas": ["7th lord dasha", "Venus dasha", "Jupiter dasha"],
        "transits": ["Jupiter over 7th", "Saturn over 7th"],
        "questions": [
            "When is marriage likely based on dasha and transits?",
            "What are the characteristics of the spouse?",
            "What factors indicate delay in marriage?",
            "Is there indication of second marriage?",
        ],
    },
    "health": {
        "factors": ["Lagna", "6th house", "8th house", "Moon", "Sun"],
        "dashas": ["6th lord dasha", "8th lord dasha"],
        "transits": ["Saturn over Lagna", "Rahu-Ketu transits"],
        "questions": [
            "What health issues are indicated by the chart?",
            "During which periods should health be carefully monitored?",
            "What are the longevity indicators?",
            "Which planets are causing health afflictions?",
        ],
    },
    "wealth": {
        "factors": ["2nd house", "11th house", "5th house", "9th house", "Jupiter"],
        "dashas": ["2nd lord dasha", "11th lord dasha", "5th lord dasha"],
        "transits": ["Jupiter over 2nd/11th", "Saturn over 11th"],
        "questions": [
            "What are the wealth indicators in this chart?",
            "When will financial gains be maximum?",
            "Is there dhana yoga present?",
            "What are the sources of income indicated?",
        ],
    },
    "education": {
        "factors": ["4th house", "5th house", "Mercury", "Jupiter", "2nd house"],
        "dashas": ["Mercury dasha", "Jupiter dasha", "5th lord dasha"],
        "questions": [
            "What field of education is suitable?",
            "Will higher education be successful?",
            "Are there breaks in education indicated?",
            "What are the learning abilities?",
        ],
    },
    "children": {
        "factors": ["5th house", "5th lord", "Jupiter", "9th house"],
        "dashas": ["5th lord dasha", "Jupiter dasha"],
        "questions": [
            "When is childbirth likely?",
            "How many children are indicated?",
            "Are there any issues regarding children?",
            "What is the relationship with children?",
        ],
    },
}


def get_graha_info(graha_key: str) -> dict:
    """Get complete information about a graha."""
    return GRAHAS.get(graha_key.lower(), {})


def get_rashi_info(rashi_key: str) -> dict:
    """Get complete information about a rashi."""
    return RASHIS.get(rashi_key.lower(), {})


def get_bhava_info(bhava_num: int) -> dict:
    """Get complete information about a bhava."""
    return BHAVAS.get(bhava_num, {})


def get_nakshatra_info(nakshatra_num: int) -> dict:
    """Get complete information about a nakshatra."""
    return NAKSHATRAS.get(nakshatra_num, {})


def get_all_grahas() -> list:
    """Get list of all graha keys."""
    return list(GRAHAS.keys())


def get_all_rashis() -> list:
    """Get list of all rashi keys."""
    return list(RASHIS.keys())
