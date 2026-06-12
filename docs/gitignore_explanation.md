# Gitignore Explanation - ValoryAI (ValorAI)

To maintain a clean repository and protect sensitive credentials, the project implements a hardened, production-grade `.gitignore` at the root. This document explains the categories of files excluded from version control.

---

## Excluded Categories

### 1. Environment and Secrets
- **Files**: `.env`, `.env.local`, `.env.*`, `*.pem`, `*.key`
- **Rationale**: Environmental files store credentials (e.g. database credentials, Firebase API keys). Committing these leaks access and compromises cloud assets.
- **Exception**: `.env.example` files containing non-sensitive placeholder configurations *are* tracked to guide developers.

### 2. Dependency Artifacts
- **Files**: `/node_modules`, `/.pnp`, `/.pnp.js`, `/.dart_tool/`, `.flutter-plugins`, `.flutter-plugins-dependencies`, `/build/`
- **Rationale**: Package managers (`npm`, `pub`) download third-party libraries locally. These directories are large, platform-dependent, and easily reconstructed using `npm install` or `flutter pub get`.

### 3. Compilation Outputs and Build Targets
- **Files**: `/dist`, `/out`, `*.pyc`, `__pycache__/`, `*.class`, `*.o`, `*.exe`
- **Rationale**: Compiled artifacts represent machine-generated code. Versioning them bloats the repository size and leads to git diff merge conflicts.

### 4. Testing, Logs, and Coverage Reports
- **Files**: `/coverage`, `*.log`, `*_dev.log`, `*_dev.out.log`, `.pytest_cache/`
- **Rationale**: Execution traces and coverage stats change with every run. Excluded to keep commits meaningful and focused only on source code modifications.

### 5. Editor and IDE Configurations
- **Files**: `/.vscode`, `/.idea`, `/*.iml`, `/*.suo`, `/*.ntvs*`
- **Rationale**: Local settings for VS Code or IntelliJ/Android Studio are developer-specific. Forcing these settings on other contributors creates friction.

### 6. Large Data Files and Temp Files
- **Files**: `*.jsonl`, `*.zip`, `*.csv`, `*.parquet`, `*.tmp`
- **Rationale**: Datasets can be hundreds of megabytes. Committing them violates Git file limits and slows operations. Large dataset releases should instead be retrieved from external storage or platforms like Kaggle.

---

## Verifying Ignored Files

Before committing any files, you can check if a file is ignored using the command:
```bash
git check-ignore -v path/to/file
```
If a file has already been accidentally tracked in the past, untrack it without deleting it from your local filesystem using:
```bash
git rm --cached path/to/file
```
