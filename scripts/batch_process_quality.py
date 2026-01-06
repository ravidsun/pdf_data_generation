#!/usr/bin/env python3
"""
Quality-Focused Batch Processing Script
========================================
Optimized for highest quality Vedic astrology Q&A generation.

Usage:
    python scripts/batch_process_quality.py

Features:
- Uses quality-focused configuration
- Enhanced quality checks on all outputs
- Detailed quality metrics and reporting
- Optimized for Claude 3.5 Sonnet, GPT-4 Turbo, or Llama 3 70B
"""

import os
import sys
import json
import time
import gc
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import traceback

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from vedic_astro_gen import VedicQAGenerator, GenerationConfig
from vedic_astro_gen.utils.config_loader import load_config


class QualityChecker:
    """Enhanced quality checking for Vedic astrology Q&A pairs."""

    @staticmethod
    def check_quality(qa_pair: Dict) -> Tuple[bool, str, float]:
        """
        Check quality of a Q&A pair.

        Returns:
            (is_quality, reason, quality_score)
        """
        question = qa_pair.get("question", "")
        answer = qa_pair.get("answer", "")
        score = 1.0

        # Length checks
        if len(question) < 25:
            return False, "Question too short", 0.0

        if len(answer) < 50:
            return False, "Answer too short", 0.0

        # Word count
        answer_words = len(answer.split())
        if answer_words < 15:
            return False, "Answer too brief", 0.0

        # Award points for good length
        if answer_words >= 30:
            score += 0.2
        if answer_words >= 50:
            score += 0.2

        # Sanskrit diacritics check
        diacritics = {'ā', 'ī', 'ū', 'ṛ', 'ṝ', 'ḷ', 'ḹ', 'ṃ', 'ḥ', 'ś', 'ṣ', 'ṭ', 'ḍ', 'ṇ'}
        diacritic_count = sum(1 for char in answer if char in diacritics)

        if diacritic_count == 0:
            score -= 0.3
            if len(answer) > 100:  # Long answer should have diacritics
                return False, "Missing Sanskrit diacritics", score

        if diacritic_count >= 3:
            score += 0.2

        # Question quality
        question_lower = question.lower()
        good_starters = ['how', 'why', 'when', 'compare', 'explain', 'analyze', 'describe', 'what']
        if any(question_lower.startswith(starter) for starter in good_starters):
            score += 0.1

        # Avoid very short answers
        if answer_words < 20:
            score -= 0.2

        # Award complexity
        if ',' in answer and '.' in answer:  # Has punctuation
            score += 0.1

        # Normalize score
        score = max(0.0, min(1.0, score))

        # Pass if score is high enough
        if score >= 0.7:
            return True, "Quality passed", score
        else:
            return False, f"Low quality score: {score:.2f}", score


class QualityBatchProcessor:
    """Batch processor optimized for quality."""

    def __init__(
        self,
        config_path: str = "configs/quality_focused.yaml",
        input_dir: str = "data/raw",
        output_dir: str = "data/output/quality"
    ):
        self.config_path = config_path
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load configuration
        self.config = self._load_config()

        # Quality checker
        self.quality_checker = QualityChecker()

        # Processing state
        self.results = []
        self.total_generated = 0
        self.total_passed = 0
        self.total_time = 0

    def _load_config(self) -> GenerationConfig:
        """Load quality-focused configuration."""
        print(f"Loading quality-focused configuration from {self.config_path}...")

        config_data = load_config(self.config_path)

        # Convert to GenerationConfig
        config = GenerationConfig(
            # LLM settings
            llm_generation_enabled=True,
            llm_provider=config_data.get("llm", {}).get("provider", "anthropic"),
            llm_model=config_data.get("llm", {}).get("model"),
            llm_base_url=config_data.get("llm", {}).get("base_url"),
            llm_api_key_env=config_data.get("llm", {}).get("api_key_env"),
            llm_temperature=config_data.get("llm", {}).get("temperature", 0.2),
            llm_max_tokens=config_data.get("llm", {}).get("max_tokens", 8192),

            # Processing settings
            qa_pairs_per_chunk=config_data.get("llm", {}).get("qa_pairs_per_chunk", 4),
            batch_size=config_data.get("llm", {}).get("batch_size", 1),
            request_timeout=config_data.get("llm", {}).get("request_timeout", 180),

            # Extraction settings
            chunk_size=config_data.get("extraction", {}).get("chunk_size", 1500),
            chunk_overlap=config_data.get("extraction", {}).get("chunk_overlap", 200),

            # Quality settings
            min_question_length=config_data.get("quality", {}).get("min_question_length", 25),
            min_answer_length=config_data.get("quality", {}).get("min_answer_length", 50),
            similarity_threshold=config_data.get("quality", {}).get("similarity_threshold", 0.90),

            # Output settings
            output_format=config_data.get("output", {}).get("format", "jsonl"),
            include_metadata=config_data.get("output", {}).get("include_metadata", True),
        )

        return config

    def find_pdfs(self) -> List[Path]:
        """Find all PDF files in input directory."""
        pdfs = list(self.input_dir.glob("*.pdf"))
        pdfs.sort()
        return pdfs

    def analyze_quality(self, output_file: Path) -> Dict:
        """Analyze quality of generated Q&A pairs."""
        quality_stats = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "avg_score": 0.0,
            "avg_question_length": 0,
            "avg_answer_length": 0,
            "avg_answer_words": 0,
            "has_diacritics": 0,
            "failure_reasons": {},
        }

        scores = []
        question_lengths = []
        answer_lengths = []
        answer_words_counts = []

        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    qa = json.loads(line)
                    quality_stats["total"] += 1

                    # Check quality
                    is_quality, reason, score = self.quality_checker.check_quality(qa)
                    scores.append(score)

                    if is_quality:
                        quality_stats["passed"] += 1
                    else:
                        quality_stats["failed"] += 1
                        quality_stats["failure_reasons"][reason] = \
                            quality_stats["failure_reasons"].get(reason, 0) + 1

                    # Collect stats
                    question = qa.get("question", "")
                    answer = qa.get("answer", "")

                    question_lengths.append(len(question))
                    answer_lengths.append(len(answer))
                    answer_words_counts.append(len(answer.split()))

                    # Check diacritics
                    diacritics = {'ā', 'ī', 'ū', 'ṛ', 'ṝ', 'ḷ', 'ḹ', 'ṃ', 'ḥ', 'ś', 'ṣ', 'ṭ', 'ḍ', 'ṇ'}
                    if any(char in answer for char in diacritics):
                        quality_stats["has_diacritics"] += 1

            # Calculate averages
            if scores:
                quality_stats["avg_score"] = sum(scores) / len(scores)
            if question_lengths:
                quality_stats["avg_question_length"] = sum(question_lengths) / len(question_lengths)
            if answer_lengths:
                quality_stats["avg_answer_length"] = sum(answer_lengths) / len(answer_lengths)
            if answer_words_counts:
                quality_stats["avg_answer_words"] = sum(answer_words_counts) / len(answer_words_counts)

        except Exception as e:
            print(f"Error analyzing quality: {e}")

        return quality_stats

    def process_single_pdf(
        self,
        pdf_path: Path,
        pdf_index: int,
        total_pdfs: int
    ) -> Dict:
        """Process a single PDF file with quality focus."""
        pdf_name = pdf_path.name
        output_file = self.output_dir / f"{pdf_path.stem}_quality_qa.jsonl"

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
            print("Running quality-focused generation...")
            pipeline_result = generator.run_full_pipeline(
                pdf_paths=[pdf_path],
                output_path=output_file,
                use_llm=True,
            )

            elapsed_time = time.time() - start_time

            # Analyze quality
            print("Analyzing quality...")
            quality_stats = self.analyze_quality(output_file)

            # Update result
            result.update({
                "status": "success",
                "qa_pairs_generated": pipeline_result.get("output_count", 0),
                "quality_stats": quality_stats,
                "processing_time_seconds": round(elapsed_time, 2),
                "processing_time_human": str(timedelta(seconds=int(elapsed_time))),
                "end_time": datetime.now().isoformat(),
            })

            # Print quality summary
            total = quality_stats["total"]
            passed = quality_stats["passed"]
            pass_rate = (passed / total * 100) if total > 0 else 0
            avg_score = quality_stats["avg_score"]

            print(f"\n✓ Success!")
            print(f"  Generated: {total} Q&A pairs")
            print(f"  Quality passed: {passed} ({pass_rate:.1f}%)")
            print(f"  Average quality score: {avg_score:.2f}")
            print(f"  Average answer words: {quality_stats['avg_answer_words']:.1f}")
            print(f"  Has Sanskrit diacritics: {quality_stats['has_diacritics']}/{total}")
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

            # Still try to clean up
            self._cleanup_memory()

        return result

    def _cleanup_memory(self):
        """Clean up memory between PDFs."""
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                print("  Cleared CUDA cache")
        except ImportError:
            pass

        gc.collect()
        print("  Ran garbage collection")

    def save_quality_report(self):
        """Save comprehensive quality report."""
        report_file = self.output_dir / "quality_report.json"

        # Calculate overall statistics
        total_generated = 0
        total_passed = 0
        all_scores = []

        for result in self.results:
            if result["status"] == "success":
                stats = result.get("quality_stats", {})
                total_generated += stats.get("total", 0)
                total_passed += stats.get("passed", 0)
                if stats.get("avg_score"):
                    all_scores.append(stats["avg_score"])

        overall_quality = (total_passed / total_generated * 100) if total_generated > 0 else 0
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

        report_data = {
            "session": {
                "start_time": self.results[0]["start_time"] if self.results else None,
                "end_time": self.results[-1]["end_time"] if self.results else None,
                "total_pdfs": len(self.results),
                "successful": len([r for r in self.results if r["status"] == "success"]),
                "failed": len([r for r in self.results if r["status"] == "failed"]),
                "total_processing_time": str(timedelta(seconds=int(self.total_time))),
            },
            "quality_summary": {
                "total_qa_pairs_generated": total_generated,
                "quality_passed": total_passed,
                "quality_pass_rate": round(overall_quality, 2),
                "average_quality_score": round(avg_score, 3),
            },
            "per_pdf_results": self.results,
            "config_file": self.config_path,
        }

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"\nQuality report saved to: {report_file}")

    def print_summary(self):
        """Print final quality summary."""
        successful = [r for r in self.results if r["status"] == "success"]
        failed = [r for r in self.results if r["status"] == "failed"]

        # Calculate totals
        total_generated = 0
        total_passed = 0

        for result in successful:
            stats = result.get("quality_stats", {})
            total_generated += stats.get("total", 0)
            total_passed += stats.get("passed", 0)

        pass_rate = (total_passed / total_generated * 100) if total_generated > 0 else 0

        print("\n" + "="*80)
        print("QUALITY-FOCUSED BATCH PROCESSING SUMMARY")
        print("="*80)
        print(f"\nTotal PDFs processed: {len(self.results)}")
        print(f"  ✓ Successful: {len(successful)}")
        print(f"  ✗ Failed: {len(failed)}")

        print(f"\nQuality Metrics:")
        print(f"  Total Q&A pairs generated: {total_generated}")
        print(f"  Quality checks passed: {total_passed}")
        print(f"  Quality pass rate: {pass_rate:.1f}%")

        print(f"\nProcessing:")
        print(f"  Total time: {timedelta(seconds=int(self.total_time))}")

        if successful:
            avg_time = self.total_time / len(successful)
            print(f"  Average per PDF: {timedelta(seconds=int(avg_time))}")

        print(f"\nOutput directory: {self.output_dir}")
        print(f"Quality report: {self.output_dir}/quality_report.json")
        print("="*80 + "\n")

    def run(self):
        """Run quality-focused batch processing."""
        # Find PDFs
        pdfs = self.find_pdfs()

        if not pdfs:
            print(f"No PDF files found in {self.input_dir}")
            print("Please place PDFs in data/raw/ directory")
            return

        print(f"\n{'='*80}")
        print("QUALITY-FOCUSED BATCH PROCESSING")
        print(f"{'='*80}")
        print(f"\nFound {len(pdfs)} PDF files to process")
        print(f"Output directory: {self.output_dir}")
        print(f"Configuration: {self.config_path}")
        print(f"Model: {self.config.llm_model}")
        print(f"Quality threshold: High (score >= 0.7)\n")

        # Confirm before processing
        response = input("Start quality-focused processing? [Y/n]: ").strip().lower()
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
                stats = result.get("quality_stats", {})
                self.total_generated += stats.get("total", 0)
                self.total_passed += stats.get("passed", 0)

            # Save report after each PDF
            self.save_quality_report()

            # Estimate remaining time
            if i < len(pdfs):
                elapsed = time.time() - batch_start_time
                avg_time_per_pdf = elapsed / i
                remaining_pdfs = len(pdfs) - i
                eta = avg_time_per_pdf * remaining_pdfs
                print(f"\nETA for remaining {remaining_pdfs} PDFs: {timedelta(seconds=int(eta))}")

        self.total_time = time.time() - batch_start_time

        # Final report
        self.save_quality_report()
        self.print_summary()


def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("Quality-Focused Vedic Astrology Q&A Generator")
    print("Optimized for Claude 3.5 Sonnet / GPT-4 Turbo / Llama 3 70B")
    print("="*80 + "\n")

    # Initialize processor
    processor = QualityBatchProcessor()

    # Run batch processing
    processor.run()


if __name__ == "__main__":
    main()
