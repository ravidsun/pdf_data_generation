"""
Tests for Vedic Astrology Data Generator

Run with: pytest tests/ -v
"""

import json
import tempfile
import pytest
from pathlib import Path


class TestKnowledgeBase:
    """Tests for knowledge base data structures."""
    
    def test_grahas_exist(self):
        """Test that all 9 grahas are defined."""
        from vedic_astro_gen.knowledge_base import GRAHAS
        
        expected_grahas = [
            "surya", "chandra", "mangala", "budha", "guru",
            "shukra", "shani", "rahu", "ketu"
        ]
        
        for graha in expected_grahas:
            assert graha in GRAHAS, f"Missing graha: {graha}"
            assert "sanskrit" in GRAHAS[graha]
            assert "english" in GRAHAS[graha]
            assert "significations" in GRAHAS[graha]
    
    def test_rashis_exist(self):
        """Test that all 12 rashis are defined."""
        from vedic_astro_gen.knowledge_base import RASHIS
        
        assert len(RASHIS) == 12, f"Expected 12 rashis, got {len(RASHIS)}"
        
        for rashi_key, rashi_data in RASHIS.items():
            assert "sanskrit" in rashi_data
            assert "english" in rashi_data
            assert "lord" in rashi_data
    
    def test_bhavas_exist(self):
        """Test that all 12 bhavas are defined."""
        from vedic_astro_gen.knowledge_base import BHAVAS
        
        for i in range(1, 13):
            assert i in BHAVAS, f"Missing bhava: {i}"
            assert "name" in BHAVAS[i]
            assert "significations" in BHAVAS[i]
    
    def test_nakshatras_exist(self):
        """Test that all 27 nakshatras are defined."""
        from vedic_astro_gen.knowledge_base import NAKSHATRAS
        
        assert len(NAKSHATRAS) == 27, f"Expected 27 nakshatras, got {len(NAKSHATRAS)}"


class TestTemplateManager:
    """Tests for template generation."""
    
    def test_template_manager_init(self):
        """Test template manager initialization."""
        from vedic_astro_gen.templates import TemplateManager
        
        manager = TemplateManager(seed=42)
        assert manager is not None
    
    def test_graha_combinations(self):
        """Test graha combination generation."""
        from vedic_astro_gen.templates import TemplateManager
        
        manager = TemplateManager(seed=42)
        combinations = manager.generate_graha_combinations()
        
        assert len(combinations) > 0, "No graha combinations generated"
        
        # Check structure
        for combo in combinations[:5]:
            assert "template" in combo
            assert "params" in combo
    
    def test_bhava_combinations(self):
        """Test bhava combination generation."""
        from vedic_astro_gen.templates import TemplateManager
        
        manager = TemplateManager(seed=42)
        combinations = manager.generate_bhava_combinations()
        
        assert len(combinations) > 0, "No bhava combinations generated"
    
    def test_template_types_count(self):
        """Test that template types are counted correctly."""
        from vedic_astro_gen.templates import TemplateManager
        
        manager = TemplateManager()
        counts = manager.get_all_template_types()
        
        assert isinstance(counts, dict)
        assert sum(counts.values()) > 0


class TestQualityFilter:
    """Tests for quality filtering."""
    
    def test_filter_initialization(self):
        """Test filter initialization."""
        from vedic_astro_gen.quality_filters import QualityFilter
        
        qf = QualityFilter(
            min_question_length=20,
            min_answer_length=30,
        )
        assert qf is not None
    
    def test_filter_removes_short_questions(self):
        """Test that short questions are filtered."""
        from vedic_astro_gen.quality_filters import QualityFilter
        
        qf = QualityFilter(min_question_length=20)
        
        data = [
            {"question": "Short?", "answer": "This is a valid answer with enough words."},
            {"question": "What is the significance of Jupiter in Vedic astrology?", 
             "answer": "Jupiter is the greatest benefic..."}
        ]
        
        result = qf.filter_dataset(data)
        assert len(result.kept) == 1
        assert len(result.removed) == 1
    
    def test_filter_removes_duplicates(self):
        """Test that exact duplicates are removed."""
        from vedic_astro_gen.quality_filters import QualityFilter
        
        qf = QualityFilter()
        
        data = [
            {"question": "What is the effect of Saturn?", "answer": "Saturn causes delays and discipline."},
            {"question": "What is the effect of Saturn?", "answer": "Saturn causes delays and discipline."},
            {"question": "What is the effect of Jupiter?", "answer": "Jupiter brings wisdom and expansion."}
        ]
        
        result = qf.filter_dataset(data)
        assert len(result.kept) == 2
        assert result.stats["duplicates"] == 1


class TestDiversityChecker:
    """Tests for diversity checking."""
    
    def test_diversity_analysis(self):
        """Test diversity analysis."""
        from vedic_astro_gen.quality_filters import DiversityChecker
        
        checker = DiversityChecker()
        
        data = [
            {"question": "What is Saturn?"},
            {"question": "What is Jupiter?"},
            {"question": "How does Mars affect career?"},
            {"question": "Why is Venus important?"},
            {"question": "Compare Sun and Moon."},
        ]
        
        report = checker.analyze_diversity(data)
        
        assert "diversity_score" in report
        assert "pattern_counts" in report
        assert report["total_questions"] == 5
    
    def test_diversity_score_range(self):
        """Test that diversity score is in valid range."""
        from vedic_astro_gen.quality_filters import DiversityChecker
        
        checker = DiversityChecker()
        
        data = [{"question": f"What is term {i}?"} for i in range(10)]
        report = checker.analyze_diversity(data)
        
        assert 0 <= report["diversity_score"] <= 1


class TestAugmentation:
    """Tests for data augmentation."""
    
    def test_augmenter_initialization(self):
        """Test augmenter initialization."""
        from vedic_astro_gen.augmentation import VedicAugmenter
        
        augmenter = VedicAugmenter(seed=42)
        assert augmenter is not None
    
    def test_term_swap_sanskrit_to_english(self):
        """Test Sanskrit to English term swapping."""
        from vedic_astro_gen.augmentation import VedicAugmenter
        
        augmenter = VedicAugmenter(seed=42)
        
        # Test with a question containing Sanskrit term
        question = "What is the effect of Sūrya in the 10th house?"
        answer = "Sūrya in the 10th gives authority and leadership."
        
        pairs = augmenter.augment_pair(question, answer, "test_1", methods=["term_swap"])
        
        # May or may not produce augmentation depending on random choice
        # Just verify no error
        assert isinstance(pairs, list)
    
    def test_augment_dataset(self):
        """Test dataset augmentation."""
        from vedic_astro_gen.augmentation import VedicAugmenter
        
        augmenter = VedicAugmenter(seed=42)
        
        data = [
            {"question": "What is the effect of planets?", "answer": "Planets influence life in various ways."},
            {"question": "How does the Moon affect mind?", "answer": "Moon governs emotions and mental state."},
        ]
        
        augmented = augmenter.augment_dataset(
            data,
            augmentations_per_item=1,
            include_original=True,
        )
        
        # Should have originals plus some augmented
        assert len(augmented) >= len(data)


class TestPDFExtractor:
    """Tests for PDF extraction."""
    
    def test_extractor_initialization(self):
        """Test extractor initialization."""
        from vedic_astro_gen.pdf_extractor import VedicPDFExtractor
        
        extractor = VedicPDFExtractor(
            chunk_size=1000,
            chunk_overlap=100,
        )
        assert extractor is not None
    
    def test_clean_text(self):
        """Test text cleaning preserves Sanskrit diacritics."""
        from vedic_astro_gen.pdf_extractor import VedicPDFExtractor
        
        extractor = VedicPDFExtractor()
        
        text = "Sūrya is the Ātmakāraka.   Multiple   spaces   here.\n\n\n\nToo many newlines."
        cleaned = extractor._clean_text(text)
        
        # Should preserve diacritics
        assert "Sūrya" in cleaned
        assert "Ātmakāraka" in cleaned
        
        # Should normalize whitespace
        assert "   " not in cleaned
        assert "\n\n\n\n" not in cleaned
    
    def test_detect_jyotish_entities(self):
        """Test Jyotiṣa entity detection."""
        from vedic_astro_gen.pdf_extractor import VedicPDFExtractor
        
        extractor = VedicPDFExtractor()
        
        text = "The Sūrya (Sun) is placed in the Lagna with Guru. The daśā of Śani begins."
        entities = extractor._detect_jyotish_entities(text)
        
        assert len(entities) > 0
        # Should detect some Jyotish terms
        assert any(e in ["sūrya", "lagna", "guru", "daśā", "śani"] for e in entities)


class TestGenerator:
    """Tests for the main generator."""
    
    def test_generator_initialization(self):
        """Test generator initialization."""
        from vedic_astro_gen.generator import VedicQAGenerator, GenerationConfig
        
        config = GenerationConfig()
        generator = VedicQAGenerator(config=config)
        
        assert generator is not None
    
    def test_generate_id(self):
        """Test ID generation is unique."""
        from vedic_astro_gen.generator import VedicQAGenerator
        
        generator = VedicQAGenerator()
        
        id1 = generator._generate_id("Question 1", "test")
        id2 = generator._generate_id("Question 2", "test")
        
        assert id1 != id2
        assert id1.startswith("test_")
    
    def test_template_generation(self):
        """Test template-based generation."""
        from vedic_astro_gen.generator import VedicQAGenerator, GenerationConfig
        
        config = GenerationConfig(
            templates_enabled=True,
            pdf_extraction_enabled=False,
            llm_generation_enabled=False,
        )
        generator = VedicQAGenerator(config=config)
        
        # Generate limited set for testing
        qa_pairs = generator.generate_from_templates(max_per_category=10)
        
        assert len(qa_pairs) > 0
        
        # Check structure
        for qa in qa_pairs[:5]:
            assert hasattr(qa, "question")
            assert hasattr(qa, "answer")
            assert hasattr(qa, "qa_type")


class TestIntegration:
    """Integration tests for the full pipeline."""
    
    def test_full_pipeline_templates_only(self):
        """Test full pipeline with templates only."""
        from vedic_astro_gen.generator import VedicQAGenerator, GenerationConfig
        
        config = GenerationConfig(
            templates_enabled=True,
            pdf_extraction_enabled=False,
            llm_generation_enabled=False,
            augmentation_enabled=False,
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_output.jsonl"
            
            generator = VedicQAGenerator(config=config)
            results = generator.run_full_pipeline(
                pdf_paths=None,
                output_path=str(output_path),
                use_templates=True,
                use_pdf=False,
                use_llm=False,
                use_augmentation=False,
            )
            
            assert output_path.exists()
            assert results["output_count"] > 0
            
            # Verify JSONL format
            with open(output_path) as f:
                first_line = f.readline()
                data = json.loads(first_line)
                assert "question" in data
                assert "answer" in data


class TestCLI:
    """Tests for CLI commands."""
    
    def test_cli_imports(self):
        """Test that CLI can be imported."""
        from vedic_astro_gen.cli import app
        assert app is not None
    
    def test_version_command(self):
        """Test version command."""
        from vedic_astro_gen import __version__
        assert __version__ is not None
        assert isinstance(__version__, str)


# Fixtures

@pytest.fixture
def sample_qa_data():
    """Sample Q&A data for testing."""
    return [
        {
            "id": "test_1",
            "question": "What is the significance of Jupiter in Vedic astrology?",
            "answer": "Jupiter (Guru) is the greatest benefic planet, signifying wisdom, knowledge, dharma, teachers, children, and wealth. It brings expansion and optimism.",
            "qa_type": "definition",
            "difficulty": "easy",
            "tags": ["guru", "jupiter"],
        },
        {
            "id": "test_2",
            "question": "How does Saturn in the 7th house affect marriage?",
            "answer": "Saturn in the 7th house typically delays marriage until after age 28-30. The spouse may be older, mature, or from a different background. The native approaches relationships seriously.",
            "qa_type": "interpretation",
            "difficulty": "medium",
            "tags": ["shani", "bhava_7", "marriage"],
        },
        {
            "id": "test_3",
            "question": "Compare the effects of exalted Mars versus debilitated Mars.",
            "answer": "Exalted Mars in Capricorn gives courage, discipline, and success in competition. Debilitated Mars in Cancer may cause suppressed anger, lack of courage, and family conflicts, though neecha bhanga can modify these results.",
            "qa_type": "comparison",
            "difficulty": "hard",
            "tags": ["mangala", "dignity"],
        },
    ]


@pytest.fixture
def temp_jsonl_file(sample_qa_data):
    """Create a temporary JSONL file with sample data."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for item in sample_qa_data:
            f.write(json.dumps(item) + '\n')
        return f.name


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
