import speech_recognition as sr
from googletrans import Translator
import pandas as pd
from fuzzywuzzy import process
from gtts import gTTS
import os
from flask import Flask, request, jsonify, send_file, render_template

app = Flask(__name__)

class TamilTranslator:
    def __init__(self):
        self.translator = Translator()
        self.dataset = pd.read_csv("D:/CIP Project/questionsv4.csv")

    def translate_tamil_to_english(self, tamil_text):
        return self.translator.translate(tamil_text, src='ta', dest='en').text
    
    def translate_english_to_tamil(self, english_text):
        return self.translator.translate(english_text, src='en', dest='ta').text

    def search_response(self, query):
        questions = self.translate_tamil_to_english(query)
        match, score, temp = process.extractOne(questions, self.dataset['questions'])
        
        if match:
            response = self.dataset.loc[self.dataset['questions'] == match, 'answers'].values[0]
            tamil_response = self.translate_english_to_tamil(response)
            return tamil_response
        return "Sorry, I couldn't find a relevant response."

def text_to_speech(text, temp_output_file):
    tts = gTTS(text=text, lang='ta')
    tts.save(temp_output_file)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    audio_data = request.json['audio_data']
    
    translator = TamilTranslator()
    response = translator.search_response(audio_data)

    temp_output_file = 'static/temp_response.mp3'
    text_to_speech(response, temp_output_file)

    return jsonify({'response': response, 'audio_file': temp_output_file})

@app.route('/audio/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
