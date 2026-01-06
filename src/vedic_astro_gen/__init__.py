"""
Vedic Astrology Data Generator

A comprehensive data generation pipeline for creating high-quality
Vedic astrology (Jyotiṣa) Q&A datasets for LLM fine-tuning.

Features:
- Structured template system for systematic Q&A generation
- PDF knowledge extraction with Sanskrit diacritics preservation
- Quality filters for duplicate and low-quality removal
- Diversity checking to ensure varied question patterns
- Domain-specific augmentation for Vedic astrology
"""

__version__ = "1.0.0"
__author__ = "Vedic Astrology ML Project"

from vedic_astro_gen.generator import VedicQAGenerator, GenerationConfig, generate_vedic_qa
from vedic_astro_gen.pdf_extractor import VedicPDFExtractor
from vedic_astro_gen.quality_filters import QualityFilter, DiversityChecker
from vedic_astro_gen.augmentation import VedicAugmenter
from vedic_astro_gen.templates import TemplateManager

__all__ = [
    "VedicQAGenerator",
    "GenerationConfig",
    "generate_vedic_qa",
    "VedicPDFExtractor",
    "QualityFilter",
    "DiversityChecker",
    "VedicAugmenter",
    "TemplateManager",
]
