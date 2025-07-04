import sys
import pandas as pd
from fuzzywuzzy import process
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import speech_recognition as sr
from googletrans import Translator

class TamilTranslator:
    def __init__(self):
        self.translator = Translator()
        self.dataset = pd.read_csv("D:\CIP Project\questionsv4.csv")
        #self.dataset['questions'] = self.dataset['Tamil_Query'].apply(self.translate_tamil_to_english)

    def translate_tamil_to_english(self, tamil_text):
        return self.translator.translate(tamil_text, src='ta', dest='en').text
    
    def translate_english_to_tamil(self, english_text):
        return self.translator.translate(english_text, src='en', dest='ta').text

    def search_response(self, query):
        questions = self.translate_tamil_to_english(query)
        match, score, temp = process.extractOne(questions, self.dataset['questions'])
        
        # Use the matched query to retrieve the response
        if match:
            response = self.dataset.loc[self.dataset['questions'] == match, 'answers'].values[0]
            tamil_response = self.translate_english_to_tamil(response)
            return tamil_response
        return "Sorry, I couldn't find a relevant response."
    
class VoiceChatbotUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tamil Voice Chatbot")
        self.setFixedSize(600, 400)

        self.translator = TamilTranslator()

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create UI elements
        self.label = QLabel("Speak something in Tamil:")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.output_label = QLabel("")
        self.output_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.output_label)

        self.start_button = QPushButton("Start Listening")
        self.start_button.clicked.connect(self.start_listening)
        layout.addWidget(self.start_button)

    def start_listening(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak something in Tamil...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=50)

        try:
            text = recognizer.recognize_google(audio, language='ta-IN')
            print("You said:", text)
            self.display_response(text)
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def display_response(self, tamil_text):
        response = self.translator.search_response(tamil_text)
        self.output_label.setText(response)

def main():
    app = QApplication(sys.argv)
    window = VoiceChatbotUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
