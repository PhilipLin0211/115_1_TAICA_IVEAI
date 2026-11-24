---
name: project-workflow
description: Standardized software and research project workflow with Light (scripts/coursework) and Full (full-stack/research) modes, root AGENTS.md rules, single-source-of-truth docs, isolated testing, and unified A/B-class QA tracking in docs/ISSUES_AND_QA.md. Use when starting a new project, modifying, adding, fixing, or refactoring any project code, files, configs, or endpoints (every project change must be recorded in docs), setting up isolated tests, running a system audit, or preparing a release.
---

# project-workflow

A two-tier project development workflow built around a root `AGENTS.md`, Single Source of Truth (SSOT) documentation, isolated idempotent testing, and unified issue/audit tracking.

## When to Use

- Starting a new project, tool script, or research system and setting up its folder and doc structure.
- Making any modification to an existing project (adding features, fixing bugs, refactoring code, editing configs, or changing files/endpoints) so every change is recorded in docs.
- Setting up automated tests and manual QA verification checklists.
- Running a security, logic, or troubleshooting audit.
- Preparing a project for release or handoff.

## Mode Selection (Light vs. Full)

Choose the lightest mode that fits the project scope. Ask the user if unclear, or infer from the task.

- **Light Mode** (utility scripts, single-file tools, coursework, small prototypes):
  - Keep `AGENTS.md`, `README.md`, and `.gitignore` (plus `.env.example` if APIs or secrets are used).
  - Place setup, usage, verification commands, and a brief Changelog section directly in `README.md`.
- **Full Mode** (full-stack apps, multi-module research systems, multi-week deliverables):
  - Maintain `AGENTS.md` (root), `README.md`, `CHANGELOG.md`, `.gitignore`, `docs/DEVELOPMENT_PLAN.md`, `docs/TESTING_GUIDE.md`, and `docs/ISSUES_AND_QA.md`.
  - Upgrade from Light Mode to Full Mode whenever a project adds a database, multi-week milestones, or separate frontend/backend modules.

## Workflow Steps

### 1. Initialize and Specify

Establish structure and boundaries before writing feature code so AI collaborators and humans share one source of truth.

- Create clean lowercase module directories when using Full Mode (e.g., `frontend/`, `backend/`, `database/`, `docs/`, `scripts/`).
- Create `.gitignore` first, always excluding `.env`, virtual environments, `node_modules/`, local database files, and `*.local.md` confidential notes.
- Create root `AGENTS.md` defining:
  - Project purpose, architecture, and visual/coding standards.
  - Mandatory doc-sync rule: every project modification (code, config, file structure, or bug fix) MUST be recorded in project documentation before completing the task, using only verified code and test results.
- Create `README.md` as the single entry point (overview, prerequisites, setup, start/stop commands, directory tree, and links to `docs/`).
- In Full Mode, create `docs/DEVELOPMENT_PLAN.md` covering business rules, database schema, milestone roadmap, and a Post-V1 Backlog to prevent scope creep.

### 2. Build and Record Every Change

Every modification to the project (new features, bug fixes, refactors, config edits, or file moves) must be recorded in documentation before finishing the turn so docs never drift from the codebase.

- Implement features milestone by milestone according to `docs/DEVELOPMENT_PLAN.md` (or `README.md` in Light Mode).
- After any project change:
  - **Full Mode**: Prepend a dated entry (`YYYY-MM-DD`) under the current week in `CHANGELOG.md` summarizing what changed and linking modified files. Update `README.md` if directory tree, dependencies, or run commands changed; update `docs/TESTING_GUIDE.md` if tests or QA steps changed; update `docs/ISSUES_AND_QA.md` if a bug, RCA, or audit item was discovered or resolved.
  - **Light Mode**: Update `README.md` (structure, usage, or its Changelog section) to reflect the modification.
- Enforce SSOT boundaries: never copy daily logs into `DEVELOPMENT_PLAN.md` or duplicate installation steps into `TESTING_GUIDE.md`. Cross-link instead.

### 3. Isolate and Verify

Ensure tests are repeatable and cannot corrupt development databases or trigger real external side effects.

- Configure test isolation before running integration tests (e.g., a `conftest.py` that routes `DATABASE_URL` to a temporary DB and clears live SMTP/API keys).
- Write idempotent tests (clean fixtures or unique dynamic IDs) so repeated runs pass consistently.
- Record runnable CLI verification commands (e.g., `pytest`, `npm run build`) and browser/E2E manual QA checkpoints in `docs/TESTING_GUIDE.md` (Full Mode) or `README.md` (Light Mode).

### 4. Audit and Log Issues

Track all bugs, architectural risks, troubleshooting notes, and test gaps in `docs/ISSUES_AND_QA.md` (Full Mode) to avoid cross-file duplication.

- Tag every entry by category and status (`Pending`, `In Progress`, `Resolved`, `Kept Intentionally`):
  - `[Class A - Dev Convenience]`: Intentional shortcuts kept for testing or development (e.g., magic links, dev reset tokens, permissive CORS) that must be reviewed before release.
  - `[Class B - Bug/Security]`: Unintended defects, IDOR, XSS/injection, or state-sync bugs to fix directly.
  - `[RCA - Troubleshooting]`: Reproducible errors, root causes, solutions, and prevention rules.
  - `[TEST-GAP]`: Unverified edge cases or manual E2E checks still pending.
- Keep sensitive details (admin backdoors, password rotation rules, credentials) out of `docs/ISSUES_AND_QA.md` and `README.md`. Record them only in a `.gitignore`-protected `docs/*.local.md` file.

### 5. Converge and Release

Clean up development shortcuts and verify the full system before delivery.

- Review every open `[Class A - Dev Convenience]` item in `docs/ISSUES_AND_QA.md`: remove, disable, or gate it behind production environment checks (`APP_ENV=production`).
- Audit `.env.example` to confirm no real secrets or misleading relative DB paths are exposed.
- Run the full automated test suite and production build, then update `CHANGELOG.md` and `README.md` to reflect the release state.

## Gotchas

- Never finish a code, config, or file modification without recording it in `CHANGELOG.md` (Full Mode) or `README.md` (Light Mode).
- Never mark a milestone, test count, or issue as resolved without running the verification command and checking actual output.
- Never duplicate the same checklist or issue details across `README.md`, `DEVELOPMENT_PLAN.md`, `TESTING_GUIDE.md`, and `ISSUES_AND_QA.md`.
- Always check `.gitignore` before creating any `*.local.md` or `.env` file.
