"""
PDF Knowledge Extractor for Vedic Astrology Texts

Enhanced extraction specifically designed for Jyotiṣa books:
- Preserves Sanskrit diacritical marks (ā, ī, ū, ṛ, ṣ, ṭ, ḍ, ṇ)
- Handles tables and charts
- Extracts section headers and structure
- Cleans OCR artifacts common in Sanskrit texts
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ExtractedSection:
    """A section extracted from PDF."""
    title: Optional[str]
    content: str
    page_start: int
    page_end: int
    section_type: str  # chapter, subsection, table, verse, example
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedChunk:
    """A chunk of text ready for Q&A generation."""
    text: str
    source_pdf: str
    page_start: int
    page_end: int
    section_title: Optional[str]
    chunk_type: str  # concept, rule, example, verse, table
    entities: List[str] = field(default_factory=list)  # Detected Jyotish terms
    

class VedicPDFExtractor:
    """
    Enhanced PDF extractor for Vedic Astrology texts.
    
    Features:
    - Sanskrit diacritics preservation
    - Jyotiṣa terminology detection
    - Section structure extraction
    - Intelligent chunking for Q&A generation
    """
    
    # Common Jyotiṣa terms with diacritics for detection
    JYOTISH_TERMS = {
        # Grahas
        "sūrya", "candra", "maṅgala", "budha", "guru", "bṛhaspati",
        "śukra", "śani", "rāhu", "ketu",
        # Rashis
        "meṣa", "vṛṣabha", "mithuna", "karkaṭa", "siṃha", "kanyā",
        "tulā", "vṛścika", "dhanu", "makara", "kumbha", "mīna",
        # Bhavas
        "lagna", "tanu", "dhana", "sahaja", "sukha", "bandhu",
        "putra", "suta", "ripu", "ari", "kalatrā", "jāyā",
        "āyu", "mṛtyu", "dharma", "bhāgya", "karma", "rājya",
        "lābha", "vyaya", "mokṣa",
        # Concepts
        "daśā", "bhukti", "antara", "pratyantara",
        "nakṣatra", "navāṃśa", "varga", "dṛṣṭi",
        "yoga", "rāja", "dhana", "ariṣṭa",
        "kāraka", "ātmakāraka", "amatyakāraka",
        "argalā", "virodhargalā",
        "upapada", "ārūḍha", "svāṃśa",
        "cara", "sthira", "dvisvabhāva",
        "krūra", "saumya", "śubha", "pāpa",
        # Jaimini specific
        "jaiminī", "sūtra", "upadeśa",
        "maheśvara", "māraka", "kakṣyā",
    }
    
    # Patterns for Sanskrit diacritics
    DIACRITIC_PATTERN = re.compile(r'[āīūṛṝḷḹṃḥṅñṭḍṇśṣ]', re.IGNORECASE)
    
    # Section header patterns
    CHAPTER_PATTERNS = [
        re.compile(r'^chapter\s+(\d+)', re.IGNORECASE),
        re.compile(r'^adhyāya\s+(\d+)', re.IGNORECASE),
        re.compile(r'^(\d+)\.\s+[A-Z]'),
        re.compile(r'^section\s+(\d+)', re.IGNORECASE),
    ]
    
    VERSE_PATTERNS = [
        re.compile(r'^\d+[\.\-]\d+'),  # 1.1, 1-1
        re.compile(r'^sūtra\s+\d+', re.IGNORECASE),
        re.compile(r'^śloka', re.IGNORECASE),
    ]
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        min_chunk_size: int = 100,
        preserve_structure: bool = True,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        self.preserve_structure = preserve_structure
    
    def extract_from_pdf(self, pdf_path: str) -> List[ExtractedChunk]:
        """
        Extract and process text from a Vedic astrology PDF.
        
        Args:
            pdf_path: Path to the PDF file.
            
        Returns:
            List of ExtractedChunk objects ready for Q&A generation.
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        logger.info(f"Extracting from: {pdf_path.name}")
        
        # Extract raw text with page info
        raw_pages = self._extract_pages(pdf_path)
        
        # Clean and normalize text
        cleaned_pages = [self._clean_text(page) for page in raw_pages]
        
        # Detect sections
        sections = self._detect_sections(cleaned_pages)
        
        # Chunk the sections
        chunks = self._chunk_sections(sections, pdf_path.name)
        
        # Detect Jyotiṣa entities in each chunk
        for chunk in chunks:
            chunk.entities = self._detect_jyotish_entities(chunk.text)
        
        logger.info(f"Extracted {len(chunks)} chunks from {pdf_path.name}")
        return chunks
    
    def _extract_pages(self, pdf_path: Path) -> List[str]:
        """Extract text from each page of the PDF."""
        pages = []
        
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(pdf_path)
            
            for page_num, page in enumerate(doc):
                text = page.get_text("text")
                pages.append(text)
            
            doc.close()
            logger.info(f"Extracted {len(pages)} pages using PyMuPDF")
            
        except ImportError:
            # Fallback to pdfplumber
            import pdfplumber
            
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    pages.append(text)
            
            logger.info(f"Extracted {len(pages)} pages using pdfplumber")
        
        return pages
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text while preserving Sanskrit diacritics.
        
        Args:
            text: Raw extracted text.
            
        Returns:
            Cleaned text with preserved diacritics.
        """
        if not text:
            return ""
        
        # Remove common OCR artifacts
        text = re.sub(r'\x00', '', text)  # Null bytes
        text = re.sub(r'[\x01-\x08\x0b\x0c\x0e-\x1f]', '', text)  # Control chars
        
        # Fix common OCR errors with diacritics
        text = self._fix_diacritic_errors(text)
        
        # Normalize whitespace but preserve paragraph breaks
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
        text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 newlines
        text = re.sub(r' *\n *', '\n', text)  # Clean around newlines
        
        # Remove page numbers and headers/footers (common patterns)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)  # Lone page numbers
        text = re.sub(r'^Page \d+.*$', '', text, flags=re.MULTILINE)
        
        # Remove repeated header/footer text (appears on multiple pages)
        # This is a simplified version - could be enhanced
        text = re.sub(r'^(In Search of Jyotish|Book \d+).*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
        
        return text.strip()
    
    def _fix_diacritic_errors(self, text: str) -> str:
        """Fix common OCR errors with Sanskrit diacritics."""
        # Common substitutions
        fixes = {
            'a¯': 'ā', 'i¯': 'ī', 'u¯': 'ū',
            'r.': 'ṛ', 'n.': 'ṇ', 't.': 'ṭ', 'd.': 'ḍ',
            's´': 'ś', 's.': 'ṣ',
            'ñ': 'ñ', 'n~': 'ñ',
            'm.': 'ṃ', 'h.': 'ḥ',
            # Sometimes diacritics get separated
            'a ̄': 'ā', 'i ̄': 'ī', 'u ̄': 'ū',
        }
        
        for wrong, correct in fixes.items():
            text = text.replace(wrong, correct)
        
        return text
    
    def _detect_sections(self, pages: List[str]) -> List[ExtractedSection]:
        """
        Detect logical sections from the extracted pages.
        
        Args:
            pages: List of cleaned page texts.
            
        Returns:
            List of ExtractedSection objects.
        """
        sections = []
        current_section = None
        current_content = []
        current_start_page = 0
        
        for page_num, page_text in enumerate(pages):
            lines = page_text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if this is a new section header
                section_info = self._identify_section_header(line)
                
                if section_info:
                    # Save previous section
                    if current_content:
                        sections.append(ExtractedSection(
                            title=current_section,
                            content='\n'.join(current_content),
                            page_start=current_start_page,
                            page_end=page_num,
                            section_type=self._classify_section_type(current_section, current_content),
                        ))
                    
                    # Start new section
                    current_section = section_info
                    current_content = []
                    current_start_page = page_num
                else:
                    current_content.append(line)
        
        # Save last section
        if current_content:
            sections.append(ExtractedSection(
                title=current_section,
                content='\n'.join(current_content),
                page_start=current_start_page,
                page_end=len(pages) - 1,
                section_type=self._classify_section_type(current_section, current_content),
            ))
        
        return sections
    
    def _identify_section_header(self, line: str) -> Optional[str]:
        """Check if a line is a section header."""
        # Check chapter patterns
        for pattern in self.CHAPTER_PATTERNS:
            if pattern.match(line):
                return line
        
        # Check for all-caps headers (common in books)
        if line.isupper() and len(line) > 3 and len(line) < 100:
            return line
        
        # Check for numbered sections with titles
        if re.match(r'^\d+\.\d*\s+[A-Z]', line):
            return line
        
        return None
    
    def _classify_section_type(self, title: Optional[str], content: List[str]) -> str:
        """Classify the type of section based on content."""
        content_text = ' '.join(content).lower()
        
        # Check for verse/sūtra content
        if any(p.search(content_text) for p in self.VERSE_PATTERNS):
            return "verse"
        
        # Check for example charts
        if "example" in content_text or "chart" in content_text or "kuṇḍalī" in content_text:
            return "example"
        
        # Check for rules
        if "rule" in content_text or "principle" in content_text:
            return "rule"
        
        # Check for tables (lots of short lines, possibly with | or tabs)
        short_lines = sum(1 for c in content if len(c) < 30)
        if short_lines > len(content) * 0.7:
            return "table"
        
        return "concept"
    
    def _chunk_sections(
        self,
        sections: List[ExtractedSection],
        source_pdf: str,
    ) -> List[ExtractedChunk]:
        """
        Chunk sections into appropriate sizes for Q&A generation.
        
        Args:
            sections: List of extracted sections.
            source_pdf: Name of source PDF.
            
        Returns:
            List of ExtractedChunk objects.
        """
        chunks = []
        
        for section in sections:
            if not section.content.strip():
                continue
            
            # For short sections, keep as single chunk
            if len(section.content) <= self.chunk_size:
                if len(section.content) >= self.min_chunk_size:
                    chunks.append(ExtractedChunk(
                        text=section.content,
                        source_pdf=source_pdf,
                        page_start=section.page_start,
                        page_end=section.page_end,
                        section_title=section.title,
                        chunk_type=section.section_type,
                    ))
            else:
                # Split into chunks with overlap
                section_chunks = self._split_with_overlap(
                    section.content,
                    section.title,
                    section.section_type,
                    source_pdf,
                    section.page_start,
                    section.page_end,
                )
                chunks.extend(section_chunks)
        
        return chunks
    
    def _split_with_overlap(
        self,
        text: str,
        section_title: Optional[str],
        section_type: str,
        source_pdf: str,
        page_start: int,
        page_end: int,
    ) -> List[ExtractedChunk]:
        """Split text into overlapping chunks, respecting sentence boundaries."""
        chunks = []
        
        # Split into sentences (respecting Sanskrit conventions)
        sentences = self._split_sentences(text)
        
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_len = len(sentence)
            
            if current_length + sentence_len > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = ' '.join(current_chunk)
                if len(chunk_text) >= self.min_chunk_size:
                    chunks.append(ExtractedChunk(
                        text=chunk_text,
                        source_pdf=source_pdf,
                        page_start=page_start,
                        page_end=page_end,
                        section_title=section_title,
                        chunk_type=section_type,
                    ))
                
                # Start new chunk with overlap
                overlap_sentences = self._get_overlap_sentences(current_chunk)
                current_chunk = overlap_sentences + [sentence]
                current_length = sum(len(s) for s in current_chunk)
            else:
                current_chunk.append(sentence)
                current_length += sentence_len
        
        # Save last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            if len(chunk_text) >= self.min_chunk_size:
                chunks.append(ExtractedChunk(
                    text=chunk_text,
                    source_pdf=source_pdf,
                    page_start=page_start,
                    page_end=page_end,
                    section_title=section_title,
                    chunk_type=section_type,
                ))
        
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences, handling Sanskrit conventions."""
        # Standard sentence endings plus Sanskrit daṇḍa (|) and double daṇḍa (॥)
        pattern = r'(?<=[.!?।॥])\s+'
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _get_overlap_sentences(self, sentences: List[str]) -> List[str]:
        """Get sentences for overlap from the end of current chunk."""
        overlap_text = 0
        overlap_sentences = []
        
        for sentence in reversed(sentences):
            if overlap_text + len(sentence) <= self.chunk_overlap:
                overlap_sentences.insert(0, sentence)
                overlap_text += len(sentence)
            else:
                break
        
        return overlap_sentences
    
    def _detect_jyotish_entities(self, text: str) -> List[str]:
        """Detect Jyotiṣa terminology in the text."""
        text_lower = text.lower()
        found_entities = []
        
        for term in self.JYOTISH_TERMS:
            if term in text_lower:
                found_entities.append(term)
        
        # Also detect capitalized terms that might be Jyotiṣa concepts
        capitalized = re.findall(r'\b[A-Z][a-zāīūṛṝḷḹṃḥṅñṭḍṇśṣ]+(?:\s+[A-Z][a-zāīūṛṝḷḹṃḥṅñṭḍṇśṣ]+)*\b', text)
        for term in capitalized:
            term_lower = term.lower()
            if term_lower not in found_entities and self.DIACRITIC_PATTERN.search(term):
                found_entities.append(term_lower)
        
        return list(set(found_entities))
    
    def extract_with_langchain(self, pdf_path: str) -> List[ExtractedChunk]:
        """
        Alternative extraction using LangChain document loaders.
        
        Args:
            pdf_path: Path to PDF file.
            
        Returns:
            List of ExtractedChunk objects.
        """
        from langchain_community.document_loaders import PyMuPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        loader = PyMuPDFLoader(pdf_path)
        documents = loader.load()
        
        # Custom separators for Jyotiṣa texts
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", "। ", "॥ ", ". ", " ", ""],
            length_function=len,
        )
        
        split_docs = splitter.split_documents(documents)
        
        chunks = []
        pdf_name = Path(pdf_path).name
        
        for doc in split_docs:
            text = self._clean_text(doc.page_content)
            if len(text) >= self.min_chunk_size:
                page = doc.metadata.get("page", 0)
                chunks.append(ExtractedChunk(
                    text=text,
                    source_pdf=pdf_name,
                    page_start=page,
                    page_end=page,
                    section_title=None,
                    chunk_type=self._infer_chunk_type(text),
                    entities=self._detect_jyotish_entities(text),
                ))
        
        return chunks
    
    def _infer_chunk_type(self, text: str) -> str:
        """Infer the type of content in a chunk."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["example", "chart", "kuṇḍalī", "horoscope"]):
            return "example"
        elif any(word in text_lower for word in ["sūtra", "śloka", "verse"]):
            return "verse"
        elif any(word in text_lower for word in ["rule", "principle", "if ", "when "]):
            return "rule"
        else:
            return "concept"


def extract_pdf_batch(
    pdf_paths: List[str],
    output_dir: Optional[str] = None,
    **kwargs,
) -> Dict[str, List[ExtractedChunk]]:
    """
    Extract from multiple PDFs.
    
    Args:
        pdf_paths: List of PDF file paths.
        output_dir: Optional directory to save extracted chunks.
        **kwargs: Additional arguments for VedicPDFExtractor.
        
    Returns:
        Dictionary mapping PDF names to their extracted chunks.
    """
    extractor = VedicPDFExtractor(**kwargs)
    results = {}
    
    for pdf_path in pdf_paths:
        try:
            chunks = extractor.extract_from_pdf(pdf_path)
            pdf_name = Path(pdf_path).name
            results[pdf_name] = chunks
            logger.info(f"Extracted {len(chunks)} chunks from {pdf_name}")
        except Exception as e:
            logger.error(f"Failed to extract from {pdf_path}: {e}")
    
    # Optionally save results
    if output_dir:
        import json
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for pdf_name, chunks in results.items():
            output_file = output_path / f"{pdf_name}_chunks.json"
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
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(chunk_dicts, f, ensure_ascii=False, indent=2)
    
    return results
