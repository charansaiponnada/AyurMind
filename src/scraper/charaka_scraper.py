"""
Charaka Samhita Online Web Scraper

Scrapes all 8 sections from https://www.carakasamhitaonline.com
Saves raw HTML and extracted text for RAG processing.
"""

import os
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Dict, Tuple
import json
from tqdm import tqdm
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CharakaScraper:
    """Scraper for Charaka Samhita Online"""
    
    # All 8 sections with their URLs
    SECTIONS = {
        "Sutra_Sthana": {
            "name": "Section on Fundamental Principles",
            "url": "https://www.carakasamhitaonline.com/index.php?title=Sutra_Sthana",
            "code": "I"
        },
        "Nidana_Sthana": {
            "name": "Section on Diagnostic Principles",
            "url": "https://www.carakasamhitaonline.com/index.php?title=Nidana_Sthana",
            "code": "II"
        },
        "Vimana_Sthana": {
            "name": "Section on Specific Medical Principles",
            "url": "https://www.carakasamhitaonline.com/index.php?title=Vimana_Sthana",
            "code": "III"
        },
        "Sharira_Sthana": {
            "name": "Section on Human Being and Genesis",
            "url": "https://www.carakasamhitaonline.com/index.php?title=Sharira_Sthana",
            "code": "IV"
        },
        "Indriya_Sthana": {
            "name": "Section on Sensorial Prognosis",
            "url": "https://www.carakasamhitaonline.com/index.php?title=Indriya_Sthana",
            "code": "V"
        },
        "Chikitsa_Sthana": {
            "name": "Section on Therapeutic Principles",
            "url": "https://www.carakasamhitaonline.com/index.php?title=Chikitsa_Sthana",
            "code": "VI"
        },
        "Kalpa_Sthana": {
            "name": "Section on Pharmaceutical Preparations",
            "url": "https://www.carakasamhitaonline.com/index.php?title=Kalpa_Sthana",
            "code": "VII"
        },
        "Siddhi_Sthana": {
            "name": "Section on Therapeutic Procedures",
            "url": "https://www.carakasamhitaonline.com/index.php?title=Siddhi_Sthana",
            "code": "VIII"
        }
    }
    
    def __init__(self, output_dir: str = "./data/raw"):
        """Initialize scraper
        
        Args:
            output_dir: Directory to save scraped data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.delay = int(os.getenv("REQUEST_DELAY", "2"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.timeout = int(os.getenv("TIMEOUT", "30"))
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Educational Research Bot for Ayurveda Study)'
        })
        
    def fetch_page(self, url: str) -> Tuple[str, bool]:
        """Fetch a single page with retries
        
        Args:
            url: URL to fetch
            
        Returns:
            Tuple of (HTML content, success status)
        """
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                time.sleep(self.delay)  # Be respectful to the server
                return response.text, True
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay * 2)  # Longer delay on retry
                    
        logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
        return "", False
    
    def extract_chapter_links(self, html: str, base_url: str) -> List[Dict[str, str]]:
        """Extract chapter links from a section page
        
        Args:
            html: HTML content of section page
            base_url: Base URL for the website
            
        Returns:
            List of chapter info dicts with 'title' and 'url'
        """
        soup = BeautifulSoup(html, 'lxml')
        chapters = []
        
        # Find all chapter links (they're usually in ordered lists or specific divs)
        # This is site-specific and may need adjustment
        content_div = soup.find('div', {'id': 'mw-content-text'})
        
        if content_div:
            # Look for links that are chapter titles
            links = content_div.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                # Filter for actual chapter links (usually contain specific patterns)
                if href.startswith('/index.php?title=') and len(title) > 10:
                    # Skip navigation links
                    if any(skip in title.lower() for skip in ['main page', 'category', 'help', 'search']):
                        continue
                        
                    full_url = f"{base_url}{href}"
                    chapters.append({
                        'title': title,
                        'url': full_url
                    })
        
        # Remove duplicates
        seen = set()
        unique_chapters = []
        for ch in chapters:
            if ch['url'] not in seen:
                seen.add(ch['url'])
                unique_chapters.append(ch)
                
        return unique_chapters
    
    def extract_text_content(self, html: str) -> str:
        """Extract clean text from HTML
        
        Args:
            html: HTML content
            
        Returns:
            Cleaned text content
        """
        soup = BeautifulSoup(html, 'lxml')
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer']):
            script.decompose()
            
        # Get main content
        content_div = soup.find('div', {'id': 'mw-content-text'})
        
        if content_div:
            text = content_div.get_text(separator='\n', strip=True)
        else:
            text = soup.get_text(separator='\n', strip=True)
            
        # Clean up text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n\n'.join(lines)
        
        return text
    
    def scrape_section(self, section_key: str) -> Dict:
        """Scrape a complete section with all chapters
        
        Args:
            section_key: Key from SECTIONS dict
            
        Returns:
            Dict with section metadata and scraped data
        """
        section_info = self.SECTIONS[section_key]
        logger.info(f"\n{'='*60}")
        logger.info(f"Scraping: {section_info['code']}. {section_info['name']}")
        logger.info(f"URL: {section_info['url']}")
        logger.info(f"{'='*60}")
        
        # Create section directory
        section_dir = self.output_dir / section_key
        section_dir.mkdir(exist_ok=True)
        
        # Fetch main section page
        html, success = self.fetch_page(section_info['url'])
        
        if not success:
            return {'error': 'Failed to fetch main section page'}
            
        # Save main page
        (section_dir / 'index.html').write_text(html, encoding='utf-8')
        
        # Extract text from main page
        main_text = self.extract_text_content(html)
        (section_dir / 'index.txt').write_text(main_text, encoding='utf-8')
        
        # Extract chapter links
        base_url = "https://www.carakasamhitaonline.com"
        chapters = self.extract_chapter_links(html, base_url)
        
        logger.info(f"Found {len(chapters)} chapters in {section_key}")
        
        # Scrape each chapter
        chapter_data = []
        for i, chapter in enumerate(tqdm(chapters, desc=f"Chapters in {section_key}")):
            chapter_html, success = self.fetch_page(chapter['url'])
            
            if success:
                # Save chapter HTML
                chapter_filename = f"chapter_{i+1:02d}.html"
                (section_dir / chapter_filename).write_text(chapter_html, encoding='utf-8')
                
                # Extract and save chapter text
                chapter_text = self.extract_text_content(chapter_html)
                text_filename = f"chapter_{i+1:02d}.txt"
                (section_dir / text_filename).write_text(chapter_text, encoding='utf-8')
                
                chapter_data.append({
                    'number': i + 1,
                    'title': chapter['title'],
                    'url': chapter['url'],
                    'html_file': chapter_filename,
                    'text_file': text_filename,
                    'word_count': len(chapter_text.split())
                })
            else:
                logger.warning(f"Failed to scrape chapter: {chapter['title']}")
        
        # Save metadata
        metadata = {
            'section_key': section_key,
            'section_code': section_info['code'],
            'section_name': section_info['name'],
            'section_url': section_info['url'],
            'total_chapters': len(chapter_data),
            'chapters': chapter_data,
            'total_words': sum(ch['word_count'] for ch in chapter_data)
        }
        
        (section_dir / 'metadata.json').write_text(
            json.dumps(metadata, indent=2),
            encoding='utf-8'
        )
        
        logger.info(f"✓ Scraped {len(chapter_data)} chapters from {section_key}")
        logger.info(f"  Total words: {metadata['total_words']:,}")
        
        return metadata
    
    def scrape_all(self) -> Dict:
        """Scrape all 8 sections
        
        Returns:
            Summary statistics
        """
        logger.info("\n" + "="*60)
        logger.info("STARTING CHARAKA SAMHITA SCRAPING")
        logger.info("="*60 + "\n")
        
        all_metadata = []
        
        for section_key in self.SECTIONS.keys():
            metadata = self.scrape_section(section_key)
            all_metadata.append(metadata)
            time.sleep(self.delay * 2)  # Extra delay between sections
        
        # Create summary
        summary = {
            'total_sections': len(all_metadata),
            'total_chapters': sum(m.get('total_chapters', 0) for m in all_metadata),
            'total_words': sum(m.get('total_words', 0) for m in all_metadata),
            'sections': all_metadata
        }
        
        # Save overall summary
        (self.output_dir / 'scraping_summary.json').write_text(
            json.dumps(summary, indent=2),
            encoding='utf-8'
        )
        
        logger.info("\n" + "="*60)
        logger.info("SCRAPING COMPLETE!")
        logger.info("="*60)
        logger.info(f"Total Sections: {summary['total_sections']}")
        logger.info(f"Total Chapters: {summary['total_chapters']}")
        logger.info(f"Total Words: {summary['total_words']:,}")
        logger.info(f"\nData saved to: {self.output_dir}")
        
        return summary


def main():
    """Main function to run scraper"""
    scraper = CharakaScraper()
    summary = scraper.scrape_all()
    
    print("\n" + "="*60)
    print("SCRAPING SUMMARY")
    print("="*60)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
