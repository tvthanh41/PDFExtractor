"""
Unit tests for PdfCanvasWidget multi-page navigation.
Tests page state transitions, boundary clamping, and signal emission.
"""
import pytest


class TestPdfCanvasMultiPage:
    """Pure logic tests for canvas page navigation (no actual PDF rendering needed)."""

    def test_initial_state(self, qtbot):
        from src.ui.pdf_canvas import PdfCanvasWidget
        canvas = PdfCanvasWidget()
        qtbot.addWidget(canvas)
        assert canvas.current_page == 0
        assert canvas.total_pages == 0

    def test_set_page_updates_current_page(self, qtbot, tmp_path):
        """After load_document, set_page should update current_page correctly."""
        import pymupdf as fitz
        from src.ui.pdf_canvas import PdfCanvasWidget

        # Create a 3-page dummy PDF
        pdf_path = tmp_path / "test.pdf"
        doc = fitz.open()
        for _ in range(3):
            doc.new_page()
        doc.save(str(pdf_path))
        doc.close()

        canvas = PdfCanvasWidget()
        qtbot.addWidget(canvas)
        canvas.load_document(str(pdf_path))

        assert canvas.total_pages == 3
        assert canvas.current_page == 0

        canvas.set_page(1)
        assert canvas.current_page == 1

        canvas.set_page(2)
        assert canvas.current_page == 2

    def test_next_page(self, qtbot, tmp_path):
        import pymupdf as fitz
        from src.ui.pdf_canvas import PdfCanvasWidget

        pdf_path = tmp_path / "test.pdf"
        doc = fitz.open()
        for _ in range(3):
            doc.new_page()
        doc.save(str(pdf_path))
        doc.close()

        canvas = PdfCanvasWidget()
        qtbot.addWidget(canvas)
        canvas.load_document(str(pdf_path))

        canvas.next_page()
        assert canvas.current_page == 1
        canvas.next_page()
        assert canvas.current_page == 2

    def test_next_page_clamped_at_last_page(self, qtbot, tmp_path):
        import pymupdf as fitz
        from src.ui.pdf_canvas import PdfCanvasWidget

        pdf_path = tmp_path / "test.pdf"
        doc = fitz.open()
        for _ in range(2):
            doc.new_page()
        doc.save(str(pdf_path))
        doc.close()

        canvas = PdfCanvasWidget()
        qtbot.addWidget(canvas)
        canvas.load_document(str(pdf_path))

        canvas.next_page()
        assert canvas.current_page == 1
        canvas.next_page()  # Should not go beyond page 1 (0-indexed last page for 2-page doc)
        assert canvas.current_page == 1

    def test_prev_page(self, qtbot, tmp_path):
        import pymupdf as fitz
        from src.ui.pdf_canvas import PdfCanvasWidget

        pdf_path = tmp_path / "test.pdf"
        doc = fitz.open()
        for _ in range(3):
            doc.new_page()
        doc.save(str(pdf_path))
        doc.close()

        canvas = PdfCanvasWidget()
        qtbot.addWidget(canvas)
        canvas.load_document(str(pdf_path))
        canvas.set_page(2)

        canvas.prev_page()
        assert canvas.current_page == 1
        canvas.prev_page()
        assert canvas.current_page == 0

    def test_prev_page_clamped_at_zero(self, qtbot, tmp_path):
        import pymupdf as fitz
        from src.ui.pdf_canvas import PdfCanvasWidget

        pdf_path = tmp_path / "test.pdf"
        doc = fitz.open()
        for _ in range(2):
            doc.new_page()
        doc.save(str(pdf_path))
        doc.close()

        canvas = PdfCanvasWidget()
        qtbot.addWidget(canvas)
        canvas.load_document(str(pdf_path))

        canvas.prev_page()  # Already on page 0, should stay
        assert canvas.current_page == 0

    def test_set_page_out_of_range_clamped(self, qtbot, tmp_path):
        import pymupdf as fitz
        from src.ui.pdf_canvas import PdfCanvasWidget

        pdf_path = tmp_path / "test.pdf"
        doc = fitz.open()
        for _ in range(3):
            doc.new_page()
        doc.save(str(pdf_path))
        doc.close()

        canvas = PdfCanvasWidget()
        qtbot.addWidget(canvas)
        canvas.load_document(str(pdf_path))

        canvas.set_page(100)  # Way beyond last page
        assert canvas.current_page == 2  # Clamped to last page

        canvas.set_page(-5)  # Negative
        assert canvas.current_page == 0  # Clamped to first page

    def test_page_changed_signal_emitted(self, qtbot, tmp_path):
        import pymupdf as fitz
        from src.ui.pdf_canvas import PdfCanvasWidget

        pdf_path = tmp_path / "test.pdf"
        doc = fitz.open()
        for _ in range(3):
            doc.new_page()
        doc.save(str(pdf_path))
        doc.close()

        canvas = PdfCanvasWidget()
        qtbot.addWidget(canvas)
        canvas.load_document(str(pdf_path))

        received = []
        canvas.page_changed.connect(lambda cur, total: received.append((cur, total)))

        canvas.set_page(1)
        assert len(received) == 1
        assert received[0] == (1, 3)
