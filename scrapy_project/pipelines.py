"""
Scrapy Pipelines for Data Processing
"""

import csv
import re
import logging
from pathlib import Path
from datetime import datetime
from .items import JobItem

logger = logging.getLogger(__name__)

# Skill keywords to extract
SKILL_KEYWORDS = {
    'python': r'\bpython\b',
    'sql': r'\b(sql|sqlite|postgresql|mysql|oracle)\b',
    'pytorch': r'\b(pytorch|pyt torch)\b',
    'tensorflow': r'\btensorflow\b',
    'spark': r'\b(spark|pyspark|apache spark)\b',
    'r': r'\br\s|(?:^|\s)r\b',
}


class DataValidationPipeline:
    """Validates job data and ensures required fields are present."""
    
    REQUIRED_FIELDS = ['job_title', 'company', 'job_url', 'job_description']
    
    def process_item(self, item, spider):
        """Validate required fields."""
        for field in self.REQUIRED_FIELDS:
            if not item.get(field):
                raise DropItem(f"Missing required field: {field}")
        
        # Clean whitespace
        for field in ['job_title', 'company', 'location', 'job_description']:
            if field in item and isinstance(item[field], str):
                item[field] = ' '.join(item[field].split())
        
        return item


class SkillsExtractionPipeline:
    """Extracts tech skills from job descriptions."""
    
    def process_item(self, item, spider):
        """Extract skills from description."""
        description = item.get('job_description', '').lower()
        requirements = item.get('requirements', '').lower()
        combined_text = f"{description} {requirements}"
        
        extracted_skills = []
        for skill, pattern in SKILL_KEYWORDS.items():
            if re.search(pattern, combined_text, re.IGNORECASE):
                extracted_skills.append(skill)
        
        item['skills'] = extracted_skills
        logger.debug(f"Extracted skills for {item.get('job_title')}: {extracted_skills}")
        
        return item


class DuplicateCheckPipeline:
    """Checks for duplicate job listings."""
    
    def __init__(self):
        """Initialize dedupe set."""
        self.ids_seen = set()
    
    def process_item(self, item, spider):
        """Check for duplicates based on URL."""
        job_key = item['job_url']
        
        if job_key in self.ids_seen:
            logger.info(f"Duplicate found: {item.get('job_title')} from {item.get('company')}")
            raise DropItem(f"Duplicate job URL: {job_key}")
        
        self.ids_seen.add(job_key)
        return item


class CSVExportPipeline:
    """Exports processed jobs to CSV."""
    
    FIELDS = [
        'job_title',
        'company',
        'location',
        'department',
        'employment_type',
        'job_description',
        'requirements',
        'posted_date',
        'job_url',
        'source',
        'skills',
        'extracted_at'
    ]
    
    def __init__(self):
        """Initialize CSV writer."""
        self.output_file = 'data/final/jobs.csv'
        Path(self.output_file).parent.mkdir(parents=True, exist_ok=True)
        self.csv_file = None
        self.writer = None
        self.item_count = 0
    
    def open_spider(self, spider):
        """Open CSV file for writing."""
        self.csv_file = open(self.output_file, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.csv_file, fieldnames=self.FIELDS)
        self.writer.writeheader()
        logger.info(f"CSV export started: {self.output_file}")
    
    def close_spider(self, spider):
        """Close CSV file."""
        if self.csv_file:
            self.csv_file.close()
        logger.info(f"CSV export completed: {self.item_count} jobs saved to {self.output_file}")
    
    def process_item(self, item, spider):
        """Write item to CSV."""
        row = {field: item.get(field, '') for field in self.FIELDS}
        
        # Convert skills list to string
        if isinstance(row.get('skills'), list):
            row['skills'] = '; '.join(row['skills'])
        
        self.writer.writerow(row)
        self.item_count += 1
        
        return item


class DropItem(Exception):
    """Exception to drop items."""
    pass
