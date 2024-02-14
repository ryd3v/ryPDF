import pdfplumber
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QFileDialog, QToolBar, QWidget


class PdfWorker(QThread):
    # Signal to send pdf text to GUI thread
    send_pdf_text = pyqtSignal(str)

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path

    def run(self):
        with pdfplumber.open(self.path) as pdf:
            content = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    content += page_text + "\n"
            self.send_pdf_text.emit(content)


class PDFReader(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PDF Reader')
        self.setGeometry(100, 100, 700, 900)
        self.setStyleSheet("background-color: #18181b;")

        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)

        open_pdf_action = QAction('File', self)
        open_pdf_action.triggered.connect(self.open_pdf)
        toolbar.addAction(open_pdf_action)

        self.text_edit = QTextEdit()
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_edit.setReadOnly(True)
        text_font = QFont("Roboto", 12)
        self.text_edit.setFont(text_font)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "File", "", "PDF Files (*.pdf)")

        if path:
            self.text_edit.setPlaceholderText("Loading...")

            self.pdf_worker = PdfWorker(path)
            self.pdf_worker.send_pdf_text.connect(self.update_text)
            self.pdf_worker.finished.connect(self.pdf_worker.deleteLater)
            self.pdf_worker.start()

    def update_text(self, text):
        self.text_edit.setPlainText(text)
        self.text_edit.setPlaceholderText("")


app = QApplication([])
window = PDFReader()
window.show()
app.exec()
