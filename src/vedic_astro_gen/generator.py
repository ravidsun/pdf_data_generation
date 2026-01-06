"""
Main Q&A Generator for Vedic Astrology Fine-Tuning Data

Orchestrates all components:
- PDF extraction
- Template-based Q&A generation
- Quality filtering
- Diversity checking
- Augmentation
- LLM-based generation (optional)
"""

import json
import logging
import hashlib
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Iterator
from dataclasses import dataclass, field
from datetime import datetime
from tqdm import tqdm

from vedic_astro_gen.knowledge_base import (
    GRAHAS, RASHIS, BHAVAS, NAKSHATRAS, YOGAS,
    PREDICTION_TEMPLATES, PredictionCategory,
)
from vedic_astro_gen.templates import TemplateManager, QuestionTemplate
from vedic_astro_gen.pdf_extractor import VedicPDFExtractor, ExtractedChunk
from vedic_astro_gen.quality_filters import QualityFilter, DiversityChecker
from vedic_astro_gen.augmentation import VedicAugmenter, AnswerEnhancer

logger = logging.getLogger(__name__)


@dataclass
class GeneratedQA:
    """A generated Q&A pair with full metadata."""
    id: str
    question: str
    answer: str
    qa_type: str
    difficulty: str
    category: Optional[str]
    tags: List[str]
    source: Dict[str, Any]
    generation_method: str  # template, pdf_extract, llm


@dataclass 
class GenerationConfig:
    """Configuration for Q&A generation."""
    # Extraction settings
    chunk_size: int = 1000
    chunk_overlap: int = 100
    min_chunk_size: int = 100
    
    # Generation settings
    templates_enabled: bool = True
    pdf_extraction_enabled: bool = True
    llm_generation_enabled: bool = False
    
    # LLM settings (if enabled)
    llm_provider: str = "anthropic"
    llm_model: str = "claude-3-haiku-20240307"
    qa_pairs_per_chunk: int = 3
    
    # Quality settings
    min_question_length: int = 20
    min_answer_length: int = 30
    min_answer_words: int = 10
    similarity_threshold: float = 0.85
    
    # Diversity settings
    max_pattern_ratio: float = 0.15
    
    # Augmentation settings
    augmentation_enabled: bool = True
    augmentations_per_item: int = 2
    
    # Output settings
    output_format: str = "jsonl"  # jsonl, json, hf_dataset
    include_metadata: bool = True


class VedicQAGenerator:
    """
    Main generator class for Vedic Astrology Q&A data.
    
    Combines all components into a unified pipeline.
    """
    
    def __init__(self, config: Optional[GenerationConfig] = None, seed: int = 42):
        self.config = config or GenerationConfig()
        self.seed = seed
        
        # Initialize components
        self.template_manager = TemplateManager(seed=seed)
        self.pdf_extractor = VedicPDFExtractor(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            min_chunk_size=self.config.min_chunk_size,
        )
        self.quality_filter = QualityFilter(
            min_question_length=self.config.min_question_length,
            min_answer_length=self.config.min_answer_length,
            min_answer_words=self.config.min_answer_words,
            similarity_threshold=self.config.similarity_threshold,
        )
        self.diversity_checker = DiversityChecker(
            max_pattern_ratio=self.config.max_pattern_ratio
        )
        self.augmenter = VedicAugmenter(seed=seed)
        self.answer_enhancer = AnswerEnhancer()
        
        # LLM generator (lazy initialization)
        self._llm = None
        
        # Stats tracking
        self.stats = {
            "templates_generated": 0,
            "pdf_extracted": 0,
            "llm_generated": 0,
            "filtered_out": 0,
            "augmented": 0,
            "total_output": 0,
        }
    
    def generate_from_templates(
        self,
        categories: Optional[List[str]] = None,
        max_per_category: int = 500,
    ) -> List[GeneratedQA]:
        """
        Generate Q&A pairs using the template system.
        
        Args:
            categories: Prediction categories to include.
            max_per_category: Maximum pairs per category.
            
        Returns:
            List of GeneratedQA objects.
        """
        logger.info("Generating Q&A from templates...")
        generated = []
        
        # Generate graha-based questions
        graha_combinations = self.template_manager.generate_graha_combinations()
        logger.info(f"Generated {len(graha_combinations)} graha template combinations")
        
        for combo in tqdm(graha_combinations[:max_per_category * 2], desc="Graha templates"):
            try:
                qa = self._generate_from_template_combo(combo, "template_graha")
                if qa:
                    generated.append(qa)
            except Exception as e:
                logger.debug(f"Template generation failed: {e}")
        
        # Generate bhava-based questions  
        bhava_combinations = self.template_manager.generate_bhava_combinations()
        logger.info(f"Generated {len(bhava_combinations)} bhava template combinations")
        
        for combo in tqdm(bhava_combinations[:max_per_category], desc="Bhava templates"):
            try:
                qa = self._generate_from_template_combo(combo, "template_bhava")
                if qa:
                    generated.append(qa)
            except Exception as e:
                logger.debug(f"Template generation failed: {e}")
        
        # Generate conjunction questions
        conjunction_combinations = self.template_manager.generate_conjunction_combinations()
        logger.info(f"Generated {len(conjunction_combinations)} conjunction combinations")
        
        for combo in tqdm(conjunction_combinations[:max_per_category // 2], desc="Conjunction templates"):
            try:
                qa = self._generate_from_template_combo(combo, "template_conjunction")
                if qa:
                    generated.append(qa)
            except Exception as e:
                logger.debug(f"Template generation failed: {e}")
        
        self.stats["templates_generated"] = len(generated)
        logger.info(f"Generated {len(generated)} Q&A pairs from templates")
        
        return generated
    
    def _generate_from_template_combo(
        self,
        combo: dict,
        source_type: str,
    ) -> Optional[GeneratedQA]:
        """Generate a Q&A from a template combination."""
        template = combo["template"]
        params = combo["params"]
        
        question, answer_guidance = self.template_manager.fill_template(template, **params)
        
        # Generate answer based on knowledge base
        answer = self._generate_answer_from_knowledge(combo, answer_guidance)
        
        if not answer or len(answer) < self.config.min_answer_length:
            return None
        
        # Create unique ID
        qa_id = self._generate_id(question, source_type)
        
        # Extract tags from combo
        tags = []
        if "graha" in combo:
            tags.append(combo["graha"])
        if "bhava" in combo:
            tags.append(f"bhava_{combo['bhava']}")
        if "rashi" in combo:
            tags.append(combo["rashi"])
        
        return GeneratedQA(
            id=qa_id,
            question=question,
            answer=answer,
            qa_type=template.qa_type,
            difficulty=template.difficulty,
            category=template.category,
            tags=tags,
            source={"type": source_type, "template": template.template},
            generation_method="template",
        )
    
    def _generate_answer_from_knowledge(
        self,
        combo: dict,
        guidance: str,
    ) -> str:
        """Generate an answer using the knowledge base."""
        parts = []
        
        # Get graha information
        if "graha" in combo:
            graha_key = combo["graha"]
            graha_info = GRAHAS.get(graha_key, {})
            
            if graha_info:
                sanskrit = graha_info.get("sanskrit", "")
                english = graha_info.get("english", "")
                nature = graha_info.get("nature", "")
                significations = graha_info.get("significations", [])
                
                parts.append(f"{sanskrit} ({english}) is a {nature}.")
                
                if significations:
                    sig_text = ", ".join(significations[:5])
                    parts.append(f"Its primary significations include {sig_text}.")
                
                # Add karakatva if relevant
                karakatva = graha_info.get("karakatva", {})
                if karakatva.get("primary"):
                    parts.append(f"As a kāraka, it represents {karakatva['primary']}.")
        
        # Get bhava information
        if "bhava" in combo:
            bhava_num = combo["bhava"]
            bhava_info = BHAVAS.get(bhava_num, {})
            
            if bhava_info:
                name = bhava_info.get("name", f"House {bhava_num}")
                significations = bhava_info.get("significations", [])
                
                if significations:
                    sig_text = ", ".join(significations[:4])
                    parts.append(f"The {name} signifies {sig_text}.")
        
        # Get rashi information
        if "rashi" in combo:
            rashi_key = combo["rashi"]
            rashi_info = RASHIS.get(rashi_key, {})
            
            if rashi_info:
                sanskrit = rashi_info.get("sanskrit", "")
                english = rashi_info.get("english", "")
                element = rashi_info.get("element", "")
                lord = rashi_info.get("lord", "")
                quality = rashi_info.get("quality", "")
                
                parts.append(
                    f"{sanskrit} ({english}) is a {element} sign of {quality} "
                    f"quality, ruled by {lord}."
                )
        
        # Combine parts
        if parts:
            answer = " ".join(parts)
            
            # Add interpretation guidance if available
            if "placement" in combo.get("template", {}).template:
                answer += " The combination indicates specific results based on the interaction of these significations."
            
            return answer
        
        return ""
    
    def generate_from_pdf(
        self,
        pdf_path: str,
        use_llm: bool = False,
    ) -> List[GeneratedQA]:
        """
        Generate Q&A pairs from a PDF document.
        
        Args:
            pdf_path: Path to the PDF file.
            use_llm: Whether to use LLM for Q&A generation.
            
        Returns:
            List of GeneratedQA objects.
        """
        logger.info(f"Extracting from PDF: {pdf_path}")
        
        # Extract chunks
        chunks = self.pdf_extractor.extract_from_pdf(pdf_path)
        logger.info(f"Extracted {len(chunks)} chunks")
        
        generated = []
        pdf_name = Path(pdf_path).stem
        
        for chunk in tqdm(chunks, desc="Processing chunks"):
            if use_llm and self.config.llm_generation_enabled:
                # Use LLM to generate Q&A
                qa_pairs = self._generate_qa_with_llm(chunk)
                generated.extend(qa_pairs)
            else:
                # Create text-based Q&A (simpler approach)
                qa = self._create_qa_from_chunk(chunk, pdf_name)
                if qa:
                    generated.append(qa)
        
        self.stats["pdf_extracted"] = len(generated)
        logger.info(f"Generated {len(generated)} Q&A pairs from PDF")
        
        return generated
    
    def _create_qa_from_chunk(
        self,
        chunk: ExtractedChunk,
        pdf_name: str,
    ) -> Optional[GeneratedQA]:
        """Create a Q&A pair from a PDF chunk (without LLM)."""
        text = chunk.text.strip()
        
        if len(text) < 100:
            return None
        
        # Try to create a question based on chunk content
        entities = chunk.entities
        
        if not entities:
            return None
        
        # Use first entity to form a question
        main_entity = entities[0]
        
        # Create question
        question = f"Based on the Jyotiṣa text, explain the concept of {main_entity}."
        
        # Use chunk text as answer (truncated if needed)
        answer = text[:500] if len(text) > 500 else text
        
        qa_id = self._generate_id(question, f"pdf_{pdf_name}")
        
        return GeneratedQA(
            id=qa_id,
            question=question,
            answer=answer,
            qa_type="concept",
            difficulty="medium",
            category=None,
            tags=entities[:5],
            source={
                "type": "pdf_extraction",
                "pdf_name": chunk.source_pdf,
                "page_start": chunk.page_start,
                "page_end": chunk.page_end,
                "section": chunk.section_title,
            },
            generation_method="pdf_extract",
        )
    
    def _generate_qa_with_llm(
        self,
        chunk: ExtractedChunk,
    ) -> List[GeneratedQA]:
        """Generate Q&A pairs using LLM API."""
        if self._llm is None:
            self._initialize_llm()
        
        if self._llm is None:
            logger.warning("LLM not available, skipping LLM generation")
            return []
        
        generated = []
        
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            
            system_prompt = """You are an expert in Vedic astrology (Jyotiṣa) creating Q&A pairs for training data.
Generate diverse, high-quality question-answer pairs from the given text.

Guidelines:
- Questions should be specific and answerable from the text
- Use proper Sanskrit terminology with diacritical marks (ā, ī, ū, ṛ, ṣ, ṭ, ḍ, ṇ)
- Vary question types: definition, interpretation, procedure, prediction, comparison
- Answers should be comprehensive and accurate

Return a JSON array with objects containing "question", "answer", "qa_type", and "difficulty" fields."""

            human_prompt = f"""Generate {self.config.qa_pairs_per_chunk} Q&A pairs from this Jyotiṣa text:

---
{chunk.text}
---

Return ONLY a valid JSON array."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt),
            ]
            
            response = self._llm.invoke(messages)
            content = response.content.strip()
            
            # Parse response
            import re
            if content.startswith("```"):
                content = re.sub(r'^```(?:json)?\n?', '', content)
                content = re.sub(r'\n?```$', '', content)
            
            pairs = json.loads(content)
            
            for pair in pairs:
                qa_id = self._generate_id(pair["question"], "llm")
                
                generated.append(GeneratedQA(
                    id=qa_id,
                    question=pair["question"],
                    answer=pair["answer"],
                    qa_type=pair.get("qa_type", "concept"),
                    difficulty=pair.get("difficulty", "medium"),
                    category=None,
                    tags=chunk.entities[:5],
                    source={
                        "type": "llm_generation",
                        "pdf_name": chunk.source_pdf,
                        "page_start": chunk.page_start,
                        "page_end": chunk.page_end,
                        "model": self.config.llm_model,
                    },
                    generation_method="llm",
                ))
            
            self.stats["llm_generated"] += len(generated)
            
        except Exception as e:
            logger.warning(f"LLM generation failed: {e}")
        
        return generated
    
    def _initialize_llm(self):
        """Initialize LLM for generation."""
        provider = self.config.llm_provider
        model = self.config.llm_model
        
        if provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                logger.warning("ANTHROPIC_API_KEY not set")
                return
            
            try:
                from langchain_anthropic import ChatAnthropic
                self._llm = ChatAnthropic(
                    model=model,
                    temperature=0.3,
                    max_tokens=1024,
                    api_key=api_key,
                )
            except ImportError:
                logger.warning("langchain-anthropic not installed")
        
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.warning("OPENAI_API_KEY not set")
                return
            
            try:
                from langchain_openai import ChatOpenAI
                self._llm = ChatOpenAI(
                    model=model or "gpt-4o-mini",
                    temperature=0.3,
                    max_tokens=1024,
                    api_key=api_key,
                )
            except ImportError:
                logger.warning("langchain-openai not installed")
    
    def run_full_pipeline(
        self,
        pdf_paths: Optional[List[str]] = None,
        output_path: str = "data/output/vedic_qa.jsonl",
        use_templates: bool = True,
        use_pdf: bool = True,
        use_llm: bool = False,
        use_augmentation: bool = True,
    ) -> Dict[str, Any]:
        """
        Run the complete generation pipeline.
        
        Args:
            pdf_paths: List of PDF paths to process.
            output_path: Output file path.
            use_templates: Whether to use template generation.
            use_pdf: Whether to extract from PDFs.
            use_llm: Whether to use LLM generation.
            use_augmentation: Whether to apply augmentation.
            
        Returns:
            Pipeline statistics and results.
        """
        logger.info("Starting full generation pipeline...")
        all_generated = []
        
        # Step 1: Template-based generation
        if use_templates and self.config.templates_enabled:
            template_qa = self.generate_from_templates()
            all_generated.extend(template_qa)
            logger.info(f"Template generation: {len(template_qa)} Q&A pairs")
        
        # Step 2: PDF extraction
        if use_pdf and pdf_paths and self.config.pdf_extraction_enabled:
            for pdf_path in pdf_paths:
                pdf_qa = self.generate_from_pdf(pdf_path, use_llm=use_llm)
                all_generated.extend(pdf_qa)
            logger.info(f"PDF extraction: {self.stats['pdf_extracted']} Q&A pairs")
        
        # Step 3: Convert to dict format for filtering
        data = [self._qa_to_dict(qa) for qa in all_generated]
        logger.info(f"Total before filtering: {len(data)} Q&A pairs")
        
        # Step 4: Quality filtering
        filter_result = self.quality_filter.filter_dataset(data)
        filtered_data = filter_result.kept
        self.stats["filtered_out"] = len(filter_result.removed)
        logger.info(f"After filtering: {len(filtered_data)} Q&A pairs")
        
        # Step 5: Diversity check and balance
        diversity_report = self.diversity_checker.analyze_diversity(filtered_data)
        logger.info(f"Diversity score: {diversity_report['diversity_score']:.2f}")
        
        if diversity_report["over_represented"]:
            filtered_data = self.diversity_checker.balance_dataset(filtered_data)
            logger.info(f"After balancing: {len(filtered_data)} Q&A pairs")
        
        # Step 6: Augmentation
        if use_augmentation and self.config.augmentation_enabled:
            augmented_data = self.augmenter.augment_dataset(
                filtered_data,
                augmentations_per_item=self.config.augmentations_per_item,
            )
            self.stats["augmented"] = len(augmented_data) - len(filtered_data)
            final_data = augmented_data
        else:
            final_data = filtered_data
        
        self.stats["total_output"] = len(final_data)
        
        # Step 7: Save output
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in final_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        logger.info(f"Saved {len(final_data)} Q&A pairs to {output_path}")
        
        # Final diversity check
        final_diversity = self.diversity_checker.analyze_diversity(final_data)
        
        return {
            "stats": self.stats,
            "output_path": str(output_path),
            "output_count": len(final_data),
            "diversity_report": final_diversity,
            "filter_stats": filter_result.stats,
        }
    
    def _qa_to_dict(self, qa: GeneratedQA) -> dict:
        """Convert GeneratedQA to dictionary."""
        result = {
            "id": qa.id,
            "question": qa.question,
            "answer": qa.answer,
            "qa_type": qa.qa_type,
            "difficulty": qa.difficulty,
            "tags": qa.tags,
        }
        
        if self.config.include_metadata:
            result["source"] = qa.source
            result["generation_method"] = qa.generation_method
            if qa.category:
                result["category"] = qa.category
        
        return result
    
    def _generate_id(self, text: str, prefix: str) -> str:
        """Generate a unique ID for a Q&A pair."""
        hash_input = f"{prefix}_{text}_{datetime.now().isoformat()}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"{prefix}_{hash_value}"


def generate_vedic_qa(
    pdf_paths: Optional[List[str]] = None,
    output_path: str = "data/output/vedic_qa.jsonl",
    config: Optional[GenerationConfig] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Convenience function to generate Vedic astrology Q&A data.
    
    Args:
        pdf_paths: List of PDF paths to process.
        output_path: Output file path.
        config: Generation configuration.
        **kwargs: Additional pipeline arguments.
        
    Returns:
        Generation results and statistics.
    """
    generator = VedicQAGenerator(config=config)
    return generator.run_full_pipeline(
        pdf_paths=pdf_paths,
        output_path=output_path,
        **kwargs,
    )
