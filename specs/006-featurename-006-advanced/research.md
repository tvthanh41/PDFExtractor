# Phase 0: Research

## Technical Decisions

### Decision 1: Collapsible "Advanced Settings" in PySide6

**Decision**: Implement collapse/expand via a `QPushButton` toggle that shows/hides a `QGroupBox` containing the advanced fields.

**Rationale**: PySide6 has no native accordion/collapsible widget. Using `widget.setVisible(True/False)` driven by a toggle button is the idiomatic Qt approach. The dialog resizes automatically via `adjustSize()` after show/hide.

**Alternatives considered**:
- `QToolBox` / `QStackedWidget` — adds unnecessary tab overhead for a single section.
- Third-party collapse widget — adds a dependency.

---

### Decision 2: No new model fields required

**Decision**: All three fields (`offset_distance`, `match_index`, `page_index`) already exist in the domain models with correct defaults. No model changes are needed.

**Rationale**: The spec confirmed these are existing Pydantic fields with proper validators (`ge=0`). The only gap is the UI not exposing them and `_create_rule()` hardcoding `page_index=0`.

---

### Decision 3: Advanced section collapsed by default

**Decision**: The `QGroupBox` containing advanced controls starts hidden. A `QPushButton("▶ Advanced Settings")` toggles it and updates its label to `▼ Advanced Settings` when open.

**Rationale**: Users who don't need advanced settings shouldn't see extra complexity. The spec explicitly requires collapsed by default.

---

### Decision 4: Separate advanced sections per rule type

**Decision**: Each rule type (Anchor, BoundingBox) has its own advanced widget embedded in its respective stacked page, each with its own toggle button.

**Rationale**: Anchor and BoundingBox have completely different advanced fields. Sharing a single section would require complex conditional visibility logic.
