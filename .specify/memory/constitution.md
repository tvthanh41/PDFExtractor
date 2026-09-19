<!-- 
Sync Impact Report:
- Version change: None -> 1.0.0 (initial setup)
- Modified principles: Initialized defaults
- Added sections: Core Principles, Additional Constraints, Development Workflow, Governance
- Removed sections: N/A
- Follow-up TODOs: None
-->
# PDF Data Extractor Constitution

## Core Principles

### I. Desktop-First Architecture
The application is built primarily as a desktop application using PySide6. The UI should remain responsive, ensuring heavy workloads (like batch processing) are offloaded to separate threads or processes where necessary.

### II. Test-Driven Quality
All core business logic, including extraction strategies, models, and controllers, MUST have accompanying unit and integration tests written in `pytest`. Test coverage for new features is mandatory.

### III. Simple and Extensible Extraction Rules
Extraction rules are the core of the application. They MUST be modeled cleanly in Pydantic to ensure predictable serialization and deserialization, allowing easy loading/saving of templates.

## Additional Constraints

All data parsing logic MUST be decoupled from the UI layer to allow headless batch processing. The UI layer should act exclusively as a visual editor and runner.

## Development Workflow

- Features MUST be developed with corresponding tests.
- Code should follow PEP-8 guidelines and be formatted correctly.
- New dependencies MUST be added to `requirements.txt`.

## Governance

Changes to these core principles or architecture guidelines MUST be documented and approved via updates to this constitution document.

**Version**: 1.0.0 | **Ratified**: 2026-09-19 | **Last Amended**: 2026-09-19
