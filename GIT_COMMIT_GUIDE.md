# ?? Git Commit Guide - Matchlogs Update v0.7.4

## ?? Lista Plików do Zacommitowania

### ? Zmodyfikowane (Modified)
```
app/backend/routers/matchlogs.py
app/backend/main.py
README.md
app/backend/README.md
app/frontend/README.md
API_ENDPOINTS_GUIDE.md
```

### ? Nowe (New)
```
README_MATCHLOGS_UPDATE.md
API_COMPLETE_REFERENCE.md
CHECKLIST_MATCHLOGS_UPDATE.md
MIGRATION_GUIDE_MATCHLOGS.md
FINAL_SUMMARY.md
GIT_COMMIT_GUIDE.md (ten plik)
```

### ?? Backupy (NIE commitowaæ!)
```
app/backend/routers/matchlogs.py.backup
app/backend/main.py.backup
README.md.backup
app/backend/README.md.backup
app/frontend/README.md.backup
API_ENDPOINTS_GUIDE.md.backup
```

---

## ?? Komendy Git

### SprawdŸ status
```bash
cd polish-players-tracker
git status
```

### Dodaj zmodyfikowane pliki
```bash
# Backend code
git add app/backend/routers/matchlogs.py
git add app/backend/main.py

# Documentation
git add README.md
git add app/backend/README.md
git add app/frontend/README.md
git add API_ENDPOINTS_GUIDE.md

# New documentation files
git add README_MATCHLOGS_UPDATE.md
git add API_COMPLETE_REFERENCE.md
git add CHECKLIST_MATCHLOGS_UPDATE.md
git add MIGRATION_GUIDE_MATCHLOGS.md
git add FINAL_SUMMARY.md
git add GIT_COMMIT_GUIDE.md
```

### Lub dodaj wszystko (bez backupów)
```bash
# Add all except backups
git add --all
git reset -- "*.backup"
```

### Commit z opisem
```bash
git commit -m "feat: Refactor matchlogs endpoints to /api/matchlogs prefix

BREAKING CHANGE: Matchlogs endpoints moved from /api/players/{id}/matches to /api/matchlogs/{id}

Changes:
- Moved matchlogs router prefix from /api/players to /matchlogs
- Updated endpoint paths for better organization
- Updated all documentation (6 files)
- Added 5 new documentation files
- Improved Swagger/ReDoc documentation

New endpoints:
- GET /api/matchlogs/{player_id} (was: /api/players/{id}/matches)
- GET /api/matchlogs/{player_id}/stats (was: /api/players/{id}/matches/stats)
- GET /api/matchlogs/match/{match_id} (was: /api/players/matches/{id})

Migration guide: See MIGRATION_GUIDE_MATCHLOGS.md

Version: 0.7.4"
```

### Tag release (opcjonalnie)
```bash
git tag -a v0.7.4 -m "Version 0.7.4: Matchlogs endpoints refactoring"
```

### Push
```bash
git push origin main
git push origin --tags  # jeœli utworzy³eœ tag
```

---

## ?? .gitignore

Upewnij siê, ¿e `.gitignore` zawiera:
```
*.backup
*.bak
```

SprawdŸ:
```bash
cat .gitignore | grep backup
```

Jeœli nie ma, dodaj:
```bash
echo "*.backup" >> .gitignore
echo "*.bak" >> .gitignore
git add .gitignore
git commit -m "chore: Add backup files to .gitignore"
```

---

## ?? Weryfikacja Przed Commitem

### 1. SprawdŸ co zostanie zacommitowane
```bash
git diff --cached
```

### 2. SprawdŸ czy backupy nie s¹ w staged
```bash
git status | grep backup
# Powinno byæ puste
```

### 3. SprawdŸ czy wszystkie nowe pliki s¹ dodane
```bash
git status --short
# Powinny byæ wszystkie pliki jako 'A' (added) lub 'M' (modified)
```

---

## ?? Alternatywny Commit Message (Conventional Commits)

```bash
git commit -m "feat!: refactor matchlogs endpoints structure

BREAKING CHANGE: Matchlogs API endpoints have been reorganized under /api/matchlogs prefix

Previous endpoints (removed):
- GET /api/players/{id}/matches
- GET /api/players/{id}/matches/stats  
- GET /api/players/matches/{id}

New endpoints:
- GET /api/matchlogs/{id}
- GET /api/matchlogs/{id}/stats
- GET /api/matchlogs/match/{id}

Modified:
- app/backend/routers/matchlogs.py: Updated router prefix and paths
- app/backend/main.py: Updated Swagger documentation
- README.md: Added matchlogs section
- app/backend/README.md: Updated all matchlogs references
- app/frontend/README.md: Added matchlogs integration examples
- API_ENDPOINTS_GUIDE.md: Updated all examples and URLs

Added:
- README_MATCHLOGS_UPDATE.md: Detailed change documentation
- API_COMPLETE_REFERENCE.md: Complete API reference
- CHECKLIST_MATCHLOGS_UPDATE.md: Testing checklist
- MIGRATION_GUIDE_MATCHLOGS.md: Migration guide for developers
- FINAL_SUMMARY.md: Project update summary
- GIT_COMMIT_GUIDE.md: Git workflow guide

For migration instructions see: MIGRATION_GUIDE_MATCHLOGS.md
For testing checklist see: CHECKLIST_MATCHLOGS_UPDATE.md

Closes #[issue-number] (if applicable)"
```

---

## ?? Workflow dla Feature Branch

Jeœli pracujesz na osobnym branchu:

```bash
# Utwórz branch
git checkout -b feature/matchlogs-refactor

# Add & commit (jak wy¿ej)
git add ...
git commit -m "..."

# Push do remote
git push -u origin feature/matchlogs-refactor

# Utwórz Pull Request na GitHubie/GitLab
# Po merge, usuñ branch:
git checkout main
git pull
git branch -d feature/matchlogs-refactor
```

---

## ?? Czyszczenie Po Commicie

### Usuñ backupy lokalnie
```bash
# Z katalogu g³ównego projektu
find . -name "*.backup" -type f -delete

# Lub rêcznie:
rm app/backend/routers/matchlogs.py.backup
rm app/backend/main.py.backup
rm README.md.backup
rm app/backend/README.md.backup
rm app/frontend/README.md.backup
rm API_ENDPOINTS_GUIDE.md.backup
```

### Opcjonalnie: commit usuniêcia backupów
```bash
git add -u
git commit -m "chore: Remove backup files"
git push
```

---

## ?? Podsumowanie Zmian dla CHANGELOG.md

Jeœli masz plik CHANGELOG.md, dodaj:

```markdown
## [0.7.4] - 2025-01-XX

### Changed (BREAKING)
- **Matchlogs endpoints refactored** - Moved from `/api/players/{id}/matches` to `/api/matchlogs/{id}`
- Endpoint paths updated for better API organization
- Router prefix changed from `/api/players` to `/matchlogs`

### Added
- New comprehensive API documentation (5 new .md files)
- Migration guide for developers using old endpoints
- Complete API reference documentation
- Testing checklist for matchlogs endpoints

### Updated
- All documentation files with new endpoint paths
- Swagger/ReDoc documentation
- Frontend README with integration examples

### Migration
See MIGRATION_GUIDE_MATCHLOGS.md for detailed migration instructions.

### Endpoints
**Before:**
- GET /api/players/{id}/matches
- GET /api/players/{id}/matches/stats
- GET /api/players/matches/{id}

**After:**
- GET /api/matchlogs/{id}
- GET /api/matchlogs/{id}/stats
- GET /api/matchlogs/match/{id}
```

---

## ? Checklist Przed Push

- [ ] Wszystkie testy przesz³y
- [ ] Backend uruchamia siê bez b³êdów
- [ ] Swagger UI wyœwietla poprawnie endpointy
- [ ] Dokumentacja jest aktualna
- [ ] Backupy NIE s¹ w commit
- [ ] Commit message jest opisowy
- [ ] .gitignore zawiera *.backup

---

## ?? Problemy i Rozwi¹zania

### Problem: Przypadkowo zacommitowa³em backupy

```bash
# Usuñ z ostatniego commita (przed push)
git reset --soft HEAD~1
git reset HEAD *.backup
git commit -m "..."  # powtórz commit bez backupów
```

### Problem: Push nie dzia³a

```bash
# SprawdŸ remote
git remote -v

# Pull najpierw jeœli s¹ zmiany
git pull origin main --rebase
git push origin main
```

### Problem: Konflikt w dokumentacji

```bash
# Jeœli konflikt w README.md:
git pull origin main
# Rozwi¹¿ konflikty rêcznie
git add .
git commit -m "merge: Resolve conflicts"
git push
```

---

**Przygotowane przez:** Rovo Dev
**Data:** 2025-01-XX
**Projekt:** Polish Football Data Hub International v0.7.4
