import difflib
import filecmp
import sys

import PyPDF2
from PyQt6.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt6.QtCore import QTimer
from layout import Ui_Dialog

class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()

        self.ui.file1button.clicked.connect(self.browsefiles)
        self.ui.file2button.clicked.connect(self.browsefiles2)
        self.ui.submit.clicked.connect(self.filesCompare)

        self.file1_path = None
        self.file2_path = None
        self.target_progress = 0
        self.current_progress = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgressBar)

    def browsefiles(self):
        file1, _ = QFileDialog.getOpenFileName(self, 'Open file')
        if file1:
            self.file1_path = file1
            print("Wybrano plik 1:", self.file1_path)

    def browsefiles2(self):
        file2, _ = QFileDialog.getOpenFileName(self, 'Open file')
        if file2:
            self.file2_path = file2
            print("Wybrano plik 2:", self.file2_path)

    def read_file_content(self, file_path):
        if file_path.endswith('.pdf'):
            content = []
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    content.extend(page.extract_text().splitlines())
            return content
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.readlines()

    def filesCompare(self):
        if self.file1_path and self.file2_path:
            try:
                lines1 = self.read_file_content(self.file1_path)
                lines2 = self.read_file_content(self.file2_path)

                words1 = [line.strip().split() for line in lines1]
                words2 = [line.strip().split() for line in lines2]

                if not words1 or not words2:
                    print("Jeden z plików jest pusty.")
                    return

                total_words = sum(len(line) for line in words1) + sum(len(line) for line in words2)
                matched_words = 0

                for line1, line2 in zip(words1, words2):
                    for word1, word2 in zip(line1, line2):
                        if word1 == word2:
                            matched_words += 1

                self.target_progress = int((matched_words / total_words) * 200) if total_words > 0 else 0
                self.current_progress = 0
                print(f"Pliki są zgodne w {self.target_progress}%")

                self.timer.start(20)

            except Exception as e:
                print(f"Błąd przy porównywaniu plików: {e}")
        else:
            print("Proszę wybrać oba pliki.")

    def updateProgressBar(self):
        if self.current_progress < self.target_progress:
            self.current_progress += 1
            self.ui.progressBar.setValue(self.current_progress)
        else:
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())
