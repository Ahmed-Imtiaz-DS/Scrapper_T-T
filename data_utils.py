"""
Data Utility Functions for Job Market System
"""

import csv
import re
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates job data"""
    
    @staticmethod
    def validate_url(url):
        """Validate URL format."""
        if not url:
            return False
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url))
    
    @staticmethod
    def validate_job_title(title):
        """Validate job title."""
        return isinstance(title, str) and len(title.strip()) > 2
    
    @staticmethod
    def validate_description(description):
        """Validate job description."""
        return isinstance(description, str) and len(description.strip()) > 50
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize text."""
        if not isinstance(text, str):
            return ''
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove special characters except punctuation
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)
        return text.strip()


class DataProcessor:
    """Processes job data"""
    
    @staticmethod
    def deduplicate_jobs(csv_file):
        """Remove duplicate jobs from CSV."""
        try:
            jobs = {}
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    job_url = row.get('job_url', '')
                    if job_url and job_url not in jobs:
                        jobs[job_url] = row
            
            # Write deduplicated data
            if jobs:
                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=jobs[list(jobs.keys())[0]].keys())
                    writer.writeheader()
                    writer.writerows(jobs.values())
                
                logger.info(f"Deduplicated {len(jobs)} unique jobs in {csv_file}")
            
            return len(jobs)
        except Exception as e:
            logger.error(f"Error deduplicating: {str(e)}")
            return 0
    
    @staticmethod
    def filter_jobs_by_keyword(csv_file, keyword, output_file=None):
        """Filter jobs by keyword in title or description."""
        filtered_jobs = []
        keyword_lower = keyword.lower()
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row.get('job_title', '').lower()
                    desc = row.get('job_description', '').lower()
                    
                    if keyword_lower in title or keyword_lower in desc:
                        filtered_jobs.append(row)
            
            if output_file:
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    if filtered_jobs:
                        writer = csv.DictWriter(f, fieldnames=filtered_jobs[0].keys())
                        writer.writeheader()
                        writer.writerows(filtered_jobs)
                logger.info(f"Filtered {len(filtered_jobs)} jobs to {output_file}")
            
            return filtered_jobs
        except Exception as e:
            logger.error(f"Error filtering jobs: {str(e)}")
            return []
    
    @staticmethod
    def extract_skills_from_description(description):
        """Extract tech skills from job description."""
        skills_keywords = {
            'python': r'\bpython\b',
            'sql': r'\b(sql|sqlite|postgresql|mysql)\b',
            'pytorch': r'\bpytorch\b',
            'tensorflow': r'\btensorflow\b',
            'spark': r'\b(spark|pyspark)\b',
            'r': r'\br\b',
            'java': r'\bjava\b',
            'javascript': r'\b(javascript|js)\b',
            'scala': r'\bscala\b',
            'hadoop': r'\bhadoop\b',
        }
        
        found_skills = []
        desc_lower = description.lower()
        
        for skill, pattern in skills_keywords.items():
            if re.search(pattern, desc_lower, re.IGNORECASE):
                found_skills.append(skill)
        
        return found_skills
    
    @staticmethod
    def generate_stats(csv_file):
        """Generate statistics from job CSV."""
        try:
            data = {
                'total_jobs': 0,
                'unique_companies': set(),
                'unique_locations': set(),
                'employment_types': {},
                'avg_description_length': 0,
                'total_description_length': 0,
            }
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data['total_jobs'] += 1
                    data['unique_companies'].add(row.get('company', 'Unknown'))
                    data['unique_locations'].add(row.get('location', 'Unknown'))
                    
                    emp_type = row.get('employment_type', 'Unknown')
                    data['employment_types'][emp_type] = data['employment_types'].get(emp_type, 0) + 1
                    
                    desc_len = len(row.get('job_description', ''))
                    data['total_description_length'] += desc_len
            
            data['unique_companies'] = len(data['unique_companies'])
            data['unique_locations'] = len(data['unique_locations'])
            
            if data['total_jobs'] > 0:
                data['avg_description_length'] = data['total_description_length'] / data['total_jobs']
            
            del data['total_description_length']
            
            return data
        except Exception as e:
            logger.error(f"Error generating stats: {str(e)}")
            return {}


class DataExporter:
    """Exports job data to various formats"""
    
    @staticmethod
    def export_to_json(csv_file, json_file):
        """Convert CSV to JSON."""
        import json
        try:
            jobs = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                jobs = list(reader)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported {len(jobs)} jobs to {json_file}")
            return len(jobs)
        except Exception as e:
            logger.error(f"Error exporting to JSON: {str(e)}")
            return 0
    
    @staticmethod
    def export_filtered_by_company(csv_file, company_name, output_file):
        """Export jobs for specific company."""
        try:
            jobs = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('company', '').lower() == company_name.lower():
                        jobs.append(row)
            
            if jobs:
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
                    writer.writeheader()
                    writer.writerows(jobs)
                logger.info(f"Exported {len(jobs)} jobs for {company_name} to {output_file}")
            
            return len(jobs)
        except Exception as e:
            logger.error(f"Error exporting by company: {str(e)}")
            return 0


# Logging setup
def setup_logging(log_file='data_utils.log'):
    """Setup logging for data utilities."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
