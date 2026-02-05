#!/usr/bin/env python3
"""
Script 01: Scrape Charaka Samhita Data

This script scrapes all 8 sections from Charaka Samhita Online.
Run this first before building the vector database.

Usage:
    python scripts/01_scrape_data.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from scraper.charaka_scraper import CharakaScraper
from scraper.data_processor import AyurvedicTextProcessor


def main():
    """Main execution"""
    print("=" * 70)
    print(" AYURMIND - DATA COLLECTION PIPELINE")
    print(" Phase 1: Web Scraping & Text Processing")
    print("=" * 70)
    print()
    
    # Step 1: Scrape data
    print("STEP 1: Scraping Charaka Samhita Online")
    print("-" * 70)
    scraper = CharakaScraper()
    scraping_summary = scraper.scrape_all()
    
    print("\n" + "=" * 70)
    print("SCRAPING COMPLETE!")
    print(f"Scraped {scraping_summary['total_sections']} sections")
    print(f"Total chapters: {scraping_summary['total_chapters']}")
    print(f"Total words: {scraping_summary['total_words']:,}")
    print("=" * 70)
    
    # Step 2: Process and chunk data
    print("\n\nSTEP 2: Processing and Chunking Text")
    print("-" * 70)
    processor = AyurvedicTextProcessor()
    processing_summary = processor.process_all()
    
    print("\n" + "=" * 70)
    print("PROCESSING COMPLETE!")
    print(f"Created {processing_summary['total_chunks']:,} chunks")
    print(f"Total tokens: {processing_summary['total_tokens']:,}")
    print(f"Avg chunk size: {processing_summary['avg_chunk_size']:.0f} tokens")
    print()
    print("Category breakdown:")
    for category, count in processing_summary['categories'].items():
        print(f"  - {category}: {count} chunks")
    print("=" * 70)
    
    print("\n✅ SUCCESS! Data is ready for vector database creation.")
    print("   Next step: Run 'python scripts/02_build_vectordb.py'")


if __name__ == "__main__":
    main()
