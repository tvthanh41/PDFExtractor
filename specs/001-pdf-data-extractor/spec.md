# Feature Specification: PDF Data Extractor

**Feature Branch**: `001-pdf-data-extractor`

**Created**: 2026-09-18

**Status**: Draft

**Input**: User description: "Tôi cần build 1 ứng dụng cho phép lấy dữ liệu từ file PDF. Ứng dụng này sẽ cho phép user khởi tạo 1 template để lấy thông tin từ các file pdf có chung 1 form (ví dụ biểu phí ngân hàng, biểu phí thuế...). Trong template này, user sẽ cho biết vị trí giá trị cần lấy ở vị trí nào hoặc nó sẽ chứa giá trị như thế nào để tìm kiếm. Ví dụ user có thể yêu cầu tìm kiếm dòng "Tổng giá trị hoá đơn" và yêu cầu lấy giá trị gần đó, ở đây ứng dụng sẽ cần cho phép user nhập vào kiểu dữ liệu mà họ mong muốn đồng thời lưu giá trị tìm được dưới dạng key như thế nào. Phương án thứ 2 mà user có thể làm là phần giao diện của ứng dụng cho phép chọn 1 vùng ở trong file, sau đó lấy tất cả các giá trị cần dùng trong vùng mà user đã chỉ định (bounding box). Về output, hiện tại ta có thể lưu dưới dạng file csv, với phần mỗi column tương ứng với tên key mà user đã define trong template. Sau khi user đã define template thì user có thể chọn template và thư mục chứa file pdf để trích xuất thông tin. Thư mục có thể chứa nhiều loại file khác nhau tuy nhiên ứng dụng phải tự lọc ra file pdf và chạy cho các file này, với mỗi file thì output sẽ thành 1 dòng trong file csv. Phần giao diện cần cho phép người dùng mở nhiều template dưới dạng tab và template cần lưu dưới 1 định dạng file phù hợp để user có thể dùng lại lần sau. Ứng dụng có thể sẽ phải chạy với 1 số lượng file rất lớn, do đó nó cần được cài đặt để xử lý nhiều file song song."

## Clarifications

### Session 2026-09-18

- Q: Should the batch directory scanner recursively process PDF files in subdirectories or only scan top-level files? → A: Option B - Recursive scanning (automatically include `.pdf` files in all nested subdirectories).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Template Creation & Value Extraction Rules (Priority: P1)

As a user processing formatted PDF documents (e.g., bank statements, tax invoices), I want to open a sample PDF document and visually define data extraction rules—using either anchor-text search or bounding-box region selection—and save this template configuration to a file so that I can reuse it for structured data extraction.

**Why this priority**: Creating and defining templates with key mapping is the foundational core of the application. Without template definition capabilities, batch processing cannot function.

**Independent Test**: Can be fully tested by opening a sample PDF file in the application UI, creating an anchor rule (e.g. search "Tổng giá trị hoá đơn", data type Number, key "total_amount") and a bounding box rule (key "vendor_name"), testing the extraction on the sample file, and saving the template to a template file.

**Acceptance Scenarios**:

1. **Given** a loaded sample PDF in the template editor, **When** the user defines an anchor rule searching for text "Tổng giá trị hoá đơn", sets location direction to "Right", data type to "Currency/Number", and key name to "total_amount", **Then** the application highlights the detected value on the preview canvas and associates it with key "total_amount".
2. **Given** a loaded sample PDF in the template editor, **When** the user drags a rectangular bounding box over a region of the document and enters key name "invoice_notes", **Then** the application extracts text within that bounding box region and assigns it to key "invoice_notes".
3. **Given** a defined template with extraction rules, **When** the user clicks "Save Template", **Then** the application prompts for a file location and saves the template in a reusable structured file format.

---

### User Story 2 - Parallel Batch Processing & CSV Export (Priority: P2)

As a data operator, I want to select a saved template and a target folder containing a large number of files, have the application automatically identify and process all PDF files in parallel, and export the aggregated results into a single CSV file with columns matching template keys.

**Why this priority**: Batch execution turns template definitions into actionable automated data extraction, delivering high business value for bulk processing.

**Independent Test**: Can be independently tested by selecting a saved template and a folder containing mixed file types (PDFs, images, TXT files), initiating batch extraction, verifying that non-PDF files are ignored, and checking that the resulting CSV file contains one header row matching key names and one data row per PDF file.

**Acceptance Scenarios**:

1. **Given** a folder containing 500 PDF files and 50 non-PDF files (e.g. PNG, DOCX) across top-level and subdirectories, **When** the user selects a template and triggers batch extraction on the folder, **Then** the system filters out non-PDF files and recursively processes all 500 PDF files found across all subdirectories.
2. **Given** batch extraction running on a multi-core system, **When** processing a large batch of PDF files, **Then** the system distributes work across multiple parallel threads/workers and displays a live progress counter (e.g., "120/500 files completed").
3. **Given** completed batch processing, **When** the user opens the output CSV file, **Then** the first row contains column headers matching template keys, followed by 500 data rows containing extracted values corresponding to each processed PDF file.

---

### User Story 3 - Multi-Tab Template Management & Workspace (Priority: P3)

As a power user working with multiple document formats, I want to open multiple template files simultaneously in a tabbed user interface, switch between them, and edit or preview rules across different document types without closing my current work.

**Why this priority**: Improves user experience and efficiency when managing multiple invoice/statement forms, allowing seamless switching and editing.

**Independent Test**: Can be tested by opening three different template files in the application, observing three distinct workspace tabs, editing rules in Tab 1, switching to Tab 2 to preview extractions, and verifying each tab maintains its isolated state.

**Acceptance Scenarios**:

1. **Given** the application running, **When** the user opens multiple existing template files, **Then** each template loads into its own tab with independent rule lists and preview state.
2. **Given** multiple open template tabs, **When** the user edits a rule in Tab 1 and switches to Tab 2, **Then** Tab 1 retains its unsaved changes indicator and Tab 2 displays its own active configuration.

---

### Edge Cases

- What happens when a PDF file in the target directory is corrupt, encrypted, or password-protected? The system logs a processing warning/error for that specific file, writes empty/error indicator cells for its CSV row, and continues processing all remaining files in the batch without crashing.
- What happens when anchor text defined in a template is not found in a particular PDF file? The extracted value for that key defaults to blank (empty string) in the CSV row, and a minor warning is logged for review.
- What happens when anchor text appears multiple times on the same page? The rule allows specifying match occurrence (e.g., first occurrence, last occurrence, or nearest to top-left).
- What happens when a bounding box region falls outside the page dimensions of a specific PDF file (e.g., page 2 doesn't exist or page orientation differs)? The system clips the bounding box coordinates to valid page boundaries or returns empty text if the page is missing.
- What happens when the selected directory contains subdirectories? The system recursively scans and processes all `.pdf` files within all subdirectories of the selected target folder.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a document canvas UI to open and preview sample PDF files for template creation.
- **FR-002**: System MUST allow users to define Anchor Search extraction rules by specifying: target search string (e.g., "Tổng giá trị hoá đơn"), search matching mode (exact, case-insensitive, contains), relative target value offset/position (Right, Below, Left, Above, or Offset distance), target data type (String, Number, Date, Currency), and target output Key name.
- **FR-003**: System MUST allow users to define Bounding Box extraction rules by visually selecting a rectangular area on a sample PDF page and assigning a target output Key name.
- **FR-004**: System MUST store template definitions in a structured, human-readable file format (e.g., JSON schema `.pdftpl`) containing all rule configurations, key names, data types, and target coordinates/anchors.
- **FR-005**: System MUST feature a multi-tab interface allowing users to open, edit, preview, and save multiple templates simultaneously in separate tabs.
- **FR-006**: System MUST allow users to select an existing template file and a target folder for bulk data extraction.
- **FR-007**: System MUST automatically scan the selected input directory recursively and filter for `.pdf` files in all subdirectories, ignoring all non-PDF files and non-compatible file formats.
- **FR-008**: System MUST implement parallel/concurrent processing to extract data from multiple PDF files simultaneously using multi-threading or worker processes.
- **FR-009**: System MUST generate an output CSV file containing a header row matching all defined template Key names, with each processed PDF contributing exactly one row of extracted values.
- **FR-010**: System MUST format extracted values according to their defined data type (e.g., cleaning currency symbols/spaces for Number types, standardizing YYYY-MM-DD for Date types).
- **FR-011**: System MUST maintain execution logs during batch processing, highlighting any unreadable files or missing keys without stopping the overall batch run.

### Key Entities

- **Template**: Represents a saved extraction configuration containing template name, description, target page layout details, and a list of Extraction Rules.
- **Extraction Rule**: Defines how a specific key value is located and parsed. Contains Rule Type (Anchor Search vs Bounding Box), Output Key Name, Data Type, and Type-Specific Parameters:
  - *Anchor Parameters*: Anchor Text, Search Mode, Relative Position (Direction & Distance Offset), Match Index.
  - *Bounding Box Parameters*: Page Index, Bounding Box Coordinates (normalized X, Y, Width, Height relative to page dimensions).
- **Batch Processing Job**: Represents an active or completed extraction run with parameters: Selected Template, Input Directory Path, Output CSV Path, Total File Count, Processed File Count, Error Count, Execution Status, and Progress Logs.
- **CSV Data Record**: A single row of key-value data corresponding to one processed PDF file, mapped strictly to the column keys defined in the template.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Parallel batch processing extracts data from 100 single-page PDF files in under 15 seconds on standard multi-core desktop systems.
- **SC-002**: 100% of non-PDF files in input directories are filtered out safely without causing application errors or execution halts.
- **SC-003**: Extraction achieves 99%+ field accuracy for text-based PDF documents matching the template structure.
- **SC-004**: Users can create a new 5-key template from a sample PDF document in under 3 minutes.
- **SC-005**: The user interface remains responsive (UI updates at >= 30 FPS) while multi-threaded batch processing executes in the background.

## Assumptions

- **PDF Document Type**: Target PDF documents contain selectable digital text layers. Scanned image-only PDFs requiring OCR are assumed out-of-scope for v1, but the template structure is designed to support OCR extensions in future releases.
- **Normalized Coordinates**: Bounding box coordinates are stored normalized as percentages of page width and height, enabling consistent extraction even if PDF documents have slightly varying render DPI or zoom levels.
- **Output Formatting**: CSV files are exported in UTF-8 encoding with standard comma delimiter, properly escaping string fields containing commas or line breaks.
- **Directory Scope**: Directory scanning recursively searches subdirectories for all files with extension `.pdf` (case-insensitive).
