#!/bin/bash
# ============================================================================
# RunPod Setup Script
# ============================================================================
# Automated setup for RunPod GPU instances
# Run this script immediately after connecting to your RunPod instance
#
# Usage:
#   chmod +x scripts/runpod_setup.sh
#   ./scripts/runpod_setup.sh
# ============================================================================

set -e  # Exit on error

echo "========================================="
echo "RunPod Setup for Vedic Astrology Data Generator"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on RunPod
if [ ! -d "/workspace" ]; then
    echo -e "${RED}Warning: /workspace not found. This may not be a RunPod instance.${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 1: System Update
echo -e "${BLUE}[1/7] Updating system packages...${NC}"
apt-get update -qq
apt-get install -y -qq git wget curl > /dev/null 2>&1
echo -e "${GREEN}✓ System updated${NC}"

# Step 2: Check GPU
echo -e "${BLUE}[2/7] Checking GPU...${NC}"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    echo -e "${GREEN}✓ GPU detected${NC}"
else
    echo -e "${RED}✗ No GPU found!${NC}"
    exit 1
fi

# Step 3: Python Environment
echo -e "${BLUE}[3/7] Setting up Python environment...${NC}"

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Installing Miniconda..."
    wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3
    export PATH="/root/miniconda3/bin:$PATH"
    rm Miniconda3-latest-Linux-x86_64.sh
fi

# Initialize conda
export PATH="/root/miniconda3/bin:$PATH"
conda init bash > /dev/null 2>&1
source ~/.bashrc

echo -e "${GREEN}✓ Python environment ready${NC}"

# Step 4: Clone or Update Repository
echo -e "${BLUE}[4/7] Setting up project...${NC}"

WORK_DIR="/workspace/vedic-astro-data-gen"

if [ -d "$WORK_DIR" ]; then
    echo "Project directory exists, updating..."
    cd "$WORK_DIR"
    git pull
else
    echo "Cloning repository..."
    cd /workspace
    # Replace with your actual repo URL when available
    # For now, assume code is already present
    if [ ! -d "vedic-astro-data-gen" ]; then
        echo -e "${RED}Please upload your project to /workspace/vedic-astro-data-gen${NC}"
        echo "You can:"
        echo "  1. Use rsync from local machine"
        echo "  2. Clone from your git repository"
        echo "  3. Upload via RunPod's web interface"
        exit 1
    fi
    cd vedic-astro-data-gen
fi

echo -e "${GREEN}✓ Project ready${NC}"

# Step 5: Install Dependencies
echo -e "${BLUE}[5/7] Installing dependencies...${NC}"
echo "This may take 5-10 minutes..."

pip install --quiet --upgrade pip
pip install --quiet -e ".[llm-opensource]"

echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 6: Setup Directories
echo -e "${BLUE}[6/7] Creating directories...${NC}"

mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/output
mkdir -p models_cache
mkdir -p /workspace/temp

echo -e "${GREEN}✓ Directories created${NC}"

# Step 7: Download Model (optional, can skip)
echo -e "${BLUE}[7/7] Checking model cache...${NC}"

read -p "Download Mistral-7B model now? (Recommended, ~4GB) (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Downloading model... This will take a few minutes."
    python3 << 'EOF'
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "mistralai/Mistral-7B-Instruct-v0.2"
print(f"Downloading {model_name}...")

try:
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir="./models_cache"
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        cache_dir="./models_cache",
        torch_dtype=torch.float16,
        device_map="auto",
        load_in_4bit=True
    )
    print("✓ Model downloaded successfully!")
except Exception as e:
    print(f"✗ Error downloading model: {e}")
    print("You can download it later during processing")
EOF
else
    echo "Skipping model download. It will download automatically during processing."
fi

# Final Summary
echo ""
echo "========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Upload your PDFs to: data/raw/"
echo ""
echo "     From your local machine:"
echo "     scp -P YOUR_RUNPOD_PORT data/raw/*.pdf root@ssh.runpod.io:/workspace/vedic-astro-data-gen/data/raw/"
echo ""
echo "  2. Process PDFs:"
echo "     python scripts/batch_process_runpod.py"
echo ""
echo "  3. Download results:"
echo "     scp -P YOUR_RUNPOD_PORT root@ssh.runpod.io:/workspace/vedic-astro-data-gen/data/output/* data/output/"
echo ""
echo "  4. Stop your pod when done to save money!"
echo ""
echo "========================================="
echo ""

# Create quick reference file
cat > /workspace/RUNPOD_COMMANDS.txt << 'EOF'
# ============================================================================
# RunPod Quick Reference
# ============================================================================

# Check GPU
nvidia-smi

# Upload PDFs
scp -P YOUR_PORT *.pdf root@ssh.runpod.io:/workspace/vedic-astro-data-gen/data/raw/

# Process all PDFs
cd /workspace/vedic-astro-data-gen
python scripts/batch_process_runpod.py

# Monitor progress
tail -f data/output/processing_log.json

# Download results
scp -P YOUR_PORT root@ssh.runpod.io:/workspace/vedic-astro-data-gen/data/output/* ./

# Check disk space
df -h

# Check running processes
ps aux | grep python

# ============================================================================
EOF

echo -e "${BLUE}Quick reference saved to: /workspace/RUNPOD_COMMANDS.txt${NC}"
echo ""
