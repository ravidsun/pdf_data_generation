#!/usr/bin/env python3
"""
Convert generated Q&A data to various training formats.

Supported output formats:
- alpaca: Alpaca/Stanford format (instruction, input, output)
- chatml: ChatML format with messages
- openai: OpenAI fine-tuning format
- sharegpt: ShareGPT conversation format
- hf: HuggingFace datasets format

Usage:
    python scripts/convert_format.py input.jsonl output.jsonl --format alpaca
"""

import argparse
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    """Load JSONL file."""
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def save_jsonl(data: List[Dict[str, Any]], path: str):
    """Save to JSONL file."""
    with open(path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def to_alpaca(item: Dict[str, Any], system_prompt: str = "") -> Dict[str, Any]:
    """Convert to Alpaca format."""
    return {
        "instruction": item["question"],
        "input": "",
        "output": item["answer"],
    }


def to_chatml(item: Dict[str, Any], system_prompt: str) -> Dict[str, Any]:
    """Convert to ChatML format."""
    messages = []
    
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": item["question"]})
    messages.append({"role": "assistant", "content": item["answer"]})
    
    return {"messages": messages}


def to_openai(item: Dict[str, Any], system_prompt: str) -> Dict[str, Any]:
    """Convert to OpenAI fine-tuning format."""
    messages = []
    
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": item["question"]})
    messages.append({"role": "assistant", "content": item["answer"]})
    
    return {"messages": messages}


def to_sharegpt(item: Dict[str, Any], system_prompt: str) -> Dict[str, Any]:
    """Convert to ShareGPT format."""
    conversations = []
    
    if system_prompt:
        conversations.append({"from": "system", "value": system_prompt})
    
    conversations.append({"from": "human", "value": item["question"]})
    conversations.append({"from": "gpt", "value": item["answer"]})
    
    return {"conversations": conversations}


def to_text_only(item: Dict[str, Any], system_prompt: str) -> Dict[str, Any]:
    """Convert to simple text format for causal LM training."""
    if system_prompt:
        text = f"{system_prompt}\n\nQuestion: {item['question']}\n\nAnswer: {item['answer']}"
    else:
        text = f"Question: {item['question']}\n\nAnswer: {item['answer']}"
    
    return {"text": text}


def convert_dataset(
    data: List[Dict[str, Any]],
    output_format: str,
    system_prompt: str = "",
) -> List[Dict[str, Any]]:
    """Convert dataset to specified format."""
    
    converters = {
        "alpaca": to_alpaca,
        "chatml": to_chatml,
        "openai": to_openai,
        "sharegpt": to_sharegpt,
        "text": to_text_only,
    }
    
    if output_format not in converters:
        raise ValueError(f"Unknown format: {output_format}. Supported: {list(converters.keys())}")
    
    converter = converters[output_format]
    return [converter(item, system_prompt) for item in data]


def main():
    parser = argparse.ArgumentParser(
        description="Convert Q&A data to various training formats"
    )
    parser.add_argument("input", help="Input JSONL file")
    parser.add_argument("output", help="Output JSONL file")
    parser.add_argument(
        "--format", "-f",
        choices=["alpaca", "chatml", "openai", "sharegpt", "text"],
        default="alpaca",
        help="Output format (default: alpaca)"
    )
    parser.add_argument(
        "--system-prompt", "-s",
        default="You are an expert Vedic astrologer (Jyotiṣī) with deep knowledge of classical texts including Bṛhat Parāśara Horā Śāstra and Jaimini Sūtra. Provide accurate, detailed interpretations using proper Sanskrit terminology.",
        help="System prompt to include"
    )
    parser.add_argument(
        "--no-system-prompt",
        action="store_true",
        help="Exclude system prompt"
    )
    
    args = parser.parse_args()
    
    # Load data
    logger.info(f"Loading: {args.input}")
    data = load_jsonl(args.input)
    logger.info(f"Loaded {len(data)} items")
    
    # Convert
    system_prompt = "" if args.no_system_prompt else args.system_prompt
    logger.info(f"Converting to {args.format} format...")
    converted = convert_dataset(data, args.format, system_prompt)
    
    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_jsonl(converted, args.output)
    logger.info(f"Saved {len(converted)} items to {args.output}")
    
    # Show sample
    logger.info("\nSample output:")
    logger.info(json.dumps(converted[0], indent=2, ensure_ascii=False)[:500] + "...")


if __name__ == "__main__":
    main()
