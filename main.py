from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QToolBar, QWidget, \
    QTextBrowser


class PdfWorker(QThread):
    # Signal to send pdf text to GUI thread
    send_pdf_text = pyqtSignal(str)

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path

    def run(self):
        import fitz  # PyMuPDF
        doc = fitz.open(self.path)
        content = ""
        for i in range(len(doc)):
            page = doc.load_page(i)
            content += page.get_text("html") + "\n"
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
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #18181b;
                color: #e4e4e7;
                
            }
                            
            QToolButton {
                border: none;
                padding: 1px;
                border-radius: 6px;
            }
            
            QToolButton:hover {
                background-color: #3b82f6;
            }
            
            QToolButton:pressed {
                background-color: #292524;
            }
            
            QToolButton:checked {
                background-color: #444444;
            }
        """)
        self.addToolBar(toolbar)

        open_pdf_action = QAction('File', self)
        open_pdf_action.triggered.connect(self.open_pdf)
        toolbar.addAction(open_pdf_action)

        # self.text_edit = QTextEdit()
        self.text_edit = QTextBrowser()
        self.text_edit.setOpenExternalLinks(True)
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
            palette = self.text_edit.palette()
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#3b82f6"))
            self.text_edit.setPalette(palette)

            self.pdf_worker = PdfWorker(path)
            self.pdf_worker.send_pdf_text.connect(self.update_text)
            self.pdf_worker.finished.connect(self.pdf_worker.deleteLater)
            self.pdf_worker.start()

    def update_text(self, text):
        # self.text_edit.setPlainText(text)
        self.text_edit.setHtml(text)
        self.text_edit.setPlaceholderText("")


app = QApplication([])
window = PDFReader()
window.show()
app.exec()
