"""
Job Market Analysis - Workforce Insights Summary
Processes jobs.csv to answer key business questions
"""

import csv
import pandas as pd
import logging
from pathlib import Path
from collections import Counter
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis/analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class JobAnalyzer:
    """Analyzes job market data for workforce insights."""
    
    def __init__(self, csv_file='data/final/jobs.csv'):
        """Initialize analyzer with CSV data."""
        self.csv_file = csv_file
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and parse job data."""
        try:
            if not Path(self.csv_file).exists():
                logger.error(f"File not found: {self.csv_file}")
                logger.error("Run Scrapy spider first: python run_project.py scrape")
                raise FileNotFoundError(self.csv_file)
            
            self.df = pd.read_csv(self.csv_file, encoding='utf-8')
            logger.info(f"Loaded {len(self.df)} jobs from {self.csv_file}")
            logger.info(f"Columns: {', '.join(self.df.columns)}")
            
            # Display basic stats
            logger.info(f"\nData Summary:")
            logger.info(f"  Total jobs: {len(self.df)}")
            logger.info(f"  Unique companies: {self.df['company'].nunique()}")
            logger.info(f"  Unique locations: {self.df['location'].nunique()}")
        
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def analyze_top_skills(self, top_n=5):
        """Find top N most common skills."""
        logger.info(f"\n{'='*60}")
        logger.info(f"TOP {top_n} SKILLS")
        logger.info(f"{'='*60}")
        
        all_skills = []
        for skills_str in self.df['skills'].dropna():
            if isinstance(skills_str, str) and skills_str.strip():
                skills = [s.strip() for s in skills_str.split(';')]
                all_skills.extend(skills)
        
        if not all_skills:
            logger.warning("No skills data found")
            return []
        
        skill_counts = Counter(all_skills)
        top_skills = skill_counts.most_common(top_n)
        
        for rank, (skill, count) in enumerate(top_skills, 1):
            pct = (count / len(self.df)) * 100
            logger.info(f"{rank}. {skill.upper()}: {count} jobs ({pct:.1f}%)")
            print(f"{rank}. {skill.upper()}: {count} jobs ({pct:.1f}%)")
        
        return top_skills
    
    def analyze_top_locations(self, top_n=5):
        """Find cities/regions with most openings."""
        logger.info(f"\n{'='*60}")
        logger.info(f"TOP {top_n} LOCATIONS")
        logger.info(f"{'='*60}")
        
        location_counts = self.df['location'].value_counts().head(top_n)
        
        for rank, (location, count) in enumerate(location_counts.items(), 1):
            pct = (count / len(self.df)) * 100
            logger.info(f"{rank}. {location}: {count} openings ({pct:.1f}%)")
            print(f"{rank}. {location}: {count} openings ({pct:.1f}%)")
        
        return location_counts.to_dict()
    
    def analyze_top_companies(self, top_n=5):
        """Find companies posting most relevant roles."""
        logger.info(f"\n{'='*60}")
        logger.info(f"TOP {top_n} COMPANIES")
        logger.info(f"{'='*60}")
        
        company_counts = self.df['company'].value_counts().head(top_n)
        
        for rank, (company, count) in enumerate(company_counts.items(), 1):
            pct = (count / len(self.df)) * 100
            logger.info(f"{rank}. {company}: {count} positions ({pct:.1f}%)")
            print(f"{rank}. {company}: {count} positions ({pct:.1f}%)")
        
        return company_counts.to_dict()
    
    def analyze_entry_level(self):
        """Count internship, junior, or entry-level positions."""
        logger.info(f"\n{'='*60}")
        logger.info(f"ENTRY-LEVEL POSITIONS")
        logger.info(f"{'='*60}")
        
        entry_keywords = ['internship', 'junior', 'entry-level', 'entry level', 'graduate', 'trainee']
        
        entry_count = 0
        matching_jobs = []
        
        for idx, row in self.df.iterrows():
            title = str(row.get('job_title', '')).lower()
            desc = str(row.get('job_description', '')).lower()
            combined = f"{title} {desc}"
            
            if any(keyword in combined for keyword in entry_keywords):
                entry_count += 1
                matching_jobs.append(row['job_title'])
        
        pct = (entry_count / len(self.df)) * 100
        logger.info(f"Entry-level positions: {entry_count} ({pct:.1f}% of total)")
        logger.info(f"Examples:")
        for job in matching_jobs[:5]:
            logger.info(f"  - {job}")
            print(f"  - {job}")
        
        return {
            'count': entry_count,
            'percentage': pct,
            'examples': matching_jobs[:10]
        }
    
    def analyze_top_titles(self, top_n=5):
        """Find most common job title patterns."""
        logger.info(f"\n{'='*60}")
        logger.info(f"TOP {top_n} JOB TITLES")
        logger.info(f"{'='*60}")
        
        title_counts = self.df['job_title'].value_counts().head(top_n)
        
        for rank, (title, count) in enumerate(title_counts.items(), 1):
            pct = (count / len(self.df)) * 100
            logger.info(f"{rank}. {title}: {count} positions ({pct:.1f}%)")
            print(f"{rank}. {title}: {count} positions ({pct:.1f}%)")
        
        return title_counts.to_dict()
    
    def generate_report(self, output_file='analysis/workforce_analysis.txt'):
        """Generate complete analysis report."""
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("JOB MARKET ANALYSIS - WORKFORCE INSIGHTS\n")
            f.write("=" * 60 + "\n\n")
            
            # Summary
            f.write(f"DATA SUMMARY\n")
            f.write(f"Total jobs analyzed: {len(self.df)}\n")
            f.write(f"Unique companies: {self.df['company'].nunique()}\n")
            f.write(f"Unique locations: {self.df['location'].nunique()}\n")
            f.write(f"Employment types: {self.df['employment_type'].nunique()}\n\n")
            
            # Top Skills
            f.write("TOP 5 SKILLS\n")
            f.write("-" * 40 + "\n")
            skills = self.analyze_top_skills(5)
            for rank, (skill, count) in enumerate(skills, 1):
                pct = (count / len(self.df)) * 100
                f.write(f"{rank}. {skill.upper()}: {count} ({pct:.1f}%)\n")
            f.write("\n")
            
            # Top Locations
            f.write("TOP 5 LOCATIONS\n")
            f.write("-" * 40 + "\n")
            locations = self.analyze_top_locations(5)
            for rank, (loc, count) in enumerate(locations.items(), 1):
                pct = (count / len(self.df)) * 100
                f.write(f"{rank}. {loc}: {count} ({pct:.1f}%)\n")
            f.write("\n")
            
            # Top Companies
            f.write("TOP 5 COMPANIES\n")
            f.write("-" * 40 + "\n")
            companies = self.analyze_top_companies(5)
            for rank, (co, count) in enumerate(companies.items(), 1):
                pct = (count / len(self.df)) * 100
                f.write(f"{rank}. {co}: {count} ({pct:.1f}%)\n")
            f.write("\n")
            
            # Entry Level
            f.write("ENTRY-LEVEL POSITIONS\n")
            f.write("-" * 40 + "\n")
            entry = self.analyze_entry_level()
            f.write(f"Count: {entry['count']} ({entry['percentage']:.1f}%)\n")
            f.write("\n")
            
            # Top Titles
            f.write("TOP 5 JOB TITLES\n")
            f.write("-" * 40 + "\n")
            titles = self.analyze_top_titles(5)
            for rank, (title, count) in enumerate(titles.items(), 1):
                pct = (count / len(self.df)) * 100
                f.write(f"{rank}. {title}: {count} ({pct:.1f}%)\n")
        
        logger.info(f"\n✓ Report saved to {output_file}")
        return output_file
    
    def run_analysis(self):
        """Run complete analysis."""
        try:
            logger.info("Starting Job Market Analysis\n")
            
            self.analyze_top_skills(5)
            self.analyze_top_locations(5)
            self.analyze_top_companies(5)
            self.analyze_entry_level()
            self.analyze_top_titles(5)
            
            report_file = self.generate_report()
            
            logger.info(f"\n{'='*60}")
            logger.info("✅ ANALYSIS COMPLETE")
            logger.info(f"{'='*60}")
            logger.info(f"Report saved to: {report_file}")
            
            return True
        
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}", exc_info=True)
            return False


def main():
    """Main execution."""
    try:
        analyzer = JobAnalyzer('data/final/jobs.csv')
        success = analyzer.run_analysis()
        return 0 if success else 1
    except FileNotFoundError:
        logger.error("Jobs CSV file not found. Run complete pipeline first.")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
