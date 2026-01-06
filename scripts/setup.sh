#!/bin/bash
# =============================================================================
# Vedic Astrology Data Generator - Setup Script
# =============================================================================
# This script installs all dependencies and verifies the installation.
# Usage: bash scripts/setup.sh
# =============================================================================

set -e

echo "=============================================="
echo "Vedic Astrology Data Generator - Setup"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
major=$(echo "$python_version" | cut -d'.' -f1)
minor=$(echo "$python_version" | cut -d'.' -f2)

if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 10 ]); then
    echo -e "${RED}Error: Python 3.10 or higher is required (found $python_version)${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $python_version${NC}"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install the package
echo -e "\n${YELLOW}Installing vedic-astro-data-gen...${NC}"
pip install -e .

# Install optional LLM dependencies
echo -e "\n${YELLOW}Installing LLM dependencies (optional)...${NC}"
pip install -e ".[llm]" 2>/dev/null || echo -e "${YELLOW}LLM dependencies skipped${NC}"

# Install dev dependencies
echo -e "\n${YELLOW}Installing development dependencies...${NC}"
pip install -e ".[dev]" 2>/dev/null || echo -e "${YELLOW}Dev dependencies skipped${NC}"

# Verify installation
echo -e "\n${YELLOW}Verifying installation...${NC}"

# Check core imports
python3 -c "from vedic_astro_gen import VedicQAGenerator; print('✓ Core package')"
python3 -c "from vedic_astro_gen.knowledge_base import GRAHAS; print(f'✓ Knowledge base ({len(GRAHAS)} grahas)')"
python3 -c "from vedic_astro_gen.templates import TemplateManager; print('✓ Templates')"
python3 -c "from vedic_astro_gen.pdf_extractor import VedicPDFExtractor; print('✓ PDF Extractor')"
python3 -c "from vedic_astro_gen.quality_filters import QualityFilter; print('✓ Quality Filters')"
python3 -c "from vedic_astro_gen.augmentation import VedicAugmenter; print('✓ Augmentation')"

# Check CLI
echo -e "\n${YELLOW}Checking CLI...${NC}"
vedic-gen --help > /dev/null && echo -e "${GREEN}✓ CLI available${NC}"

# Check optional dependencies
echo -e "\n${YELLOW}Checking optional dependencies...${NC}"
python3 -c "import fitz; print('✓ PyMuPDF')" 2>/dev/null || echo "  PyMuPDF not available (PDF extraction may be limited)"
python3 -c "import sentence_transformers; print('✓ Sentence Transformers')" 2>/dev/null || echo "  Sentence Transformers not available (semantic dedup disabled)"
python3 -c "import rapidfuzz; print('✓ RapidFuzz')" 2>/dev/null || echo "  RapidFuzz not available (fuzzy matching disabled)"

# Check LLM dependencies
echo -e "\n${YELLOW}Checking LLM dependencies...${NC}"
python3 -c "import langchain_anthropic; print('✓ LangChain Anthropic')" 2>/dev/null || echo "  LangChain Anthropic not available"
python3 -c "import langchain_openai; print('✓ LangChain OpenAI')" 2>/dev/null || echo "  LangChain OpenAI not available"

echo -e "\n=============================================="
echo -e "${GREEN}Setup complete!${NC}"
echo -e "=============================================="
echo -e "\nTo activate the environment in future sessions:"
echo -e "  ${YELLOW}source venv/bin/activate${NC}"
echo -e "\nTo generate Q&A data:"
echo -e "  ${YELLOW}vedic-gen generate --output data/output/vedic_qa.jsonl${NC}"
echo -e "\nTo run tests:"
echo -e "  ${YELLOW}pytest tests/ -v${NC}"
