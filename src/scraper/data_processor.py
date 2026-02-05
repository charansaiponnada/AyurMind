"""
Data Processor - Intelligent Text Chunking

Processes scraped text files into semantic chunks for RAG.
Preserves context and adds metadata for better retrieval.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict
import tiktoken
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AyurvedicTextProcessor:
    """Process Ayurvedic texts into semantic chunks"""
    
    def __init__(
        self,
        input_dir: str = "./data/raw",
        output_dir: str = "./data/processed",
        chunk_size: int = 800,
        chunk_overlap: int = 200
    ):
        """Initialize processor
        
        Args:
            input_dir: Directory with scraped raw data
            output_dir: Directory to save processed chunks
            chunk_size: Target chunk size in tokens
            chunk_overlap: Overlap between chunks in tokens
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize tokenizer
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def count_tokens(self, text: str) -> int:
        """Count tokens in text
        
        Args:
            text: Input text
            
        Returns:
            Token count
        """
        return len(self.tokenizer.encode(text))
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        text = re.sub(r'  +', ' ', text)
        
        # Remove page numbers, headers, footers
        text = re.sub(r'\[Page \d+\]', '', text)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text.strip()
    
    def split_into_sections(self, text: str) -> List[Dict[str, str]]:
        """Split text into logical sections
        
        Args:
            text: Input text
            
        Returns:
            List of section dicts with 'title' and 'content'
        """
        sections = []
        
        # Try to detect section headers (all caps, followed by content)
        section_pattern = r'^([A-Z][A-Z\s]{10,})\n+(.+?)(?=\n[A-Z][A-Z\s]{10,}\n|\Z)'
        matches = re.findall(section_pattern, text, re.DOTALL | re.MULTILINE)
        
        if matches:
            for title, content in matches:
                sections.append({
                    'title': title.strip(),
                    'content': content.strip()
                })
        else:
            # If no clear sections, split by double newlines
            paragraphs = text.split('\n\n')
            current_section = {'title': 'Content', 'content': ''}
            
            for para in paragraphs:
                para = para.strip()
                if len(para) > 20:  # Skip very short paragraphs
                    current_section['content'] += para + '\n\n'
            
            if current_section['content']:
                sections.append(current_section)
        
        return sections
    
    def chunk_text_semantic(self, text: str, metadata: Dict) -> List[Dict]:
        """Create semantic chunks from text
        
        Args:
            text: Input text
            metadata: Metadata about the source
            
        Returns:
            List of chunk dicts
        """
        chunks = []
        
        # Clean text first
        text = self.clean_text(text)
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        current_chunk = []
        current_tokens = 0
        chunk_id = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_tokens = self.count_tokens(sentence)
            
            # Check if adding this sentence exceeds chunk size
            if current_tokens + sentence_tokens > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'chunk_id': chunk_id,
                    'text': chunk_text,
                    'token_count': current_tokens,
                    'metadata': metadata.copy()
                })
                
                chunk_id += 1
                
                # Start new chunk with overlap
                # Keep last few sentences for context
                overlap_sentences = []
                overlap_tokens = 0
                
                for sent in reversed(current_chunk):
                    sent_tokens = self.count_tokens(sent)
                    if overlap_tokens + sent_tokens <= self.chunk_overlap:
                        overlap_sentences.insert(0, sent)
                        overlap_tokens += sent_tokens
                    else:
                        break
                
                current_chunk = overlap_sentences
                current_tokens = overlap_tokens
            
            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_tokens += sentence_tokens
        
        # Don't forget the last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'chunk_id': chunk_id,
                'text': chunk_text,
                'token_count': current_tokens,
                'metadata': metadata.copy()
            })
        
        return chunks
    
    def process_chapter(self, text_file: Path, metadata: Dict) -> List[Dict]:
        """Process a single chapter file
        
        Args:
            text_file: Path to text file
            metadata: Chapter metadata
            
        Returns:
            List of chunks
        """
        text = text_file.read_text(encoding='utf-8')
        
        # Add file-specific metadata
        chunk_metadata = {
            **metadata,
            'source_file': text_file.name,
            'source_path': str(text_file)
        }
        
        chunks = self.chunk_text_semantic(text, chunk_metadata)
        
        return chunks
    
    def categorize_content(self, text: str, section_name: str) -> str:
        """Categorize content type for better retrieval
        
        Args:
            text: Chunk text
            section_name: Section name
            
        Returns:
            Category tag
        """
        text_lower = text.lower()
        
        # Prakriti-related content
        if any(term in text_lower for term in ['vata', 'pitta', 'kapha', 'constitution', 'prakriti']):
            return 'prakriti'
        
        # Vikriti/Disease content
        if any(term in text_lower for term in ['disease', 'symptom', 'disorder', 'imbalance', 'dosha']):
            return 'vikriti'
        
        # Treatment content
        if any(term in text_lower for term in ['treatment', 'therapy', 'remedy', 'herb', 'diet', 'lifestyle']):
            return 'treatment'
        
        # Default to section-based categorization
        if 'chikitsa' in section_name.lower():
            return 'treatment'
        elif 'nidana' in section_name.lower() or 'vimana' in section_name.lower():
            return 'vikriti'
        else:
            return 'general'
    
    def process_all(self) -> Dict:
        """Process all scraped sections
        
        Returns:
            Processing summary
        """
        logger.info("="*60)
        logger.info("STARTING TEXT PROCESSING")
        logger.info("="*60)
        
        all_chunks = []
        section_stats = []
        
        # Load scraping summary
        summary_file = self.input_dir / 'scraping_summary.json'
        if not summary_file.exists():
            logger.error("Scraping summary not found! Run scraper first.")
            return {}
        
        scraping_summary = json.loads(summary_file.read_text())
        
        # Process each section
        for section in scraping_summary['sections']:
            section_key = section['section_key']
            section_dir = self.input_dir / section_key
            
            if not section_dir.exists():
                logger.warning(f"Section directory not found: {section_dir}")
                continue
            
            logger.info(f"\nProcessing: {section['section_name']}")
            
            section_chunks = []
            
            # Process index/main page
            index_file = section_dir / 'index.txt'
            if index_file.exists():
                index_metadata = {
                    'section': section['section_name'],
                    'section_code': section['section_code'],
                    'chapter': 'Introduction',
                    'chapter_number': 0
                }
                index_chunks = self.process_chapter(index_file, index_metadata)
                section_chunks.extend(index_chunks)
            
            # Process each chapter
            for chapter_info in tqdm(section.get('chapters', []), desc=f"Chapters in {section_key}"):
                text_file = section_dir / chapter_info['text_file']
                
                if text_file.exists():
                    chapter_metadata = {
                        'section': section['section_name'],
                        'section_code': section['section_code'],
                        'chapter': chapter_info['title'],
                        'chapter_number': chapter_info['number'],
                        'source_url': chapter_info['url']
                    }
                    
                    chapter_chunks = self.process_chapter(text_file, chapter_metadata)
                    
                    # Add content categorization
                    for chunk in chapter_chunks:
                        chunk['metadata']['category'] = self.categorize_content(
                            chunk['text'], 
                            section['section_name']
                        )
                    
                    section_chunks.extend(chapter_chunks)
            
            all_chunks.extend(section_chunks)
            
            section_stats.append({
                'section': section['section_name'],
                'total_chunks': len(section_chunks),
                'total_tokens': sum(c['token_count'] for c in section_chunks)
            })
            
            logger.info(f"  Chunks created: {len(section_chunks)}")
            logger.info(f"  Total tokens: {sum(c['token_count'] for c in section_chunks):,}")
        
        # Save all chunks
        chunks_file = self.output_dir / 'all_chunks.json'
        chunks_file.write_text(
            json.dumps(all_chunks, indent=2),
            encoding='utf-8'
        )
        
        # Create summary
        summary = {
            'total_chunks': len(all_chunks),
            'total_tokens': sum(c['token_count'] for c in all_chunks),
            'avg_chunk_size': sum(c['token_count'] for c in all_chunks) / len(all_chunks) if all_chunks else 0,
            'sections': section_stats,
            'categories': self._get_category_stats(all_chunks)
        }
        
        summary_file = self.output_dir / 'processing_summary.json'
        summary_file.write_text(
            json.dumps(summary, indent=2),
            encoding='utf-8'
        )
        
        logger.info("\n" + "="*60)
        logger.info("PROCESSING COMPLETE!")
        logger.info("="*60)
        logger.info(f"Total Chunks: {summary['total_chunks']:,}")
        logger.info(f"Total Tokens: {summary['total_tokens']:,}")
        logger.info(f"Avg Chunk Size: {summary['avg_chunk_size']:.0f} tokens")
        logger.info(f"\nData saved to: {self.output_dir}")
        
        return summary
    
    def _get_category_stats(self, chunks: List[Dict]) -> Dict:
        """Get statistics by category
        
        Args:
            chunks: List of chunks
            
        Returns:
            Category statistics
        """
        categories = {}
        for chunk in chunks:
            cat = chunk['metadata'].get('category', 'unknown')
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        
        return categories


def main():
    """Main function"""
    processor = AyurvedicTextProcessor()
    summary = processor.process_all()
    
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
