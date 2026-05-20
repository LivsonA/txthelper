import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QGroupBox,
    QListWidget,
    QStackedWidget,
    QLineEdit,
    QListWidgetItem, QDialog, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import pymorphy3
from pymystem3 import Mystem
from bs4 import BeautifulSoup
import requests
from PyQt6.QtWidgets import QMessageBox
import wikipedia
import webbrowser
from ZZZ import synonym, WordError
from text_recognition import text_recognitions

wikipedia.set_lang("ru")


class CounterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Счетчик")
        self.setMinimumSize(600, 450)
        self.setStyleSheet(self.light_style())
        self.flag = True
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)

        self.page_list = QListWidget()
        self.page_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.page_list.setMaximumWidth(160)
        self.page_list.setMinimumHeight(350)
        self.page_list.addItem("📊 Счётчик")
        self.page_list.addItem("Морфологический\nразбор")
        self.page_list.addItem("Морфемный\nразбор")
        self.page_list.currentRowChanged.connect(self.switch_page)
        self.stacked_widget = QStackedWidget()
        self.wikibt1 = QPushButton('WIKI', central_widget)
        self.wikibt1.move(9, 380)
        self.wikibt1.resize(156, 30)
        self.wikibt1.hide()
        self.wikibt1.clicked.connect(self.wiki)
        page_counter = self.create_counter_page()
        self.stacked_widget.addWidget(page_counter)

        page_extra = self.create_extra_page()
        self.stacked_widget.addWidget(page_extra)

        page_extra2 = self.create_extra_page2()
        self.stacked_widget.addWidget(page_extra2)

        self.theme_changerbt = QPushButton("Темная тема", parent=central_widget)
        self.theme_changerbt.clicked.connect(self.changer_theme)
        main_layout.addWidget(self.page_list, alignment=Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(self.stacked_widget, 1)
        self.theme_changerbt.move(9, 418)
        self.theme_changerbt.resize(156, 30)
        self.theme_changerbt.setStyleSheet(
            """QPushButton {
            background-color: #5a5a5a;
            color: white;
            border: 1px solid #444444;
            padding: 8px 16px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 13px;
            }
        """
        )

    def create_counter_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Введите текст для анализа...")
        self.text_input.setMaximumHeight(130)
        self.ee = QPushButton("Выбрать фото с текстом")
        self.ee.clicked.connect(self.ryttyr)
        layout.addWidget(self.text_input)
        layout.addWidget(self.ee)
        letters_group = QGroupBox("Анализ букв")
        letters_layout = QHBoxLayout()
        self.btn_letters = QPushButton("Анализировать кол-во букв")
        self.btn_letters.clicked.connect(self.count_letters)
        self.label_letters = QLabel("0 кол-во букв")
        self.label_letters.setAlignment(Qt.AlignmentFlag.AlignCenter)
        letters_layout.addWidget(self.btn_letters)
        letters_layout.addWidget(self.label_letters)
        letters_group.setLayout(letters_layout)
        layout.addWidget(letters_group)
        all_chars_group = QGroupBox("Анализ символов")
        all_chars_layout = QHBoxLayout()
        self.btn_all_chars = QPushButton("Анализировать все символы")
        self.btn_all_chars.clicked.connect(self.count_all_chars)
        self.label_all_chars = QLabel("0 кол-во символов")
        self.label_all_chars.setAlignment(Qt.AlignmentFlag.AlignCenter)
        all_chars_layout.addWidget(self.btn_all_chars)
        all_chars_layout.addWidget(self.label_all_chars)
        all_chars_group.setLayout(all_chars_layout)
        layout.addWidget(all_chars_group)
        words_group = QGroupBox("Анализ слов")
        words_layout = QHBoxLayout()
        self.btn_words = QPushButton("Анализировать кол-во слов")
        self.btn_words.clicked.connect(self.count_words)
        self.label_words = QLabel("0 кол-во слов")
        self.label_words.setAlignment(Qt.AlignmentFlag.AlignCenter)
        words_layout.addWidget(self.btn_words)
        words_layout.addWidget(self.label_words)
        words_group.setLayout(words_layout)
        layout.addWidget(words_group)
        layout.addStretch()
        return widget

    def create_extra_page(self):
        """Создаёт вторую страницу (другое окно)"""
        widget = QWidget()
        self.layout = QVBoxLayout(widget)

        self.info_label = QLineEdit()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.info_label)
        self.demo_button = QPushButton("Морфологический разбор")
        self.demo_button.clicked.connect(self.show_demo_message)


        self.layout.addWidget(self.demo_button, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addSpacing(100)
        return widget

    def create_extra_page2(self):
        widget = QWidget()
        self.layout3 = QVBoxLayout(widget)

        self.info_label2 = QLineEdit()
        self.info_label2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout3.addWidget(self.info_label2)
        self.demo_button2 = QPushButton("Морфемный разбор")
        self.demo_button2.clicked.connect(self.show_demo_message2)
        self.layout3.addWidget(self.demo_button2, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout3.addSpacing(100)
        return widget

    def show_demo_message(self):
        if hasattr(self, "unt") and self.unt is not None:
            self.layout.removeWidget(self.unt)
            self.unt.deleteLater()
            self.unt = None
        if hasattr(self, "unt2") and self.unt2 is not None:
            self.layout.removeWidget(self.unt2)
            self.unt2.deleteLater()
            self.unt2 = None

        analysis_result = self.analyze()
        try:

            self.unt = QLabel(f"{' '.join(analysis_result)}")
            self.layout.addWidget(self.unt, alignment=Qt.AlignmentFlag.AlignCenter)
        
            if self.parse.tag.POS == "NOUN":
                self.unt2 = QTextEdit("")
                self.unt2.setReadOnly(True)
                self.unt2.setText(
                    f"Именительный (кто? что?): {self.parse.inflect({'nomn'}).word}\nРодительный (кого? чего?): {self.parse.inflect({'gent'}).word}\nДательный (кому? чему?): {self.parse.inflect({'datv'}).word}\nВинительный (кого? что?): {self.parse.inflect({'accs'}).word}\nТворительный (кем? чем?): {self.parse.inflect({'ablt'}).word}\nПредложный (о ком? о чём?): {self.parse.inflect({'loct'}).word}"
                )

                self.layout.insertWidget(2, self.unt2)
                self.unt2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        except BaseException:
            QMessageBox.warning(self, "Ошибка", "введите слово")
    def show_demo_message2(self):
        if hasattr(self, "unt3") and self.unt3 is not None:
            self.layout3.removeWidget(self.unt3)
            self.unt3.deleteLater()
            self.unt3 = None
        if hasattr(self, "unt4") and self.unt4 is not None:
            self.layout3.removeWidget(self.unt4)
            self.unt4.deleteLater()
            self.unt4 = None
        if hasattr(self, "unt5") and self.unt5 is not None:
            self.layout3.removeWidget(self.unt5)
            self.unt5.deleteLater()
            self.unt5 = None
        try:
            analysis_result = self.parser()
            self.unt3 = QLabel(f"{''.join(analysis_result)}")
            self.unt3.setWordWrap(True)
            self.unt3.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )


            self.layout3.addWidget(self.unt3)
            parse = pymorphy3.MorphAnalyzer(lang="ru").parse(self.info_label2.text().strip())[0]
            if parse.tag.POS == "NOUN":
                self.unt4 = QTextEdit("")
                self.unt4.setReadOnly(True)
                self.unt4.setText(
                    f"Именительный (кто? что?): {parse.inflect({'nomn'}).word}\nРодительный (кого? чего?): {parse.inflect({'gent'}).word}\nДательный (кому? чему?): {parse.inflect({'datv'}).word}\nВинительный (кого? что?): {parse.inflect({'accs'}).word}\nТворительный (кем? чем?): {parse.inflect({'ablt'}).word}\nПредложный (о ком? о чём?): {parse.inflect({'loct'}).word}"
                )
                self.layout3.insertWidget(2, self.unt4)
                self.unt4.setAlignment(Qt.AlignmentFlag.AlignLeft)
            vyvich = synonym(self.info_label2.text().strip())
            self.unt5 = QTextEdit("")
            self.unt5.setReadOnly(True)
            self.unt5.setText(', '.join(vyvich))
            self.layout3.insertWidget(3, self.unt5, alignment=Qt.AlignmentFlag.AlignBottom)
            # self.unt5.setAlignment(Qt.AlignmentFlag.AlignBottom)
        except WordError as e:
            print(e)
        except ConnectionError:
            QMessageBox.warning(self, "Ошибка", "неустойчивое подключение")
        except BaseException as e:
            QMessageBox.warning(self, "Ошибка", "неправильный ввод")
            print(e)

    def analyze(self):
        morph = pymorphy3.MorphAnalyzer(lang="ru")
        if self.info_label.text().split() == []:
            pass
        else:
            self.parse = morph.parse(self.info_label.text().strip())[0]
            return self.parse.tag.cyr_repr, " Н.Ф " + self.parse.normal_form

    def parser(self):
        word = self.info_label2.text()
        firstlet = self.info_label2.text()[0].upper()

        Url = "https://morphemeonline.ru/{1}/{0}".format(word, firstlet)
        test = requests.get(Url)
        bs = BeautifulSoup(test.text, "html.parser")
        result = (
            bs.find(class_="fs-5 bg-light d-inline-block p-3")
            .get_text()
            .replace(":", "\n")
        )
        return result

    def ryttyr(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Выберите файл", "", "All Files (*);;Text Files (*.txt)")
        if file_path:
            self.text_input.setText(text_recognitions(file_path))
        else:
            pass
        # a = Dialog()
        # a.show()
        # result = a.exec()

        # if result == QDialog.DialogCode.Accepted:
        #     print("ee")

    def switch_page(self, index):
        if index == 0:
            self.wikibt1.hide()
        else:
            self.wikibt1.show()
        self.stacked_widget.setCurrentIndex(index)

    def get_text(self) -> str:
        return self.text_input.toPlainText()

    def count_letters(self):
        text = self.get_text()
        letter_count = sum(1 for ch in text if ch.isalpha())
        self.label_letters.setText(f"{letter_count} кол-во букв")

    def count_all_chars(self):
        text = self.get_text()
        total_chars = len(text)
        self.label_all_chars.setText(f"{total_chars} кол-во символов")

    def count_words(self):
        text = self.get_text()
        words = text.split()
        word_count = len(words)
        self.label_words.setText(f"{word_count} кол-во слов")

    def wiki(self, word, lang= 'ru'):
        if self.stacked_widget.currentIndex() == 1:
            rer = self.info_label.text()
        elif self.stacked_widget.currentIndex() == 2:
            rer = self.info_label2.text()
        Url = f"https://ru.wikipedia.org/wiki/{rer}"
        webbrowser.open(Url)

    def light_style(self):
        return """
                QMainWindow {
                    background-color: #f5f5f5;
                }
                QListWidget {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 14px;
                    padding: 5px;
                }
                QListWidget::item {
                    padding: 10px;
                    border-radius: 3px;
                }
                QListWidget::item:selected {
                    background-color: #4CAF50;
                    color: white;
                }
                QListWidget::item:hover {
                    background-color: #7CD782;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    margin-top: 12px;
                    font-size: 14px;
                    background-color: white;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QLineEdit {
                    background-color: white;
                    border: 1px solid #555;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 16px;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
                QLabel {
                    font-size: 15px;
                    background-color: #f0f0f0;
                    padding: 8px;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                    min-width: 150px;
                }
                QTextEdit {
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                    background-color: white;
                }
            """

    def dark_style(self):
        return """
    QMainWindow {
        background-color: #2b2b2b;
    }
    QListWidget {
        background-color: #3c3f41;
        border: 1px solid #555;
        border-radius: 5px;
        font-size: 14px;
        padding: 5px;
        color: #e0e0e0;
    }
    QListWidget::item {
        padding: 10px;
        border-radius: 3px;
    }
    QListWidget::item:selected {
        background-color: #A0A5A8;
        color: white;
    }
    QListWidget::item:hover {
        background-color: #4c4f51;
    }
    QGroupBox {
        font-weight: bold;
        border: 1px solid #555;
        border-radius: 8px;
        margin-top: 12px;
        font-size: 14px;
        background-color: #3c3f41;
        color: #e0e0e0;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }
    QPushButton {
        background-color: #5a5a5a;
        color: white;
        border: 1px solid #444444;
        padding: 8px 16px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px;
    }
    QLineEdit {
        border: 1px solid #555;
        border-radius: 5px;
        padding: 5px;
        font-size: 16px;
        background-color: #3c3f41;
        color: #e0e0e0;
    }
    QPushButton:hover {
        background-color: #6e6e6e;
    }
    QPushButton:pressed {
        background-color: #4a4a4a;
    }
    QLabel {
        font-size: 15px;
        background-color: #4a4a4a;
        padding: 8px;
        border-radius: 5px;
        border: 1px solid #555;
        min-width: 150px;
        color: #e0e0e0;
    }
    QTextEdit {
        border: 1px solid #555;
        border-radius: 5px;
        padding: 5px;
        font-size: 14px;
        background-color: #3c3f41;
        color: #e0e0e0;
    }
    """

    def changer_theme(self):
        self.flag = not self.flag
        if self.flag:
            self.theme_changerbt.setText("Темная тема")
            self.setStyleSheet(self.light_style())
            self.theme_changerbt.setStyleSheet(
                """
        background-color: #5a5a5a;
        color: white;
        border: 1px solid #444444;
        padding: 8px 16px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px;
        """
            )
        else:
            self.theme_changerbt.setText("Светлая тема")
            self.setStyleSheet(self.dark_style())
            self.theme_changerbt.setStyleSheet(
                """background-color: #C6EDFF;
                    color: black;
                    border: 1px solid #555;
                    padding: 8px 16px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 13px;
                    """
            )
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Диалоговое окно")
        self.setModal(True)
        self.setGeometry(200, 200, 300, 200)


def main():
    app = QApplication(sys.argv)
    window = CounterApp()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
