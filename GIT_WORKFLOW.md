# 🌳 Git Workflow & Branch Setup Guide

## Current Branch Status
```
master (root-commit a44306e)
├── develop
└── feature/complete-pipeline
```

All branches created and ready to use!

---

## 📋 Workflow Overview

### Daily Workflow
```
1. Switch to develop branch
   git checkout develop

2. Create/switch to feature branch
   git checkout -b feature/my-feature
   
3. Make changes and commit
   git add .
   git commit -m "type: description"
   
4. Push feature branch
   git push origin feature/my-feature
   
5. Create Pull Request on GitHub
   
6. After merge, update local
   git checkout develop
   git pull origin develop
```

---

## 🔀 Branch Descriptions

### `master` (Main Branch)
- ✅ Production-ready code only
- 🔒 Protected branch (requires PR review)
- 📦 Release versions tagged here
- **When to merge**: After PR review and testing

### `develop` (Integration Branch)
- 🟡 Latest development code
- ✅ All features merged here first
- 🧪 Testing branch
- **When to update**: After feature PRs are merged

### `feature/complete-pipeline` (Feature Branch)
- 🟠 Specific feature development
- 👤 Individual developer branch
- 🔧 Work-in-progress
- **When to delete**: After merging to develop

---

## 💬 Commit Message Format

Atomic commits with descriptive messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

### Examples
```
✓ feat(selenium): Add WebDriverWait for job cards
✓ fix(spider): Repair relative URLs to absolute
✓ feat(analysis): Add entry-level position counts
✓ docs: Update README with setup guide
✓ refactor(pipeline): Optimize skill extraction
```

---

## 🚀 Step-by-Step Examples

### Example 1: Fix Selenium Selectors
```powershell
# 1. Switch to develop
git checkout develop

# 2. Create feature branch
git checkout -b feature/fix-selectors

# 3. Edit selenium/extractor.py
# (edit file)

# 4. Stage and commit
git add selenium/extractor.py
git commit -m "fix(selenium): Update CSS selectors for job cards"

# 5. Push to remote
git push origin feature/fix-selectors

# 6. Create PR (on GitHub)
# 7. Merge PR
# 8. Delete feature branch
git checkout develop
git pull origin develop
git branch -d feature/fix-selectors
```

### Example 2: Add New Analysis Metric
```powershell
# 1. Create feature branch
git checkout develop
git checkout -b feature/job-salary-analysis

# 2. Edit analysis/summary.py
# (add salary analysis function)

# 3. Commit
git add analysis/summary.py
git commit -m "feat(analysis): Add salary range statistics"

# 4. Push and create PR
git push origin feature/job-salary-analysis
```

---

## 📊 Viewing Commit History

```powershell
# Simple log
git log --oneline

# Detailed log
git log --stat

# Graphical view
git log --graph --oneline --all

# Commits by author
git log --author="UCP Student"

# Last N commits
git log -n 5

# Commits with specific file
git log -- selenium/extractor.py
```

---

## 🔄 Branch Management

### List branches
```powershell
git branch              # Local branches
git branch -a           # All branches (local + remote)
git branch -v           # Branches with latest commit
```

### Switch branches
```powershell
git checkout develop
git checkout master
git checkout feature/complete-pipeline
```

### Delete branches
```powershell
# Delete local branch
git branch -d feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature
```

### Rename branch
```powershell
git branch -m old-name new-name
```

---

## 🔀 Merge Operations

### Merge feature to develop
```powershell
git checkout develop
git pull origin develop
git merge feature/complete-pipeline
git push origin develop
```

### Merge develop to master (Release)
```powershell
git checkout master
git pull origin master
git merge develop
git tag -a v1.0 -m "Release version 1.0"
git push origin master --tags
```

---

## 🛠️ Useful Git Commands

```powershell
# See what changed
git diff
git diff --staged

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Stash temporary work
git stash
git stash pop

# Check status
git status

# Rebase branches (cleaner history)
git rebase develop
```

---

## ✅ Pre-commit Checklist

Before committing code:
- [ ] Code tested locally
- [ ] No debug print statements
- [ ] Comments for complex logic
- [ ] Follows naming conventions
- [ ] No hardcoded values
- [ ] Logging added
- [ ] Error handling implemented

---

## 🚨 Common Issues & Fixes

### Accidentally committed to master
```powershell
# Move commits to new branch
git branch feature/my-feature
git reset --hard origin/master
git checkout feature/my-feature
```

### Need to undo last commit
```powershell
# Keep changes
git reset --soft HEAD~1

# Discard changes
git reset --hard HEAD~1
```

### Wrong commit message
```powershell
# Amend last commit
git commit --amend -m "New message"
git push origin branch-name --force
```

### Merge conflicts
```powershell
# View conflicts
git status

# After resolving in editor
git add .
git commit -m "Resolve merge conflicts"
git push origin branch-name
```

---

## 📚 References

- **Git Basics**: https://git-scm.com/book/en/v2
- **GitHub Flow**: https://guides.github.com/introduction/flow/
- **Conventional Commits**: https://www.conventionalcommits.org/

---

## 🎯 Assignment Submission

### Before Submitting
```powershell
# 1. Update master from develop
git checkout develop
git log --oneline -5          # View latest commits

git checkout master
git merge develop
git push origin master

# 2. Create release tag
git tag -a v1.0-assignment -m "UCP Assignment 1 - Complete"
git push origin --tags

# 3. Verify branches
git branch -a
git log --graph --oneline --all
```

### Summary
- ✅ All work committed to feature branch
- ✅ PRs created and reviewed
- ✅ Code merged to develop
- ✅ Develop merged to master
- ✅ Release tagged
- ✅ All commits have descriptive messages
