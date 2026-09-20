<!-- 
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0 (MINOR: new principle added)
- Modified principles: None renamed
- Added sections: Principle IV. Versioned Changelog; Development Workflow updated with changelog rule
- Removed sections: None
- Follow-up TODOs: Create CHANGELOG.md in repo root (deferred — see Next Actions in update summary)
-->
# PDF Data Extractor Constitution

## Core Principles

### I. Desktop-First Architecture
The application is built primarily as a desktop application using PySide6. The UI MUST remain
responsive; heavy workloads (e.g. batch processing) MUST be offloaded to separate threads or
processes where necessary.

### II. Test-Driven Quality
All core business logic — including extraction strategies, models, and controllers — MUST have
accompanying unit and integration tests written in `pytest`. Test coverage for new features is
mandatory.

### III. Simple and Extensible Extraction Rules
Extraction rules are the core of the application. They MUST be modeled cleanly in Pydantic to
ensure predictable serialization and deserialization, allowing easy loading and saving of templates.

### IV. Versioned Changelog
The project MUST maintain a `CHANGELOG.md` file in the repository root that tracks every release
version and its associated changes. The format MUST follow [Keep a Changelog](https://keepachangelog.com/)
conventions (sections: Added, Changed, Deprecated, Removed, Fixed, Security).

- Every new feature, bug fix, or breaking change MUST be recorded in `CHANGELOG.md` under the
  appropriate `## [Unreleased]` section before the change is merged.
- When a version is released, the `## [Unreleased]` section MUST be promoted to a dated version
  heading (e.g., `## [1.1.0] - 2026-09-20`) and a new empty `## [Unreleased]` section MUST be
  added above it.
- Changelog entries MUST be human-readable and describe *what* changed and *why*, not just *how*.

## Additional Constraints

All data parsing logic MUST be decoupled from the UI layer to allow headless batch processing.
The UI layer MUST act exclusively as a visual editor and runner.

## Development Workflow

- Features MUST be developed with corresponding tests.
- Code MUST follow PEP-8 guidelines and be formatted correctly.
- New dependencies MUST be added to `requirements.txt`.
- Every user-visible change (feature, fix, or removal) MUST include a corresponding entry in
  `CHANGELOG.md` under `## [Unreleased]` before the work is considered complete.

## Governance

Changes to these core principles or architecture guidelines MUST be documented and approved via
updates to this constitution document. The version line below MUST be incremented according to
semantic versioning rules on every amendment.

**Version**: 1.1.0 | **Ratified**: 2026-09-19 | **Last Amended**: 2026-09-20
