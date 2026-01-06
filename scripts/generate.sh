#!/bin/bash
# =============================================================================
# Vedic Astrology Data Generator - Generation Script
# =============================================================================
# Generates high-quality Vedic astrology Q&A data for LLM fine-tuning.
# Usage: bash scripts/generate.sh [options]
# =============================================================================

set -e

# Default values
OUTPUT_DIR="data/output"
PDF_PATH=""
USE_LLM=false
AUGMENT=true
AUGMENT_COUNT=2
CONFIG="configs/default.yaml"
SEED=42
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --pdf)
            PDF_PATH="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --llm)
            USE_LLM=true
            shift
            ;;
        --no-augment)
            AUGMENT=false
            shift
            ;;
        --augment-count)
            AUGMENT_COUNT="$2"
            shift 2
            ;;
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --seed)
            SEED="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --pdf PATH         PDF file to extract from"
            echo "  --output DIR       Output directory (default: data/output)"
            echo "  --llm              Enable LLM-based generation"
            echo "  --no-augment       Disable augmentation"
            echo "  --augment-count N  Augmentations per item (default: 2)"
            echo "  --config PATH      Config file path"
            echo "  --seed N           Random seed (default: 42)"
            echo "  --verbose, -v      Enable verbose output"
            echo "  --help, -h         Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Build command
CMD="vedic-gen generate --output ${OUTPUT_DIR}/vedic_qa.jsonl --seed $SEED --augment-count $AUGMENT_COUNT"

if [ -n "$PDF_PATH" ]; then
    CMD="$CMD --pdf $PDF_PATH"
fi

if [ "$USE_LLM" = true ]; then
    CMD="$CMD --llm"
fi

if [ "$AUGMENT" = false ]; then
    CMD="$CMD --no-augment"
fi

if [ "$VERBOSE" = true ]; then
    CMD="$CMD --verbose"
fi

# Print configuration
echo "=============================================="
echo "Vedic Astrology Data Generation"
echo "=============================================="
echo "Output directory: $OUTPUT_DIR"
echo "PDF path: ${PDF_PATH:-None}"
echo "Use LLM: $USE_LLM"
echo "Augmentation: $AUGMENT (count: $AUGMENT_COUNT)"
echo "Seed: $SEED"
echo "=============================================="

# Run generation
echo ""
echo "Running: $CMD"
echo ""
$CMD

# Post-generation analysis
echo ""
echo "=============================================="
echo "Post-Generation Analysis"
echo "=============================================="
vedic-gen analyze "${OUTPUT_DIR}/vedic_qa.jsonl"

echo ""
echo "=============================================="
echo "Generation Complete!"
echo "=============================================="
echo "Output: ${OUTPUT_DIR}/vedic_qa.jsonl"
echo ""
echo "Next steps:"
echo "  1. Review the generated data"
echo "  2. Adjust config if needed and re-run"
echo "  3. Use data for fine-tuning your model"
