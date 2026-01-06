#!/usr/bin/env python3
"""
Batch Processing Script for RunPod
===================================
Optimized for processing multiple PDFs on RunPod GPU instances.

Usage:
    python scripts/batch_process_runpod.py

Features:
- Automatic discovery of PDFs in data/raw/
- Progress tracking with ETA
- Error handling with retry logic
- Memory optimization (clear cache between PDFs)
- Detailed logging to JSON file
- Summary statistics
"""

import os
import sys
import json
import time
import gc
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import traceback

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from vedic_astro_gen import VedicQAGenerator, GenerationConfig
from vedic_astro_gen.utils.config_loader import load_config


class RunPodBatchProcessor:
    """Batch processor optimized for RunPod GPU instances."""

    def __init__(
        self,
        config_path: str = "configs/runpod_llm.yaml",
        input_dir: str = "data/raw",
        output_dir: str = "data/output",
        log_file: str = "data/output/processing_log.json"
    ):
        self.config_path = config_path
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.log_file = Path(log_file)

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load configuration
        self.config = self._load_config()

        # Processing state
        self.results = []
        self.total_qa_pairs = 0
        self.total_time = 0
        self.errors = []

    def _load_config(self) -> GenerationConfig:
        """Load RunPod-optimized configuration."""
        print(f"Loading configuration from {self.config_path}...")

        config_data = load_config(self.config_path)

        # Convert to GenerationConfig
        config = GenerationConfig(
            # LLM settings
            llm_generation_enabled=True,
            llm_provider=config_data.get("llm", {}).get("provider", "huggingface"),
            llm_model=config_data.get("llm", {}).get("model"),
            llm_base_url=config_data.get("llm", {}).get("base_url"),
            llm_api_key_env=config_data.get("llm", {}).get("api_key_env"),
            llm_temperature=config_data.get("llm", {}).get("temperature", 0.3),
            llm_max_tokens=config_data.get("llm", {}).get("max_tokens", 2048),

            # HuggingFace specific
            llm_load_in_4bit=config_data.get("llm", {}).get("load_in_4bit", True),
            llm_load_in_8bit=config_data.get("llm", {}).get("load_in_8bit", False),
            llm_device_map=config_data.get("llm", {}).get("device_map", "auto"),
            llm_torch_dtype=config_data.get("llm", {}).get("torch_dtype", "float16"),
            llm_cache_dir=config_data.get("llm", {}).get("cache_dir", "./models_cache"),

            # Processing settings
            qa_pairs_per_chunk=config_data.get("llm", {}).get("qa_pairs_per_chunk", 3),
            batch_size=config_data.get("llm", {}).get("batch_size", 1),
            request_timeout=config_data.get("llm", {}).get("request_timeout", 180),

            # Extraction settings
            chunk_size=config_data.get("extraction", {}).get("chunk_size", 1000),
            chunk_overlap=config_data.get("extraction", {}).get("chunk_overlap", 100),

            # Quality settings
            min_question_length=config_data.get("quality", {}).get("min_question_length", 20),
            min_answer_length=config_data.get("quality", {}).get("min_answer_length", 30),
            similarity_threshold=config_data.get("quality", {}).get("similarity_threshold", 0.85),

            # Output settings
            output_format=config_data.get("output", {}).get("format", "jsonl"),
            include_metadata=config_data.get("output", {}).get("include_metadata", True),
        )

        return config

    def find_pdfs(self) -> List[Path]:
        """Find all PDF files in input directory."""
        pdfs = list(self.input_dir.glob("*.pdf"))
        pdfs.sort()  # Process in alphabetical order
        return pdfs

    def process_single_pdf(
        self,
        pdf_path: Path,
        pdf_index: int,
        total_pdfs: int
    ) -> Dict:
        """Process a single PDF file."""
        pdf_name = pdf_path.name
        output_file = self.output_dir / f"{pdf_path.stem}_qa.jsonl"

        print(f"\n{'='*80}")
        print(f"Processing PDF {pdf_index}/{total_pdfs}: {pdf_name}")
        print(f"{'='*80}")

        result = {
            "pdf_name": pdf_name,
            "pdf_path": str(pdf_path),
            "output_file": str(output_file),
            "start_time": datetime.now().isoformat(),
            "status": "processing",
        }

        try:
            start_time = time.time()

            # Initialize generator
            print("Initializing generator...")
            generator = VedicQAGenerator(config=self.config)

            # Run pipeline
            print("Running generation pipeline...")
            pipeline_result = generator.run_full_pipeline(
                pdf_paths=[pdf_path],
                output_path=output_file,
                use_llm=True,
            )

            elapsed_time = time.time() - start_time

            # Update result
            result.update({
                "status": "success",
                "qa_pairs_generated": pipeline_result.get("output_count", 0),
                "chunks_processed": pipeline_result.get("chunks_processed", 0),
                "processing_time_seconds": round(elapsed_time, 2),
                "processing_time_human": str(timedelta(seconds=int(elapsed_time))),
                "end_time": datetime.now().isoformat(),
            })

            print(f"\n✓ Success!")
            print(f"  Generated: {result['qa_pairs_generated']} Q&A pairs")
            print(f"  Time: {result['processing_time_human']}")

            # Clean up memory
            self._cleanup_memory()

        except Exception as e:
            error_msg = str(e)
            error_trace = traceback.format_exc()

            result.update({
                "status": "failed",
                "error": error_msg,
                "error_trace": error_trace,
                "end_time": datetime.now().isoformat(),
            })

            print(f"\n✗ Failed: {error_msg}")
            self.errors.append(result)

            # Still try to clean up
            self._cleanup_memory()

        return result

    def _cleanup_memory(self):
        """Clean up memory between PDFs."""
        try:
            # Clear CUDA cache if available
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                print("  Cleared CUDA cache")
        except ImportError:
            pass

        # Run garbage collection
        gc.collect()
        print("  Ran garbage collection")

    def save_log(self):
        """Save processing log to JSON file."""
        log_data = {
            "processing_session": {
                "start_time": self.results[0]["start_time"] if self.results else None,
                "end_time": self.results[-1]["end_time"] if self.results else None,
                "total_pdfs": len(self.results),
                "successful": len([r for r in self.results if r["status"] == "success"]),
                "failed": len([r for r in self.results if r["status"] == "failed"]),
                "total_qa_pairs": self.total_qa_pairs,
                "total_processing_time": str(timedelta(seconds=int(self.total_time))),
            },
            "results": self.results,
        }

        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        print(f"\nLog saved to: {self.log_file}")

    def print_summary(self):
        """Print final summary statistics."""
        successful = [r for r in self.results if r["status"] == "success"]
        failed = [r for r in self.results if r["status"] == "failed"]

        print("\n" + "="*80)
        print("BATCH PROCESSING SUMMARY")
        print("="*80)
        print(f"\nTotal PDFs processed: {len(self.results)}")
        print(f"  ✓ Successful: {len(successful)}")
        print(f"  ✗ Failed: {len(failed)}")
        print(f"\nTotal Q&A pairs generated: {self.total_qa_pairs}")
        print(f"Total processing time: {timedelta(seconds=int(self.total_time))}")

        if successful:
            avg_time = self.total_time / len(successful)
            avg_pairs = self.total_qa_pairs / len(successful)
            print(f"\nAverage per PDF:")
            print(f"  Time: {timedelta(seconds=int(avg_time))}")
            print(f"  Q&A pairs: {int(avg_pairs)}")

        if failed:
            print(f"\nFailed PDFs:")
            for result in failed:
                print(f"  - {result['pdf_name']}: {result.get('error', 'Unknown error')}")

        print(f"\nOutput directory: {self.output_dir}")
        print(f"Processing log: {self.log_file}")
        print("="*80 + "\n")

    def run(self):
        """Run batch processing for all PDFs."""
        # Find PDFs
        pdfs = self.find_pdfs()

        if not pdfs:
            print(f"No PDF files found in {self.input_dir}")
            print("Please upload PDFs to data/raw/ directory")
            return

        print(f"\nFound {len(pdfs)} PDF files to process")
        print(f"Output directory: {self.output_dir}")
        print(f"Configuration: {self.config_path}\n")

        # Confirm before processing
        response = input("Start processing? [Y/n]: ").strip().lower()
        if response and response != 'y':
            print("Processing cancelled.")
            return

        # Process each PDF
        batch_start_time = time.time()

        for i, pdf_path in enumerate(pdfs, start=1):
            result = self.process_single_pdf(pdf_path, i, len(pdfs))
            self.results.append(result)

            # Update totals
            if result["status"] == "success":
                self.total_qa_pairs += result.get("qa_pairs_generated", 0)

            # Save log after each PDF
            self.save_log()

            # Estimate remaining time
            if i < len(pdfs):
                elapsed = time.time() - batch_start_time
                avg_time_per_pdf = elapsed / i
                remaining_pdfs = len(pdfs) - i
                eta = avg_time_per_pdf * remaining_pdfs
                print(f"\nETA for remaining {remaining_pdfs} PDFs: {timedelta(seconds=int(eta))}")

        self.total_time = time.time() - batch_start_time

        # Final log save
        self.save_log()

        # Print summary
        self.print_summary()


def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("RunPod Batch PDF Processor")
    print("Vedic Astrology Q&A Dataset Generation")
    print("="*80 + "\n")

    # Initialize processor
    processor = RunPodBatchProcessor()

    # Run batch processing
    processor.run()


if __name__ == "__main__":
    main()
