# 🎯 EXECUTION COMMANDS - Copy & Paste Ready

Quick reference for all commands needed to run the project.

---

## 🔧 INITIAL SETUP (First Time Only)

### 1. Create Virtual Environment
```powershell
cd "c:\Users\AHMED IMTIAZ\Desktop\Scrapper_T&T"
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Verify Installation
```powershell
python -c "import selenium; import scrapy; import pandas; print('✓ All packages installed')"
```

---

## 📥 CHROMEDRIVER SETUP

### 1. Download
- Go to: https://chromedriver.chromium.org/
- Select your Chrome version
- Download `.zip` file

### 2. Extract
- Open downloaded `.zip`
- Extract `chromedriver.exe` to:
  ```
  c:\Users\AHMED IMTIAZ\Desktop\Scrapper_T&T\selenium\chromedriver.exe
  ```

### 3. Verify
```powershell
Test-Path "selenium\chromedriver.exe"
```

---

## 🚀 RUN THE PIPELINE

### Option A: Run Complete Pipeline (Recommended)
```powershell
python run_project.py all
```

### Option B: Run Individual Steps

**Only Selenium Extraction**
```powershell
python run_project.py extract
```

**Only Scrapy Processing**
```powershell
python run_project.py scrape
```

**Only Analysis**
```powershell
python run_project.py analyze
```

---

## 📊 CHECK RESULTS

### View Extracted Links (Raw)
```powershell
# Show first 10 rows
Get-Content data\raw\job_links.csv | Select-Object -First 10

# Or open in Excel/Notepad
notepad data\raw\job_links.csv
```

### View Processed Jobs (Final)
```powershell
# Show job count
(Get-Content data\final\jobs.csv | Measure-Object -Line).Lines

# Open in Excel
Invoke-Item data\final\jobs.csv
```

### View Analysis Report
```powershell
# Display in terminal
Get-Content analysis\workforce_analysis.txt

# Or open in Notepad
notepad analysis\workforce_analysis.txt
```

---

## 🌳 GIT COMMANDS

### Check Current Status
```powershell
git status
git branch          # Show current branch
git log --oneline   # Show commit history
```

### Make Commits
```powershell
# Stage all changes
git add .

# Commit with message
git commit -m "feat: Complete ETL pipeline with Selenium, Scrapy, and Analysis"

# View commit
git log -1
```

### Switch Branches
```powershell
# View all branches
git branch -a

# Switch to develop
git checkout develop

# Switch to feature branch
git checkout feature/complete-pipeline

# Switch back to master
git checkout master
```

### Create & Push Feature Branch
```powershell
# Create new feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: description of changes"

# Push to remote
git push origin feature/my-feature
```

### Merge After Testing
```powershell
# Merge develop into master (production)
git checkout master
git pull origin master
git merge develop
git push origin master

# Tag release
git tag -a v1.0 -m "Release v1.0"
git push origin --tags
```

---

## 🔍 DEBUGGING COMMANDS

### View Logs
```powershell
# Selenium logs
Get-Content selenium\extraction.log -Tail 50

# Scrapy logs
Get-Content scrapy_project\logs\scrapy.log -Tail 50

# Analysis logs
Get-Content analysis\analysis.log -Tail 50
```

### Count Results
```powershell
# Count job links extracted
$links = (Get-Content data\raw\job_links.csv | Measure-Object -Line).Lines - 1
Write-Output "Links found: $links"

# Count jobs processed
$jobs = (Get-Content data\final\jobs.csv | Measure-Object -Line).Lines - 1
Write-Output "Jobs processed: $jobs"
```

### Validate CSV Files
```powershell
# Test if CSV is readable
$csv = Import-Csv data\final\jobs.csv
Write-Output "Total jobs: $($csv.Count)"
Write-Output "Columns: $($csv[0].PSObject.Properties.Name -join ', ')"
```

---

## 🧹 CLEANUP COMMANDS

### Clear Cache & Logs
```powershell
# Remove Scrapy cache
Remove-Item -Recurse -Force scrapy_project\httpcache

# Remove logs
Remove-Item selenium\extraction.log
Remove-Item scrapy_project\logs\scrapy.log
Remove-Item analysis\analysis.log

# Remove old data (keep backups first!)
Remove-Item data\raw\*.csv
Remove-Item data\final\*.csv
```

### Git Cleanup
```powershell
# Delete old feature branch
git branch -d feature/old-feature

# Force delete remote branch
git push origin --delete feature/old-feature

# Show all branches
git branch -a
```

---

## 📋 COMPLETE EXECUTION SEQUENCE

### Fresh Start (First Run)
```powershell
# 1. Setup
cd "c:\Users\AHMED IMTIAZ\Desktop\Scrapper_T&T"
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Verify ChromeDriver exists
Test-Path "selenium\chromedriver.exe"

# 3. Git setup
git status
git branch -a

# 4. Run pipeline
python run_project.py all

# 5. Check results
Get-Content analysis\workforce_analysis.txt

# 6. Commit
git add .
git commit -m "feat: Initial ETL pipeline with all components"
git push origin develop
```

### Subsequent Runs
```powershell
# 1. Activate venv
venv\Scripts\Activate.ps1

# 2. Run pipeline
python run_project.py all

# 3. Commit changes
git add .
git commit -m "chore: Updated job data from latest run"
git push origin develop
```

---

## 🎓 UCP SUBMISSION CHECKLIST

```powershell
# Before submitting:

# 1. Verify all branches exist
git branch -a

# 2. View commit history
git log --oneline -10

# 3. Ensure master has latest
git checkout master
git pull origin develop
git merge develop

# 4. Tag release
git tag -a ucp-assignment-1 -m "UCP Assignment 1 Submission"

# 5. Push everything
git push origin --all
git push origin --tags

# 6. Final verification
git log --graph --oneline --all
```

---

## 📝 NOTES

- **First run**: 5-10 minutes (scraping takes time)
- **Subsequent runs**: 3-5 minutes (caching helps)
- **ChromeDriver**: Update when Chrome browser updates
- **Virtual env**: Always activate before running
- **Logs**: Check for errors in log files

---

## ⚡ QUICK COMMANDS CHEAT SHEET

```powershell
# Activate venv
venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt

# Run pipeline
python run_project.py all

# Check status
git status

# Make commit
git add . ; git commit -m "message"

# Push code
git push origin develop

# View logs
Get-Content selenium\extraction.log -Tail 20

# View results
Import-Csv data\final\jobs.csv | Format-Table
```

---

**Ready? Start with: `python run_project.py all`** 🚀
