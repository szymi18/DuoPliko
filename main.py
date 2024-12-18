import os
import sys
from difflib import Differ

import PyPDF2
from PyQt6.QtGui import QIcon, QColor, QTextCharFormat
from PyQt6.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt6.QtCore import QTimer
from layout import Ui_Dialog
from layout2 import Ui_DuoPliko


class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("./DuoPlikoLogo.png"))
        self.show()

        self.ui.file1button.clicked.connect(self.browsefiles)
        self.ui.file2button.clicked.connect(self.browsefiles2)
        self.ui.submit.clicked.connect(self.filesCompare)
        self.ui.show.clicked.connect(self.openSecondDialog)


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
                    content.append(page.extract_text())
            return "\n".join(content)
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

    def filesCompare(self):
        if self.file1_path and self.file2_path:
            try:
                lines1 = self.read_file_content(self.file1_path).splitlines()
                lines2 = self.read_file_content(self.file2_path).splitlines()

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

    def openSecondDialog(self):
        if self.file1_path and self.file2_path:
            self.second_dialog = MyForm2(file1_path=self.file1_path, file2_path=self.file2_path, current_progress=self.ui.progressBar.value())
            self.second_dialog.exec()
        else:
            print("Najpierw wybierz oba pliki.")


class MyForm2(QDialog):
    def __init__(self, file1_path=None, file2_path=None, current_progress=0):
        super().__init__()
        self.ui = Ui_DuoPliko()
        self.ui.setupUi(self)
        self.ui.progressBar2.setValue(current_progress)
        self.setWindowIcon(QIcon("./DuoPlikoLogo.png"))

        self.file1_path = file1_path
        self.file2_path = file2_path

        self.ui.return_2.clicked.connect(self.close)
        self.ui.save.clicked.connect(self.save_changes)
        self.ui.file_compare_button.clicked.connect(self.compare_files_and_update)

        self.load_files_into_text_edits()
        self.show_differences()
        self.ui.save.clicked.connect(self.show_differences)


        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.updateProgressBar2)
        self.current_progress2 = 0
        self.target_progress2 = 0

        self.show()

    def load_files_into_text_edits(self):
        if self.file1_path:
            self.ui.textEdit1.setPlainText(self.read_file_content(self.file1_path))
            self.ui.label_2.setText(f"Plik 1: {os.path.basename(self.file1_path)}")
        if self.file2_path:
            self.ui.textEdit2.setPlainText(self.read_file_content(self.file2_path))
            self.ui.label.setText(f"Plik 2: {os.path.basename(self.file2_path)}")
        if self.is_pdf(self.file1_path) or self.is_pdf(self.file2_path):
            self.ui.user_info2.setText("Pliki .pdf nie mogą być edytowane.")

    def read_file_content(self, file_path):
        if file_path.endswith('.pdf'):
            content = []
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        content.append(page.extract_text())
                return "\n".join(content)
            except Exception as e:
                print(f"Błąd przy odczycie pliku PDF: {e}")
                return ""
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            except Exception as e:
                print(f"Błąd przy odczycie pliku TXT: {e}")
                return ""

    def is_pdf(self, file_path):
        if file_path and file_path.endswith('.pdf'):
            return True
        return False

    def save_changes(self):
        if self.file1_path:
            self.write_file_content(self.file1_path, self.ui.textEdit1.toPlainText())
        if self.file2_path:
            self.write_file_content(self.file2_path, self.ui.textEdit2.toPlainText())
        print("Zapisano zmiany w plikach.")

    def write_file_content(self, file_path, content):
        try:
            if file_path.endswith('.pdf'):
                print("Zapisywanie do PDF nieobsługiwane w tym przykładzie.")
            else:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
        except Exception as e:
            print(f"Błąd przy zapisie pliku {file_path}: {e}")

    def compare_files_and_update(self):
        if self.file1_path and self.file2_path:
            try:
                lines1 = self.read_file_content(self.file1_path).splitlines()
                lines2 = self.read_file_content(self.file2_path).splitlines()

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

                self.target_progress2 = int((matched_words / total_words) * 200) if total_words > 0 else 0
                print(f"Pliki są zgodne w {self.target_progress2}%")

                self.timer2.start(20)

            except Exception as e:
                print(f"Błąd przy porównywaniu plików: {e}")
        else:
            print("Proszę wybrać oba pliki.")

    def show_differences(self):
        text1 = self.read_file_content(self.file1_path).splitlines()
        text2 = self.read_file_content(self.file2_path).splitlines()

        differ = Differ()
        diff = list(differ.compare(text1, text2))

        self.ui.textEdit1.clear()
        self.ui.textEdit2.clear()

        for line in diff:
            if line.startswith('  '):
                self.add_formatted_text(self.ui.textEdit1, line[2:], QColor('black'))
                self.add_formatted_text(self.ui.textEdit2, line[2:], QColor('black'))
            elif line.startswith('- '):
                self.add_formatted_text(self.ui.textEdit1, line[2:], QColor('red'))
            elif line.startswith('+ '):
                self.add_formatted_text(self.ui.textEdit2, line[2:], QColor('green'))

    def add_formatted_text(self, text_edit, text, color):
        cursor = text_edit.textCursor()
        format = QTextCharFormat()
        format.setForeground(color)
        cursor.insertText(text + '\n', format)


    def updateProgressBar2(self):
        if self.current_progress2 < self.target_progress2:
            self.current_progress2 += 1
            self.ui.progressBar2.setValue(self.current_progress2)
        else:
            self.timer2.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())
