"""
Main Job Market Monitoring System - CLI Runner
Orchestrates the complete ETL pipeline: Extract → Process → Analyze
"""

import sys
import argparse
import logging
import subprocess
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProjectRunner:
    """Runs the complete job market monitoring pipeline."""
    
    def __init__(self):
        """Initialize project runner."""
        self.project_root = Path(__file__).parent
        self.script_paths = {
            'extract': self.project_root / 'selenium' / 'extractor.py',
            'scrape': self.project_root / 'scrapy_project' / 'spiders' / 'job_market.py',
            'analyze': self.project_root / 'analysis' / 'summary.py',
        }
    
    def extract_jobs(self):
        """Run Selenium extractor."""
        logger.info("\n" + "="*60)
        logger.info("STEP 1: SELENIUM JOB EXTRACTION")
        logger.info("="*60)
        
        try:
            cmd = [sys.executable, str(self.project_root / 'selenium' / 'extractor.py')]
            result = subprocess.run(cmd, check=True)
            logger.info("✓ Extraction complete - Links saved to data/raw/job_links.csv")
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Extraction failed: {str(e)}")
            return False
        except FileNotFoundError:
            logger.error("✗ ChromeDriver not found. Download from https://chromedriver.chromium.org/")
            logger.error("   Place in selenium/ directory")
            return False
    
    def scrape_jobs(self):
        """Run Scrapy spider."""
        logger.info("\n" + "="*60)
        logger.info("STEP 2: SCRAPY JOB DETAIL EXTRACTION")
        logger.info("="*60)
        
        try:
            cmd = [
                sys.executable, '-m', 'scrapy', 'crawl', 'job_market',
                '-a', 'csv_file=data/raw/job_links.csv',
                '-s', 'JOBDIR=scrapy_project/job_cache',
                '-s', 'LOG_FILE=scrapy_project/logs/scrapy.log'
            ]
            
            # Change to project directory
            result = subprocess.run(cmd, cwd=str(self.project_root), check=True)
            logger.info("✓ Scraping complete - Jobs saved to data/final/jobs.csv")
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Scraping failed: {str(e)}")
            return False
    
    def analyze_jobs(self):
        """Run analysis script."""
        logger.info("\n" + "="*60)
        logger.info("STEP 3: WORKFORCE ANALYSIS")
        logger.info("="*60)
        
        try:
            cmd = [sys.executable, str(self.project_root / 'analysis' / 'summary.py')]
            result = subprocess.run(cmd, check=True)
            logger.info("✓ Analysis complete - Report saved to analysis/workforce_analysis.txt")
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Analysis failed: {str(e)}")
            return False
    
    def run_all(self):
        """Run complete pipeline."""
        logger.info("\n" + "█"*60)
        logger.info("█  JOB MARKET MONITORING SYSTEM - COMPLETE PIPELINE")
        logger.info("█"*60)
        
        # Step 1: Extract
        if not self.extract_jobs():
            logger.error("Pipeline stopped at extraction")
            return False
        
        # Step 2: Scrape
        if not self.scrape_jobs():
            logger.error("Pipeline stopped at scraping")
            return False
        
        # Step 3: Analyze
        if not self.analyze_jobs():
            logger.error("Pipeline stopped at analysis")
            return False
        
        logger.info("\n" + "█"*60)
        logger.info("█  ✅ COMPLETE PIPELINE SUCCESS")
        logger.info("█"*60)
        logger.info("\n📊 Output Files Generated:")
        logger.info("  • data/raw/job_links.csv - Extracted job links")
        logger.info("  • data/final/jobs.csv - Processed job details")
        logger.info("  • analysis/workforce_analysis.txt - Analysis report")
        logger.info("\nNext steps:")
        logger.info("  1. Review data/final/jobs.csv for job details")
        logger.info("  2. Check analysis/workforce_analysis.txt for insights")
        logger.info("  3. Commit changes to git\n")
        
        return True
    
    def validate_setup(self):
        """Validate project setup."""
        logger.info("Validating project setup...")
        
        required_dirs = [
            'selenium',
            'scrapy_project',
            'analysis',
            'data/raw',
            'data/final'
        ]
        
        for dir_path in required_dirs:
            path = self.project_root / dir_path
            if not path.exists():
                logger.error(f"✗ Missing directory: {dir_path}")
                return False
        
        logger.info("✓ Project structure valid")
        return True


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='Job Market Monitoring System - Complete ETL Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_project.py all       # Run complete pipeline
  python run_project.py extract   # Only run Selenium extraction
  python run_project.py scrape    # Only run Scrapy spider
  python run_project.py analyze   # Only run analysis
        """
    )
    
    parser.add_argument(
        'command',
        choices=['all', 'extract', 'scrape', 'analyze', 'validate'],
        help='Command to run'
    )
    
    args = parser.parse_args()
    
    runner = ProjectRunner()
    
    # Validate setup
    if not runner.validate_setup():
        logger.error("Project setup validation failed")
        return 1
    
    # Execute command
    if args.command == 'all':
        success = runner.run_all()
    elif args.command == 'extract':
        success = runner.extract_jobs()
    elif args.command == 'scrape':
        success = runner.scrape_jobs()
    elif args.command == 'analyze':
        success = runner.analyze_jobs()
    elif args.command == 'validate':
        logger.info("✓ Project setup is valid")
        return 0
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
