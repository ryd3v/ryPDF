import pdfplumber
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog


class PDFReader(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('ryPDF')
        self.setGeometry(100, 100, 600, 900)
        self.setStyleSheet("background-color: #09090b;")
        app.setStyle("Fusion")

        self.text_edit = QTextEdit()
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_edit.setReadOnly(True)
        text_font = QFont("Roboto", 12)
        self.text_edit.setFont(text_font)

        self.button = QPushButton('Open PDF')
        self.button.clicked.connect(self.open_pdf)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def open_pdf(self):
        # Get file using file dialog
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF files (*.pdf)")

        if path:
            # Use PDFPlumber to load and read PDF
            with pdfplumber.open(path) as pdf:
                content = ""

                # Iterate through pdf pages
                for page in pdf.pages:
                    # Extract text
                    page_text = page.extract_text()
                    content += page_text if page_text else ""

                # Set the text in the QTextEdit widget
                self.text_edit.setText(content)


app = QApplication([])
window = PDFReader()
window.show()
app.exec()
