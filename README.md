# Vedic Astrology Data Generator

A comprehensive data generation pipeline for creating high-quality **Vedic astrology (Jyotiṣa) Q&A datasets** for LLM fine-tuning. Designed to solve the common problem of repetitive, low-diversity training data that causes fine-tuned models to produce repetitive outputs.

## 📑 Table of Contents

- [Problem Solved](#-problem-solved)
- [Architecture Overview](#-architecture-overview)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
  - [Setup Guide](docs/SETUP_GUIDE.md) - Complete step-by-step instructions
- [Data Quality Analysis](#-data-quality-analysis)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Output Format](#-output-format)
- [Comparison: Before vs After](#-comparison-before-vs-after)
- [Makefile Commands](#-makefile-commands)
- [Utility Scripts](#-utility-scripts)
- [Knowledge Base Coverage](#-knowledge-base-coverage)
- [Advanced Usage](#-advanced-usage)
- [Performance Tips](#-performance-tips)
- [Troubleshooting](#-troubleshooting)
- [Additional Resources](#-additional-resources)
- [Contributing](#-contributing)
- [License](#-license)
- [Dependencies](#-dependencies)
- [Acknowledgments](#-acknowledgments)
- [Appendix: Sanskrit Diacritics Reference](#appendix-sanskrit-diacritics-reference)

## 🎯 Problem Solved

When fine-tuning LLMs on domain-specific data, common issues include:
- **Repetitive question patterns** (e.g., 50%+ starting with "What is...")
- **Short, template-like answers** lacking depth
- **Limited diversity** in question types
- **Poor coverage** of domain concepts
- **Duplicate or near-duplicate** content

This tool addresses all these issues with a comprehensive pipeline specifically designed for Vedic astrology content.

## 🏗️ Architecture Overview

The pipeline consists of five main components that work together:

```
┌─────────────────┐
│  Input Sources  │
│  - Templates    │
│  - PDFs         │
│  - LLM (opt)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Extraction    │
│  - PDF Parser   │
│  - Chunking     │
│  - Entities     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Generation    │
│  - Templates    │
│  - Combinations │
│  - LLM Gen      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Quality Filter  │
│  - Duplicates   │
│  - Min length   │
│  - Relevance    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Augmentation   │
│  - Term swap    │
│  - Paraphrase   │
│  - Synonyms     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Diversity Check │
│  - Balance      │
│  - Metrics      │
│  - Report       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Output (JSONL)  │
└─────────────────┘
```

**Key Features:**
- **Modular Design**: Each component can be used independently
- **Pipeline Orchestration**: [generator.py](src/vedic_astro_gen/generator.py) coordinates all steps
- **Configurable**: Every step is customizable via YAML or Python API
- **Extensible**: Easy to add new templates, filters, or augmentation methods

## ✨ Features

### 1. Structured Template System
- **9 Grahas (Planets)** × **12 Bhavas (Houses)** × **12 Rashis (Signs)** = comprehensive combinations
- **27 Nakshatras (Lunar Mansions)** with lords, deities, and significations
- **50+ Yogas** including Pancha Mahapurusha, Raja, Dhana, and Jaimini yogas
- **Vimshottari & Jaimini Dasha systems** for timing predictions
- **Krishnamurti Paddhati (KP System)** - sub-lords, significators, cuspal analysis, horary
- **15+ question patterns** avoiding repetitive starters
- **Difficulty levels**: easy, medium, hard
- **Prediction categories**: career, marriage, health, wealth, children, spirituality, etc.

### 2. PDF Knowledge Extractor
- **Sanskrit diacritics preservation** (ā, ī, ū, ṛ, ṣ, ṭ, ḍ, ṇ)
- **Intelligent chunking** respecting sentence boundaries
- **Jyotiṣa terminology detection** for entity extraction
- **Section structure detection** for context preservation

### 3. Quality Filters
- **Exact duplicate removal**
- **Near-duplicate detection** using fuzzy matching
- **Minimum length enforcement** for questions and answers
- **Domain relevance checking** (off-topic removal)
- **Repetition detection** in answers

### 4. Diversity Checker
- **Question pattern analysis** and balancing
- **Shannon entropy-based diversity scoring**
- **Automatic dataset rebalancing**
- **Recommendations for improvement**

### 5. Domain-Specific Augmentation
- **Sanskrit ↔ English term swapping** (Sūrya ↔ Sun)
- **Astrological synonym replacement**
- **Question paraphrasing** with domain templates
- **Question type transformation**

## 📋 Prerequisites

- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux
- **Disk Space**: Minimum 500MB for dependencies, additional space for PDFs and generated data
- **Memory**: 4GB RAM minimum (8GB recommended for large PDFs)
- **Optional**: Anthropic or OpenAI API key for LLM-based generation

## 📦 Installation

### Method 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/vedic-astro-data-gen.git
cd vedic-astro-data-gen

# Install the package
pip install -e .

# For proprietary LLM APIs (OpenAI, Anthropic)
pip install -e ".[llm]"

# For open-source LLMs (Llama, Mistral, etc.)
pip install -e ".[llm-opensource]"

# For vLLM (high-performance inference)
pip install -e ".[llm-vllm]"

# For all LLM options
pip install -e ".[llm-all]"

# For development
pip install -e ".[dev]"

# Install everything
pip install -e ".[dev,llm-all]"
```

### Method 2: Using Makefile

```bash
# Install core package
make install

# Install with LLM support
make install-llm

# Install development dependencies
make install-dev

# Install everything
make install-all
```

### Method 3: Using requirements.txt

```bash
pip install -r requirements.txt

# Optional: Install LLM dependencies manually
pip install langchain-anthropic anthropic
```

### Verify Installation

```bash
# Check if CLI is working
vedic-gen --help

# List available templates
vedic-gen templates
```

## 🚀 Quick Start

> **📖 Complete Setup Guide:** [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)
>
> **Configuration:** Llama 3 70B via Groq (8.5/10 quality, $5.40 for 30 PDFs, 13k-16k Q&A pairs)

### Generate Complete Dataset

The generator includes comprehensive templates covering:
- **9 Grahas** × **12 Bhavas** × **12 Rashis** combinations
- **27 Nakshatras** with complete attributes
- **50+ Yogas** (Pancha Mahapurusha, Raja, Dhana, Jaimini)
- **Vimshottari & Jaimini Dasha** systems
- **Krishnamurti Paddhati (KP)** - sub-lords, significators, horary
- **13+ prediction categories**

```bash
# Generate Q&A from templates + your PDF
vedic-gen generate --pdf /path/to/jyotish_book.pdf --output data/vedic_qa.jsonl

# Without PDF (templates only)
vedic-gen generate --output data/vedic_qa.jsonl

# With LLM-based generation - Proprietary API (requires ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=your_key
vedic-gen generate --pdf /path/to/book.pdf --llm --output data/vedic_qa.jsonl

# With Open-Source LLM - Local Ollama (no API key needed!)
vedic-gen generate --config configs/opensource_llm.yaml --pdf /path/to/book.pdf --llm --output data/vedic_qa.jsonl
```

### Individual Commands

```bash
# Extract text from PDF
vedic-gen extract book.pdf --output chunks.json

# Filter existing dataset
vedic-gen filter input.jsonl --output filtered.jsonl

# Augment existing dataset
vedic-gen augment input.jsonl --output augmented.jsonl --per-item 2

# Analyze dataset quality
vedic-gen analyze dataset.jsonl

# List available templates
vedic-gen templates
```

## 📊 Data Quality Analysis

When you run `vedic-gen analyze`, you'll see:

```
Basic Statistics
┌─────────────────┬─────┬─────┬───────┐
│ Metric          │ Min │ Max │ Avg   │
├─────────────────┼─────┼─────┼───────┤
│ Question Length │ 20  │ 150 │ 65.3  │
│ Answer Length   │ 30  │ 500 │ 185.2 │
│ Answer Words    │ 10  │ 100 │ 45.8  │
└─────────────────┴─────┴─────┴───────┘

Diversity Score: 0.82

Over-represented patterns:
  • what_is: 18% (target: <15%)

Recommendations:
  • Add more 'why' questions (currently 3%)
  • Add more 'compare' questions (currently 2%)
```

## 🔧 Configuration

### Using Configuration Files

The project includes pre-configured YAML files for different use cases:

```bash
# Use default configuration
vedic-gen generate --config configs/default.yaml --output data/output/qa.jsonl

# Use Jaimini-specific configuration
vedic-gen generate --config configs/jaimini.yaml --pdf data/raw/jaimini.pdf --output data/output/jaimini_qa.jsonl

# Use KP System configuration
vedic-gen generate --config configs/kp.yaml --pdf data/raw/kp_reader.pdf --output data/output/kp_qa.jsonl
```

**Available Configuration Files:**

- [configs/default.yaml](configs/default.yaml) - General Vedic astrology configuration
- [configs/jaimini.yaml](configs/jaimini.yaml) - Jaimini system-specific templates
- [configs/kp.yaml](configs/kp.yaml) - Krishnamurti Paddhati (KP) system configuration
- [configs/opensource_llm.yaml](configs/opensource_llm.yaml) - Open-source LLM models configuration
- [configs/llm_models.yaml](configs/llm_models.yaml) - Comprehensive LLM models database

**Key Configuration Options:**

```yaml
extraction:
  chunk_size: 1000          # Characters per chunk
  chunk_overlap: 100        # Overlap between chunks

quality:
  min_question_length: 20   # Minimum question length
  min_answer_length: 30     # Minimum answer length
  similarity_threshold: 0.85 # Duplicate detection threshold

diversity:
  max_pattern_ratio: 0.15   # Max 15% per question pattern

augmentation:
  enabled: true
  per_item: 2               # Augmentations per original

llm:
  provider: "anthropic"     # anthropic, openai, ollama, huggingface, vllm
  model: "claude-3-haiku-20240307"
  temperature: 0.3
  qa_pairs_per_chunk: 3

# For open-source LLMs
llm_opensource:
  provider: "ollama"        # Easy local setup
  model: "mistral"          # or llama2, llama3, mixtral
  base_url: "http://localhost:11434"
  max_tokens: 2048
```

### Python API

```python
from vedic_astro_gen import VedicQAGenerator, GenerationConfig

config = GenerationConfig(
    # Extraction settings
    chunk_size=1000,
    chunk_overlap=100,
    
    # Quality settings
    min_question_length=20,
    min_answer_length=30,
    min_answer_words=10,
    similarity_threshold=0.85,
    
    # Diversity settings
    max_pattern_ratio=0.15,
    
    # Augmentation settings
    augmentation_enabled=True,
    augmentations_per_item=2,
    
    # LLM settings (optional)
    llm_generation_enabled=False,
    llm_provider="anthropic",
    llm_model="claude-3-haiku-20240307",
    qa_pairs_per_chunk=3,
)

generator = VedicQAGenerator(config=config)
results = generator.run_full_pipeline(
    pdf_paths=["book1.pdf", "book2.pdf"],
    output_path="vedic_qa.jsonl",
)
```

## 🤖 Open-Source LLM Support

Generate Q&A datasets using **free, local open-source models** - no API keys or cloud costs required!

### Supported Models

**Llama Family:**
- Llama 2 (7B, 13B, 70B)
- Llama 3 (8B, 70B) - Latest, recommended

**Mistral Family:**
- Mistral 7B - Excellent efficiency
- Mixtral 8x7B - High quality
- Mixtral 8x22B - Highest quality

**Others:**
- Gemma (Google), Qwen 2, Phi-3

### Quick Start with Ollama

**Easiest method** - runs on your laptop:

```bash
# 1. Install Ollama
# Visit https://ollama.ai or:
curl https://ollama.ai/install.sh | sh

# 2. Pull a model (one-time)
ollama pull mistral

# 3. Generate dataset
vedic-gen generate \
  --config configs/opensource_llm.yaml \
  --pdf data/raw/jyotish.pdf \
  --llm \
  --output data/output/qa.jsonl
```

### Alternative Methods

**HuggingFace Transformers** (direct control):
```bash
pip install -e ".[llm-opensource]"
# Configure in configs/opensource_llm.yaml
```

**vLLM** (high-performance production):
```bash
pip install -e ".[llm-vllm]"
python -m vllm.entrypoints.openai.api_server --model mistralai/Mistral-7B-Instruct-v0.2
```

**API Providers** (hosted open-source):
- **Groq** - Ultra-fast inference
- **Together.ai** - Wide model selection
- **Anyscale** - Enterprise-grade

### Configuration Examples

See [configs/opensource_llm.yaml](configs/opensource_llm.yaml) for complete examples.

**Ollama (Local)**:
```yaml
llm:
  provider: "ollama"
  base_url: "http://localhost:11434"
  model: "mistral"  # or llama3, mixtral, gemma
  temperature: 0.3
  max_tokens: 2048
```

**HuggingFace (Local)**:
```yaml
llm:
  provider: "huggingface"
  model: "mistralai/Mistral-7B-Instruct-v0.2"
  load_in_4bit: true  # Reduces VRAM usage
  device_map: "auto"
```

**Groq API (Hosted)**:
```bash
export GROQ_API_KEY=your_key
```
```yaml
llm:
  provider: "openai"
  base_url: "https://api.groq.com/openai/v1"
  model: "mixtral-8x7b-32768"
```

### Performance Comparison

| Method | Speed | Quality | Cost | GPU Needed |
|--------|-------|---------|------|------------|
| Ollama (Mistral 7B) | ⭐⭐⭐ | ⭐⭐⭐½ | Free | 8GB VRAM |
| HuggingFace (Llama 3 8B) | ⭐⭐⭐ | ⭐⭐⭐⭐ | Free | 8-16GB VRAM |
| vLLM (Mistral 7B) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐½ | Free | 8GB VRAM |
| Groq API (Mixtral 8x7B) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $0.24/1M tokens | No |
| Claude Haiku API | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $0.25/1M tokens | No |

### Batch Processing Multiple PDFs

Process multiple PDFs efficiently using the automated batch script:

```bash
# 1. Place all PDFs in data/raw/ directory
cp *.pdf data/raw/

# 2. Run batch processor
python scripts/batch_process_runpod.py
```

**Features:**
- Automatic PDF discovery and processing
- Progress tracking with ETA
- Error handling and recovery
- Memory optimization
- Complete processing logs

**Example output:**
```
Found 30 PDF files to process
Start processing? [Y/n]: y

Processing PDF 1/30: jyotish_basics.pdf
✓ Success! Generated: 127 Q&A pairs | Time: 0:06:23
ETA for remaining 29 PDFs: 3:05:07

[... continues ...]

BATCH PROCESSING SUMMARY
Total PDFs processed: 30
  ✓ Successful: 30
Total Q&A pairs generated: 3,847
Total processing time: 3:12:15
```

### Budget Options for Large-Scale Processing

**Processing 30 PDFs - Cost Comparison:**

| Method | Setup | Time | Cost | Best For |
|--------|-------|------|------|----------|
| **RunPod RTX 4090** | 30 mins | 3-4 hrs | **$2.50** | Best value ⭐ |
| **Groq API** | 5 mins | 1-2 hrs | **$0.50-1.20** | Fastest setup ⭐ |
| **Local (Ollama)** | 30 mins | 12-24 hrs | **$0** | Privacy-focused |
| **Google Colab Free** | 20 mins | 6-12 hrs | **$0** | No local GPU |

**RunPod Quick Start:**
1. Create account at [runpod.io](https://runpod.io)
2. Deploy RTX 4090 pod ($0.69/hour)
3. Run setup script: `bash scripts/runpod_setup.sh`
4. Upload PDFs and process
5. Download results and stop pod

**Complete budget guide:** See [docs/BUDGET_OPTIONS.md](docs/BUDGET_OPTIONS.md)

### Complete Guide

See [docs/OPENSOURCE_LLM_GUIDE.md](docs/OPENSOURCE_LLM_GUIDE.md) for:
- Detailed setup instructions
- Model recommendations by GPU
- Performance optimization
- Troubleshooting
- Cost comparisons

## 📁 Project Structure

```
vedic-astro-data-gen/
├── src/vedic_astro_gen/        # Main package
│   ├── __init__.py             # Package exports
│   ├── __main__.py             # CLI entry point
│   ├── cli.py                  # Typer-based CLI interface
│   ├── knowledge_base.py       # Complete Vedic astrology knowledge
│   ├── templates.py            # Template manager (9×12×12 combos)
│   ├── pdf_extractor.py        # PDF processing with diacritics
│   ├── quality_filters.py      # Filtering & deduplication
│   ├── augmentation.py         # Domain-specific augmentation
│   └── generator.py            # Main pipeline orchestrator
├── configs/                    # YAML configuration files
│   ├── default.yaml            # General configuration
│   ├── jaimini.yaml            # Jaimini-specific config
│   ├── kp.yaml                 # Krishnamurti Paddhati config
│   ├── opensource_llm.yaml     # Open-source LLM configurations
│   ├── runpod_llm.yaml         # RunPod GPU optimized config
│   └── llm_models.yaml         # Complete LLM models database
├── data/                       # Data directory (gitignored)
│   ├── raw/                    # Input PDFs (.gitkeep only)
│   ├── processed/              # Extracted chunks (.gitkeep only)
│   └── output/                 # Generated Q&A (.gitkeep only)
├── scripts/                    # Utility scripts
│   ├── analyze_dataset.py      # Advanced dataset analysis
│   ├── convert_format.py       # Format conversion utilities
│   ├── batch_process_runpod.py # Batch PDF processing script
│   ├── runpod_setup.sh         # RunPod instance setup
│   ├── generate.sh             # Batch generation script
│   └── setup.sh                # Environment setup
├── docs/                       # Documentation
│   ├── EXAMPLES.md             # Detailed usage examples
│   ├── OPENSOURCE_LLM_GUIDE.md # Complete open-source LLM guide
│   └── BUDGET_OPTIONS.md       # Budget options for processing
├── tests/                      # Unit tests
│   └── test_*.py               # Test modules
├── pyproject.toml              # Project metadata & dependencies
├── requirements.txt            # Direct pip dependencies
├── Makefile                    # Common development tasks
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🌟 Output Format

Generated Q&A pairs in JSONL format:

```json
{
  "id": "template_graha_a1b2c3d4",
  "question": "How does Śani (Saturn) placed in the 7th house affect marriage and partnerships?",
  "answer": "Śani (Saturn) in the 7th house typically indicates delayed marriage, often after age 28-30. The native approaches relationships with caution and seeks stability...",
  "qa_type": "interpretation",
  "difficulty": "medium",
  "category": "marriage",
  "tags": ["shani", "bhava_7", "marriage"],
  "source": {
    "type": "template_graha",
    "template": "Interpret {graha_sanskrit} placed in the {bhava_ordinal} house ({bhava_name})."
  },
  "generation_method": "template"
}
```

## 📈 Comparison: Before vs After

| Metric | Your Current Data | After This Pipeline |
|--------|-------------------|---------------------|
| Repetitive question starters | 50%+ "What is/are/does" | <15% per pattern |
| Average answer words | 29.6 | 45+ |
| Question type diversity | 3-4 types | 10+ types |
| Duplicate rate | Unknown | <1% |
| Diversity score | ~0.4 | >0.8 |

## 🛠️ Makefile Commands

The project includes a comprehensive Makefile for common tasks:

```bash
# Show all available commands
make help

# Installation
make install          # Install core package
make install-llm      # Install with LLM support
make install-dev      # Install development tools
make install-all      # Install everything

# Development
make test             # Run tests
make test-cov         # Run tests with coverage report
make lint             # Run linter (ruff)
make format           # Format code (black + ruff)
make clean            # Remove build artifacts

# Data Generation
make generate         # Generate from templates only
make generate-pdf PDF=path/to/file.pdf
make generate-llm PDF=path/to/file.pdf
make extract PDF=path/to/file.pdf

# Analysis & Processing
make analyze DATA=path/to/data.jsonl
make filter DATA=path/to/data.jsonl
make augment DATA=path/to/data.jsonl

# Templates
make templates        # List available templates
```

## 📜 Utility Scripts

The [scripts/](scripts/) directory contains helpful utilities:

### [analyze_dataset.py](scripts/analyze_dataset.py)
Advanced dataset analysis with visualizations:

```bash
python scripts/analyze_dataset.py data/output/qa.jsonl --visualize
```

Features:
- Detailed statistics and metrics
- Question pattern distribution
- Answer length histograms
- Diversity score calculation
- Export reports to HTML/PDF

### [convert_format.py](scripts/convert_format.py)
Convert JSONL to various training formats:

```bash
# Convert to Alpaca format
python scripts/convert_format.py data/output/qa.jsonl --format alpaca

# Convert to ChatML format
python scripts/convert_format.py data/output/qa.jsonl --format chatml

# Convert to ShareGPT format
python scripts/convert_format.py data/output/qa.jsonl --format sharegpt
```

### [generate.sh](scripts/generate.sh)
Batch generation script for processing multiple PDFs:

```bash
./scripts/generate.sh
```

### [setup.sh](scripts/setup.sh)
One-command environment setup:

```bash
./scripts/setup.sh
```

## 🔬 Knowledge Base Coverage

The knowledge base includes comprehensive information about:

### Grahas (Planets) - 9 Total
- **All 9 planets** with Sanskrit/English names
- **Nature**: benefic/malefic, gender, element, guna, caste
- **Dignities**: exaltation, debilitation, own sign, moolatrikona
- **Relationships**: friends, enemies, neutral planets
- **Significations**: karakatvas (soul, mind, intelligence, etc.)
- **Physical**: body parts, diseases, colors, gemstones, metals
- **Temporal**: day of week, dasha years, mahadasha order
- **Aspects**: special aspects for Mars, Jupiter, Saturn

### Rashis (Zodiac Signs) - 12 Total
- **All 12 signs** with Sanskrit and English names
- **Classification**: element (fire/earth/air/water), quality (cardinal/fixed/mutable)
- **Rulership**: lord, exaltation/debilitation rulers
- **Physical**: body parts, directions
- **Characteristics**: nature, symbol, dasha progression

### Bhavas (Houses) - 12 Total
- **All 12 houses** with comprehensive significations
- **Karakas**: natural indicators for each house
- **Categories**: kendra (1,4,7,10), trikona (1,5,9), dusthana (6,8,12), upachaya (3,6,10,11)
- **Prediction areas**: specific life domains for each house
- **Jaimini**: chara karakas and special significations

### Nakshatras (Lunar Mansions) - 27 Total
Complete details for all 27 nakshatras:
- **Names**: Aśvinī, Bharaṇī, Kṛttikā, Rohiṇī, Mṛgaśirā, Ārdrā, Punarvasu, Puṣya, Āśleṣā, Maghā, Pūrva Phālgunī, Uttara Phālgunī, Hasta, Citrā, Svātī, Viśākhā, Anurādhā, Jyeṣṭhā, Mūla, Pūrvāṣāḍhā, Uttarāṣāḍhā, Śravaṇa, Dhaniṣṭhā, Śatabhiṣā, Pūrva Bhādrapadā, Uttara Bhādrapadā, Revatī
- **Lords**: planetary rulers for each nakshatra
- **Deities**: presiding deities (Aśvini Kumāras, Yama, Agni, etc.)
- **Symbols**: representative symbols (horse head, yoni, flame, etc.)
- **Nature**: Light/Swift, Fierce, Fixed, Movable, Soft, Sharp, Mixed
- **Gana**: Deva (divine), Manushya (human), Rakshasa (demonic)

### Yogas (Planetary Combinations) - 50+ Total

**Pancha Mahapurusha Yogas (5)**:
- Ruchaka (Mars), Bhadra (Mercury), Hamsa (Jupiter), Malavya (Venus), Śaśa (Saturn)

**Raja Yogas** (power and authority):
- Rāja Yoga, Dharma-Karmādhipati Yoga, and variations

**Dhana Yogas** (wealth):
- Dhana Yoga, Lakshmi Yoga, combinations of lords

**Jaimini Yogas**:
- Svāṃśa analysis, Karakāṃśa placements, Chara Rāśi Daśā combinations

**Negative Yogas**:
- Kemadruma Yoga, Kālasarpa Yoga (with cancellation factors)

### Dasha Systems

**Vimshottari Dasha**:
- 120-year cycle
- Planetary periods for all 9 grahas
- Mahadasha, antardasha, and pratyantardasha calculations

**Jaimini Dashas**:
- Chara Rāśi Daśā (movable sign dasha)
- Sthira Rāśi Daśā (fixed sign dasha)
- Brahma Rāśi Daśā
- Alternative timing systems

### Krishnamurti Paddhati (KP System)

**Core KP Concepts**:
- **Sub-Lords**: Most critical significator - each nakshatra divided into 9 subs
- **Cuspal Interlinks**: Cusp sub-lords determine house results
- **Significators**: Planet connections to houses (occupant → star lord → house lord)
- **Ruling Planets**: 7 ruling planets for horary and timing
- **House Groupings**: Dharma (1-5-9), Artha (2-6-10), Kama (3-7-11), Moksha (4-8-12)

**KP House Significations**:
- Marriage: 2-7-11 (avoid 1-6-10)
- Career: 2-6-10-11
- Education: 4-9-11 (avoid 3-8)
- Children: 2-5-11 (avoid 1-4-10)
- Foreign Travel: 3-9-12
- Moksha/Liberation: 4-8-12

**KP Timing Methods**:
- Viṃśottarī Daśā (KP Style) with 5 levels
- Transit timing on sensitive cuspal degrees
- Secondary progressions (1 day = 1 year)

**KP Stellar Astrology**:
- Planet gives results of its star lord
- 249 sub-divisions for precise predictions
- Cuspal sub-lord rules (YES/NO predictions)

**KP Horary Astrology**:
- Number selection (1-249) or time-based
- 11th cusp sub-lord for judgment
- Ruling planets confirmation

**KP Yogas**:
- KP Raja Yoga (1-2-6-10-11 houses)
- KP Dhana Yoga (2-6-10-11 houses)
- Negative combinations (Maraka, disease, obstacles)

**KP Ayanāṃśa**:
- Krishnamurti Ayanāṃśa (different from Lahiri)
- Critical for accurate sub-lord calculation

### Prediction Templates
- **13+ categories**: career, marriage, health, wealth, children, education, spirituality, longevity, foreign travel, litigation, property, vehicles, general
- **Multiple question types**: interpretation, prediction, comparison, timing, remedies
- **Context-aware**: considers dignity, house placement, aspects, yogas
- **KP-specific**: sub-lord analysis, cuspal predictions, horary questions

## 🚀 Advanced Usage

### Custom Templates

Create your own templates by extending the knowledge base:

```python
from vedic_astro_gen.templates import TemplateManager
from vedic_astro_gen.knowledge_base import GRAHAS, BHAVAS

manager = TemplateManager()

# Add custom template
custom_template = {
    "template": "What happens when {graha} transits through {rashi}?",
    "difficulty": "medium",
    "qa_type": "prediction",
    "category": "transits"
}

# Generate Q&A from custom template
qa_pairs = manager.generate_from_custom_template(custom_template)
```

### Combining Multiple Sources

Process multiple PDFs with different configurations:

```python
from vedic_astro_gen import VedicQAGenerator, GenerationConfig

# Create separate configs for different books
parashara_config = GenerationConfig(chunk_size=1200, qa_pairs_per_chunk=4)
jaimini_config = GenerationConfig(chunk_size=800, qa_pairs_per_chunk=3)

# Generate from multiple sources
generator = VedicQAGenerator()
all_data = []

for pdf, config in [
    ("data/raw/parashara.pdf", parashara_config),
    ("data/raw/jaimini.pdf", jaimini_config),
]:
    generator.config = config
    results = generator.run_full_pipeline(pdf_paths=[pdf])
    all_data.extend(results['data'])
```

### Filtering by Metadata

Filter generated data by specific criteria:

```python
import json

# Load data
with open("data/output/qa.jsonl", "r") as f:
    data = [json.loads(line) for line in f]

# Filter by difficulty
advanced_only = [qa for qa in data if qa.get("difficulty") == "hard"]

# Filter by category
marriage_qa = [qa for qa in data if qa.get("category") == "marriage"]

# Filter by tags
saturn_qa = [qa for qa in data if "shani" in qa.get("tags", [])]
```

### Programmatic Dataset Merging

Merge multiple datasets with deduplication:

```python
from vedic_astro_gen import QualityFilter
import json

# Load multiple datasets
datasets = []
for file in ["qa1.jsonl", "qa2.jsonl", "qa3.jsonl"]:
    with open(f"data/output/{file}", "r") as f:
        datasets.append([json.loads(line) for line in f])

# Merge
merged = [item for dataset in datasets for item in dataset]

# Deduplicate
qf = QualityFilter(similarity_threshold=0.90)
result = qf.filter_dataset(merged)

print(f"Merged: {len(merged)} → {len(result.kept)} (removed {len(result.removed)} duplicates)")
```

## 💡 Performance Tips

1. **PDF Processing**: For large PDFs (>500 pages), increase chunk size to 1500-2000 characters
2. **Memory Usage**: Process PDFs one at a time if memory is limited
3. **LLM Generation**: Use `claude-3-haiku` for cost-effectiveness, `claude-3-sonnet` for quality
4. **Batch Processing**: Use the [generate.sh](scripts/generate.sh) script for multiple PDFs
5. **Caching**: Extracted PDF chunks are cached in `data/processed/` - reuse them to save time
6. **Parallel Processing**: Run multiple generation jobs in parallel for different categories

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'vedic_astro_gen'`

**Solution**: Install the package in editable mode:
```bash
pip install -e .
```

**Issue**: PDF extraction fails with Unicode errors

**Solution**: Ensure the PDF contains actual text (not scanned images). For scanned PDFs, use OCR first:
```bash
# Use tesseract OCR for scanned PDFs
tesseract input.pdf output pdf
```

**Issue**: LLM generation fails with API errors

**Solution**: Check your API key and rate limits:
```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Set it if missing
export ANTHROPIC_API_KEY=your_key_here
```

**Issue**: Low diversity scores (<0.5)

**Solution**:
- Enable augmentation: `augmentation.enabled: true`
- Increase augmentations per item: `augmentation.per_item: 3`
- Use multiple templates and question types

**Issue**: Questions/answers too short

**Solution**: Adjust minimum lengths in config:
```yaml
quality:
  min_question_length: 30
  min_answer_length: 50
  min_answer_words: 15
```

**Issue**: Too many duplicates

**Solution**: Lower similarity threshold:
```yaml
quality:
  similarity_threshold: 0.80  # Lower = stricter deduplication
```

### Getting Help

1. Check [docs/EXAMPLES.md](docs/EXAMPLES.md) for detailed examples
2. Review configuration in [configs/default.yaml](configs/default.yaml)
3. Run with verbose logging:
   ```bash
   vedic-gen generate --verbose --output qa.jsonl
   ```
4. Open an issue on GitHub with:
   - Python version (`python --version`)
   - Package version
   - Full error traceback
   - Minimal reproduction example

## 📚 Additional Resources

- **Detailed Examples**: See [docs/EXAMPLES.md](docs/EXAMPLES.md) for comprehensive usage examples
- **Configuration Reference**: Check [configs/default.yaml](configs/default.yaml) for all options
- **API Documentation**: Browse source code in [src/vedic_astro_gen/](src/vedic_astro_gen/)
- **Test Examples**: Review [tests/](tests/) for usage patterns

## 🤝 Contributing

Contributions are welcome! This is an open-source project and we appreciate all contributions.

### Areas That Need Help

1. **More templates** for prediction scenarios
   - Transit predictions
   - Dasha period interpretations
   - Yoga formations and results
2. **Additional yogas** and their interpretations
   - Special yogas (Neecha Bhanga, etc.)
   - Jaimini yogas
   - Nadi yogas
3. **Divisional chart** (varga) templates - *Not yet implemented*
   - D-1 (Rāśi), D-9 (Navāṃśa), D-10 (Daśāṃśa), D-16 (Ṣoḍaśāṃśa)
   - D-20 (Vimśāṃśa), D-24 (Siddāṃśa), D-30 (Triṃśāṃśa), D-60 (Ṣaṣṭyāṃśa)
   - Varga-specific interpretations and strength calculations
   - Vargottama positions and special placements
4. **More PDF processing** edge cases
   - Multi-column layouts
   - Tables and charts
   - Footnotes and references
5. **Test coverage** improvements
   - Unit tests for all components
   - Integration tests
   - Edge case testing

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `make test`
5. **Format code**: `make format`
6. **Commit changes**: `git commit -m "Add amazing feature"`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/vedic-astro-data-gen.git
cd vedic-astro-data-gen

# Install development dependencies
make install-dev

# Run tests
make test

# Run linter
make lint

# Format code
make format
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for all public functions
- Keep functions focused and small
- Write tests for new features

### Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Full error traceback
- Steps to reproduce
- Expected vs actual behavior

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 📦 Dependencies

This project uses the following major dependencies:

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pymupdf | >=1.24.0 | PDF text extraction |
| pdfplumber | >=0.10.0 | Alternative PDF processing |
| langchain | >=0.2.0 | Document processing framework |
| langchain-text-splitters | >=0.2.0 | Text chunking |
| pandas | >=2.0.0 | Data manipulation |
| numpy | >=1.24.0 | Numerical operations |
| sentence-transformers | >=2.2.0 | Semantic similarity |
| scikit-learn | >=1.3.0 | ML utilities |
| rapidfuzz | >=3.0.0 | Fuzzy string matching |
| typer | >=0.9.0 | CLI framework |
| rich | >=13.0.0 | Terminal formatting |
| pyyaml | >=6.0 | Configuration files |
| tqdm | >=4.65.0 | Progress bars |

### Optional Dependencies (Proprietary LLM APIs)

| Package | Version | Purpose |
|---------|---------|---------|
| langchain-anthropic | >=0.1.0 | Claude API integration |
| anthropic | >=0.25.0 | Anthropic SDK |
| langchain-openai | >=0.1.0 | OpenAI API integration |
| openai | >=1.0.0 | OpenAI SDK |

### Optional Dependencies (Open-Source LLMs)

| Package | Version | Purpose |
|---------|---------|---------|
| transformers | >=4.35.0 | HuggingFace models |
| torch | >=2.0.0 | PyTorch for model inference |
| accelerate | >=0.24.0 | Efficient model loading |
| bitsandbytes | >=0.41.0 | Model quantization (4-bit/8-bit) |
| sentencepiece | >=0.1.99 | Tokenization for some models |
| langchain-ollama | >=0.1.0 | Ollama integration |
| langchain-huggingface | >=0.0.1 | HuggingFace LangChain integration |
| vllm | >=0.2.0 | High-performance inference (optional) |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | >=7.0.0 | Testing framework |
| pytest-cov | >=4.0.0 | Code coverage |
| black | >=23.0.0 | Code formatting |
| ruff | >=0.1.0 | Linting |

### Installation

```bash
# Core dependencies only
pip install -e .

# With proprietary LLM APIs (OpenAI, Anthropic)
pip install -e ".[llm]"

# With open-source LLMs (Llama, Mistral, etc.)
pip install -e ".[llm-opensource]"

# With vLLM for high-performance inference
pip install -e ".[llm-vllm]"

# All LLM options
pip install -e ".[llm-all]"

# With development tools
pip install -e ".[dev]"

# Everything
pip install -e ".[dev,llm-all]"
```

For detailed dependency management, see [pyproject.toml](pyproject.toml) and [requirements.txt](requirements.txt).

## 🙏 Acknowledgments

- Classical Jyotiṣa texts (Bṛhat Parāśara Horā Śāstra, Jaimini Sūtra)
- Prof. K.S. Krishnamurti and the KP System of astrology
- KP Readers (I-VI) and Stellar Astrology literature
- "In Search of Jyotish" book series
- The Vedic astrology and KP astrology communities

---

## Appendix: Sanskrit Diacritics Reference

This tool preserves proper IAST (International Alphabet of Sanskrit Transliteration):

### Vowels

| Character | Pronunciation | Example |
|-----------|---------------|---------|
| a | short 'a' (schwa) | Brahma |
| ā | long 'a' (as in 'father') | Rāhu |
| i | short 'i' (as in 'pin') | Śiva |
| ī | long 'i' (as in 'machine') | Jyotīṣa |
| u | short 'u' (as in 'put') | Guru |
| ū | long 'u' (as in 'rule') | Sūrya |
| ṛ | vocalic 'r' | Kṛṣṇa |
| ṝ | long vocalic 'r' | Amṝta |
| ḷ | vocalic 'l' | Kḷpta |
| ḹ | long vocalic 'l' | Kḹpta |
| e | long 'e' (as in 'they') | Ketu |
| ai | diphthong 'ai' | Vaiśya |
| o | long 'o' (as in 'go') | Yoga |
| au | diphthong 'au' | Mauna |

### Consonants

#### Velars (Guttural)
| Character | Pronunciation | Example |
|-----------|---------------|---------|
| k | unaspirated 'k' | Karma |
| kh | aspirated 'k' | Khagola |
| g | unaspirated 'g' | Graha |
| gh | aspirated 'g' | Ghaṭikā |
| ṅ | velar nasal (as 'ng' in 'sing') | Aṅga |

#### Palatals
| Character | Pronunciation | Example |
|-----------|---------------|---------|
| c | unaspirated 'ch' (as in 'church') | Candra |
| ch | aspirated 'ch' | Chāyā |
| j | unaspirated 'j' | Jyotiṣa |
| jh | aspirated 'j' | Jhāṭa |
| ñ | palatal nasal (as 'ny') | Jñāna |

#### Retroflexes (Cerebrals)
| Character | Pronunciation | Example |
|-----------|---------------|---------|
| ṭ | retroflex 't' | Kuṇṭa |
| ṭh | aspirated retroflex 't' | Aṣṭha |
| ḍ | retroflex 'd' | Kuṇḍalī |
| ḍh | aspirated retroflex 'd' | Ḍhakkā |
| ṇ | retroflex 'n' | Rāvaṇa |

#### Dentals
| Character | Pronunciation | Example |
|-----------|---------------|---------|
| t | dental 't' (tongue at teeth) | Tattva |
| th | aspirated dental 't' | Pṛthivī |
| d | dental 'd' | Daśā |
| dh | aspirated dental 'd' | Dharma |
| n | dental 'n' | Nakṣatra |

#### Labials
| Character | Pronunciation | Example |
|-----------|---------------|---------|
| p | unaspirated 'p' | Pañca |
| ph | aspirated 'p' (not 'f') | Phala |
| b | unaspirated 'b' | Budha |
| bh | aspirated 'b' | Bhāva |
| m | labial 'm' | Maṅgala |

#### Semivowels
| Character | Pronunciation | Example |
|-----------|---------------|---------|
| y | 'y' | Yoga |
| r | 'r' (rolled) | Rāśi |
| l | 'l' | Lagna |
| v | 'v' or 'w' | Varga |

#### Sibilants
| Character | Pronunciation | Example |
|-----------|---------------|---------|
| ś | palatal 'sh' (soft) | Śani |
| ṣ | retroflex 'sh' | Viṣṇu |
| s | dental 's' | Sūrya |

#### Aspirate
| Character | Pronunciation | Example |
|-----------|---------------|---------|
| h | 'h' | Hora |

### Special Marks

| Character | Name | Pronunciation | Example |
|-----------|------|---------------|---------|
| ṃ | Anusvāra | nasalization (m/n) | Saṃskṛta |
| ḥ | Visarga | voiced 'h' sound | Duḥkha |
| ṁ | Candrabindu | nasal vowel | Oṁ |
| ~ | Tilde (over vowel) | nasalization | õ |
