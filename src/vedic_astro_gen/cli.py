"""
Command-line interface for Vedic Astrology Data Generator.

Commands:
- generate: Run the full generation pipeline
- extract: Extract text from PDFs
- filter: Filter and clean existing datasets
- augment: Augment existing datasets
- analyze: Analyze dataset quality and diversity
- templates: List available templates
"""

import logging
import sys
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer(
    name="vedic-gen",
    help="Vedic Astrology Q&A Data Generator for LLM Fine-Tuning",
    add_completion=False,
)
console = Console()


def setup_logging(verbose: bool = False):
    """Configure logging with rich output."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )


@app.command("generate")
def generate(
    pdf_paths: Optional[List[Path]] = typer.Option(
        None,
        "--pdf", "-p",
        help="PDF file(s) to extract from",
    ),
    output: Path = typer.Option(
        Path("data/output/vedic_qa.jsonl"),
        "--output", "-o",
        help="Output JSONL file path",
    ),
    use_templates: bool = typer.Option(
        True,
        "--templates/--no-templates",
        help="Enable template-based generation",
    ),
    use_llm: bool = typer.Option(
        False,
        "--llm/--no-llm",
        help="Enable LLM-based generation (requires API key)",
    ),
    augment: bool = typer.Option(
        True,
        "--augment/--no-augment",
        help="Enable data augmentation",
    ),
    augment_per_item: int = typer.Option(
        2,
        "--augment-count",
        help="Number of augmentations per item",
    ),
    seed: int = typer.Option(
        42,
        "--seed",
        help="Random seed for reproducibility",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose logging",
    ),
):
    """
    Run the full Q&A generation pipeline.
    
    Generates high-quality Vedic astrology Q&A pairs from:
    - Structured templates (planet/house/sign combinations)
    - PDF text extraction
    - Optional LLM-based generation
    """
    setup_logging(verbose)
    
    console.print(Panel.fit(
        "[bold blue]Vedic Astrology Q&A Generator[/bold blue]\n"
        "Generating high-quality training data for LLM fine-tuning"
    ))
    
    from vedic_astro_gen.generator import VedicQAGenerator, GenerationConfig
    
    # Build config
    config = GenerationConfig(
        templates_enabled=use_templates,
        pdf_extraction_enabled=pdf_paths is not None,
        llm_generation_enabled=use_llm,
        augmentation_enabled=augment,
        augmentations_per_item=augment_per_item,
    )
    
    # Convert paths to strings
    pdf_path_strs = [str(p) for p in pdf_paths] if pdf_paths else None
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating Q&A data...", total=None)
        
        generator = VedicQAGenerator(config=config, seed=seed)
        results = generator.run_full_pipeline(
            pdf_paths=pdf_path_strs,
            output_path=str(output),
            use_templates=use_templates,
            use_pdf=pdf_paths is not None,
            use_llm=use_llm,
            use_augmentation=augment,
        )
        
        progress.update(task, completed=True)
    
    # Display results
    console.print("\n[green]✓ Generation complete![/green]\n")
    
    stats_table = Table(title="Generation Statistics")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="green")
    
    for key, value in results["stats"].items():
        stats_table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(stats_table)
    
    # Diversity report
    diversity = results["diversity_report"]
    console.print(f"\n[bold]Diversity Score:[/bold] {diversity['diversity_score']:.2f}")
    
    if diversity.get("recommendations"):
        console.print("\n[yellow]Recommendations:[/yellow]")
        for rec in diversity["recommendations"][:5]:
            console.print(f"  • {rec}")
    
    console.print(f"\n[bold]Output:[/bold] {results['output_path']}")
    console.print(f"[bold]Total Q&A pairs:[/bold] {results['output_count']}")


@app.command("extract")
def extract(
    pdf_path: Path = typer.Argument(
        ...,
        help="PDF file to extract from",
    ),
    output: Path = typer.Option(
        None,
        "--output", "-o",
        help="Output JSON file (default: same name as PDF)",
    ),
    chunk_size: int = typer.Option(
        1000,
        "--chunk-size",
        help="Text chunk size",
    ),
    chunk_overlap: int = typer.Option(
        100,
        "--overlap",
        help="Chunk overlap",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose logging",
    ),
):
    """
    Extract text chunks from a Vedic astrology PDF.
    
    Preserves Sanskrit diacritical marks and detects Jyotiṣa terminology.
    """
    setup_logging(verbose)
    
    console.print(Panel.fit(
        f"[bold]Extracting from:[/bold] {pdf_path.name}"
    ))
    
    from vedic_astro_gen.pdf_extractor import VedicPDFExtractor
    import json
    
    extractor = VedicPDFExtractor(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    
    chunks = extractor.extract_from_pdf(str(pdf_path))
    
    # Determine output path
    if output is None:
        output = pdf_path.with_suffix('.chunks.json')
    
    # Save chunks
    chunk_dicts = [
        {
            "text": c.text,
            "source_pdf": c.source_pdf,
            "page_start": c.page_start,
            "page_end": c.page_end,
            "section_title": c.section_title,
            "chunk_type": c.chunk_type,
            "entities": c.entities,
        }
        for c in chunks
    ]
    
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(chunk_dicts, f, ensure_ascii=False, indent=2)
    
    console.print(f"\n[green]✓ Extracted {len(chunks)} chunks[/green]")
    console.print(f"[bold]Output:[/bold] {output}")
    
    # Show entity statistics
    all_entities = []
    for c in chunks:
        all_entities.extend(c.entities)
    
    entity_counts = {}
    for e in all_entities:
        entity_counts[e] = entity_counts.get(e, 0) + 1
    
    top_entities = sorted(entity_counts.items(), key=lambda x: -x[1])[:10]
    
    console.print("\n[bold]Top detected entities:[/bold]")
    for entity, count in top_entities:
        console.print(f"  {entity}: {count}")


@app.command("filter")
def filter_data(
    input_path: Path = typer.Argument(
        ...,
        help="Input JSONL file to filter",
    ),
    output: Path = typer.Option(
        None,
        "--output", "-o",
        help="Output JSONL file (default: input_filtered.jsonl)",
    ),
    min_q_length: int = typer.Option(
        20,
        "--min-q-len",
        help="Minimum question length",
    ),
    min_a_length: int = typer.Option(
        30,
        "--min-a-len",
        help="Minimum answer length",
    ),
    min_a_words: int = typer.Option(
        10,
        "--min-a-words",
        help="Minimum answer word count",
    ),
    similarity_threshold: float = typer.Option(
        0.85,
        "--similarity",
        help="Similarity threshold for near-duplicate detection",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose logging",
    ),
):
    """
    Filter and clean an existing Q&A dataset.
    
    Removes duplicates, low-quality pairs, and off-topic content.
    """
    setup_logging(verbose)
    
    console.print(Panel.fit(
        f"[bold]Filtering:[/bold] {input_path.name}"
    ))
    
    from vedic_astro_gen.quality_filters import filter_jsonl_file
    
    if output is None:
        output = input_path.with_suffix('.filtered.jsonl')
    
    results = filter_jsonl_file(
        input_path=str(input_path),
        output_path=str(output),
        min_question_length=min_q_length,
        min_answer_length=min_a_length,
        min_answer_words=min_a_words,
        similarity_threshold=similarity_threshold,
    )
    
    console.print(f"\n[green]✓ Filtering complete![/green]")
    
    stats_table = Table(title="Filter Statistics")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="green")
    
    for key, value in results["filter_stats"].items():
        stats_table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(stats_table)
    
    diversity = results["diversity_report"]
    console.print(f"\n[bold]Diversity Score:[/bold] {diversity['diversity_score']:.2f}")
    
    console.print(f"\n[bold]Output:[/bold] {results['output_path']}")
    console.print(f"[bold]Removed items:[/bold] {results['removed_path']}")


@app.command("augment")
def augment_data(
    input_path: Path = typer.Argument(
        ...,
        help="Input JSONL file to augment",
    ),
    output: Path = typer.Option(
        None,
        "--output", "-o",
        help="Output JSONL file",
    ),
    per_item: int = typer.Option(
        2,
        "--per-item", "-n",
        help="Number of augmentations per item",
    ),
    seed: int = typer.Option(
        42,
        "--seed",
        help="Random seed",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose logging",
    ),
):
    """
    Augment an existing Q&A dataset.
    
    Uses domain-aware augmentation techniques for Vedic astrology.
    """
    setup_logging(verbose)
    
    console.print(Panel.fit(
        f"[bold]Augmenting:[/bold] {input_path.name}"
    ))
    
    from vedic_astro_gen.augmentation import augment_jsonl_file
    
    if output is None:
        output = input_path.with_suffix('.augmented.jsonl')
    
    results = augment_jsonl_file(
        input_path=str(input_path),
        output_path=str(output),
        augmentations_per_item=per_item,
        seed=seed,
    )
    
    console.print(f"\n[green]✓ Augmentation complete![/green]")
    console.print(f"[bold]Original count:[/bold] {results['original_count']}")
    console.print(f"[bold]Augmented count:[/bold] {results['augmented_count']}")
    console.print(f"[bold]Added:[/bold] {results['added_count']}")
    console.print(f"\n[bold]Output:[/bold] {results['output_path']}")


@app.command("analyze")
def analyze(
    input_path: Path = typer.Argument(
        ...,
        help="JSONL file to analyze",
    ),
    question_field: str = typer.Option(
        "question",
        "--q-field",
        help="Field name for questions",
    ),
    answer_field: str = typer.Option(
        "answer",
        "--a-field",
        help="Field name for answers",
    ),
):
    """
    Analyze dataset quality and diversity.
    
    Shows statistics, pattern distribution, and recommendations.
    """
    console.print(Panel.fit(
        f"[bold]Analyzing:[/bold] {input_path.name}"
    ))
    
    import json
    from vedic_astro_gen.quality_filters import DiversityChecker
    from collections import Counter
    
    # Load data
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    
    console.print(f"\n[bold]Total items:[/bold] {len(data)}")
    
    # Basic statistics
    q_lengths = [len(item.get(question_field, "")) for item in data]
    a_lengths = [len(item.get(answer_field, "")) for item in data]
    a_words = [len(item.get(answer_field, "").split()) for item in data]
    
    stats_table = Table(title="Basic Statistics")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Min", style="yellow")
    stats_table.add_column("Max", style="yellow")
    stats_table.add_column("Avg", style="green")
    
    stats_table.add_row(
        "Question Length",
        str(min(q_lengths)),
        str(max(q_lengths)),
        f"{sum(q_lengths)/len(q_lengths):.1f}",
    )
    stats_table.add_row(
        "Answer Length",
        str(min(a_lengths)),
        str(max(a_lengths)),
        f"{sum(a_lengths)/len(a_lengths):.1f}",
    )
    stats_table.add_row(
        "Answer Words",
        str(min(a_words)),
        str(max(a_words)),
        f"{sum(a_words)/len(a_words):.1f}",
    )
    
    console.print(stats_table)
    
    # QA type distribution
    qa_types = Counter(item.get("qa_type", "unknown") for item in data)
    
    type_table = Table(title="QA Type Distribution")
    type_table.add_column("Type", style="cyan")
    type_table.add_column("Count", style="green")
    type_table.add_column("Percentage", style="yellow")
    
    for qa_type, count in qa_types.most_common():
        type_table.add_row(qa_type, str(count), f"{count/len(data)*100:.1f}%")
    
    console.print(type_table)
    
    # Diversity analysis
    checker = DiversityChecker()
    diversity = checker.analyze_diversity(data, question_field)
    
    console.print(f"\n[bold]Diversity Score:[/bold] {diversity['diversity_score']:.2f}")
    
    if diversity.get("over_represented"):
        console.print("\n[yellow]Over-represented patterns:[/yellow]")
        for pattern, ratio in diversity["over_represented"].items():
            console.print(f"  • {pattern}: {ratio:.1%}")
    
    if diversity.get("under_represented"):
        console.print("\n[yellow]Under-represented patterns:[/yellow]")
        for pattern, ratio in diversity["under_represented"].items():
            console.print(f"  • {pattern}: {ratio:.1%}")
    
    if diversity.get("recommendations"):
        console.print("\n[bold]Recommendations:[/bold]")
        for rec in diversity["recommendations"]:
            console.print(f"  • {rec}")


@app.command("templates")
def list_templates():
    """
    List all available Q&A templates.
    """
    from vedic_astro_gen.templates import TemplateManager
    
    console.print(Panel.fit("[bold]Available Q&A Templates[/bold]"))
    
    manager = TemplateManager()
    template_counts = manager.get_all_template_types()
    
    table = Table(title="Template Categories")
    table.add_column("Category", style="cyan")
    table.add_column("Count", style="green")
    
    total = 0
    for category, count in sorted(template_counts.items()):
        table.add_row(category.replace("_", " ").title(), str(count))
        total += count
    
    table.add_row("[bold]Total[/bold]", f"[bold]{total}[/bold]")
    
    console.print(table)
    
    # Calculate potential combinations
    from vedic_astro_gen.knowledge_base import GRAHAS, RASHIS, BHAVAS
    
    graha_count = len(GRAHAS)
    rashi_count = len(RASHIS)
    bhava_count = len(BHAVAS)
    
    console.print(f"\n[bold]Potential Combinations:[/bold]")
    console.print(f"  Grahas: {graha_count}")
    console.print(f"  Rāśis: {rashi_count}")
    console.print(f"  Bhāvas: {bhava_count}")
    console.print(f"  Graha × Bhāva: {graha_count * bhava_count}")
    console.print(f"  Graha × Rāśi: {graha_count * rashi_count}")
    console.print(f"  Graha pairs: {graha_count * (graha_count-1) // 2}")


@app.command("version")
def version():
    """Show version information."""
    from vedic_astro_gen import __version__
    console.print(f"vedic-astro-data-gen version {__version__}")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
