# Data Model

No changes to the domain layer are required. All fields already exist:

## `AnchorExtractionRule` (existing fields exposed)

| Field | Type | Default | Constraint | UI Control |
|-------|------|---------|------------|------------|
| `offset_distance` | `float` | `150.0` | `ge=0` | `QDoubleSpinBox` (min=0, max=9999, step=10) |
| `match_index` | `int` | `0` | `ge=0` | `QSpinBox` (min=0, max=99) |

## `BoundingBoxExtractionRule` (existing field exposed)

| Field | Type | Default | Constraint | UI Control |
|-------|------|---------|------------|------------|
| `page_index` | `int` | `0` | `ge=0` | `QSpinBox` (min=0, max=999) |

## UI Contract: `RuleDialog` changes

The existing `RuleDialog` (`src/ui/rule_dialog.py`) is modified in-place:

```
RuleDialog
├── [common form] key_name, data_type, rule_type
├── stacked_widget
│   ├── anchor_widget
│   │   ├── [basic] anchor_text, search_mode, direction
│   │   └── [toggle btn] ▶ Advanced Settings
│   │       └── [advanced group, hidden by default]
│   │           ├── Offset Distance: QDoubleSpinBox
│   │           └── Match Index: QSpinBox
│   └── box_widget
│       ├── [info label] Bounding Box defined...
│       └── [toggle btn] ▶ Advanced Settings
│           └── [advanced group, hidden by default]
│               └── Page Index: QSpinBox
└── [Save / Cancel buttons]
```
