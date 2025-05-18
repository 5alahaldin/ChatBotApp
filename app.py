import sys
from PyQt5.QtWidgets import (
  QApplication, QWidget, QVBoxLayout, QHBoxLayout,
  QTextBrowser, QLineEdit, QLabel, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor

# --- LangChain & Ollama Setup ---
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

if len(sys.argv) > 1:
  model_name = sys.argv[1]
else:
  model_name = "prakasharyan/qwen-arabic"

template = """
أنت مساعد ذكي يتحدث اللغة العربية فقط. مهمتك هي الرد على الأسئلة بدقة ووضوح، باستخدام اللغة العربية الفصحى، بناءً على سياق المحادثة السابق.

السياق السابق للمحادثة:
{context}

السؤال الحالي:
{question}

الجواب:
"""

prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model=model_name)
chain = prompt | model


class ChatbotWorker(QThread):
  response_ready = pyqtSignal(str)

  def __init__(self, context, question):
    super().__init__()
    self.context = context
    self.question = question

  def run(self):
    try:
      result = chain.invoke({"context": self.context, "question": self.question})
      self.response_ready.emit(result)
    except Exception:
      self.response_ready.emit("حدث خطأ أثناء توليد الرد.")


class ChatWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Lyla")
    self.setFixedSize(1350, 900)
    self.setLayoutDirection(Qt.RightToLeft)
    self.context = ""
    self.init_ui()

  def set_background(self, path):
    bg = QLabel(self)
    bg.setPixmap(QPixmap(path).scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding))
    bg.resize(self.size())
    bg.lower()

  def init_ui(self):
    self.set_background("ui/backgrownd_1350x900.png")

    layout = QVBoxLayout()
    layout.setContentsMargins(90, 150, 700, 70)

    self.chat_display = QTextBrowser(self)
    self.chat_display.setStyleSheet("""
      QTextBrowser {
        background: transparent;
        border: none;
        padding: 10px;
        font-size: 24px;
        font-family: 'Amiri', serif;
        color: #4B2E2E;
      }
      QTextBrowser::verticalScrollBar { width: 0px; }
      QTextBrowser::horizontalScrollBar { height: 0px; }
    """)
    self.chat_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 
    self.chat_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
    layout.addWidget(self.chat_display)

    input_layout = QHBoxLayout()

    self.user_input = QLineEdit(self)
    self.user_input.setPlaceholderText("اكتب رسالتك هنا...")
    self.user_input.setAlignment(Qt.AlignRight)
    self.user_input.setLayoutDirection(Qt.RightToLeft)
    self.user_input.setStyleSheet("""
      QLineEdit {
        background: rgba(255, 223, 186, 100);
        border: 4px solid #4C312A;
        border-radius: 10px;
        padding: 15px;
        font-size: 18px;
        font-family: 'Amiri', serif;
        color: #4B2E2E;
      }
      QLineEdit::placeholder {
        color: rgba(76, 49, 42, 150);
      }
    """)
    shadow = QGraphicsDropShadowEffect(self)
    shadow.setBlurRadius(10)
    shadow.setOffset(2, 2)
    shadow.setColor(QColor(0, 0, 0, 120))
    self.user_input.setGraphicsEffect(shadow)
    self.user_input.returnPressed.connect(self.handle_user_input)
    self.user_input.textChanged.connect(self.adjust_text_alignment)
    input_layout.addWidget(self.user_input)

    layout.addLayout(input_layout)
    self.setLayout(layout)

  def adjust_text_alignment(self):
    text = self.user_input.text()
    if text and text[0].isascii():
      self.user_input.setAlignment(Qt.AlignLeft)
      self.user_input.setLayoutDirection(Qt.LeftToRight)
    else:
      self.user_input.setAlignment(Qt.AlignRight)
      self.user_input.setLayoutDirection(Qt.RightToLeft)

  def handle_user_input(self):
    user_message = self.user_input.text().strip()
    if not user_message:
      return

    self.chat_display.append(f"<p style='color:#4B2E2E'><b>أنت:</b> {user_message}</p>")
    self.user_input.clear()

    self.worker = ChatbotWorker(self.context, user_message)
    self.worker.response_ready.connect(self.display_bot_response)
    self.worker.start()

  def display_bot_response(self, bot_response):
    self.context += f"أنت: {self.user_input.text()}\nليلي: {bot_response}\n"
    self.bot_response = bot_response
    self.typing_text = ""
    self.current_char_index = 0
    self.typing_timer = QTimer(self)
    self.typing_timer.timeout.connect(self.type_next_character)
    self.typing_timer.start(30)

  def type_next_character(self):
    if self.current_char_index < len(self.bot_response):
      self.typing_text += self.bot_response[self.current_char_index]
      self.current_char_index += 1
    else:
      self.typing_timer.stop()
      self.chat_display.append(
        f"<p style='color:#6F4E37; font-weight:bold'><b>ليلي:</b> {self.typing_text}</p>"
      )


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = ChatWindow()
  window.show()
  sys.exit(app.exec_())
