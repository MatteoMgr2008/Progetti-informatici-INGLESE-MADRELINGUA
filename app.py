from flask import Flask, request, jsonify, send_from_directory, render_template  # Aggiunto jsonify
from gtts import gTTS
import cohere
import os

app = Flask(__name__)

# Route per visualizzare il form HTML
@app.route('/')
def index():
    return render_template('index.html')  # Flask cerca in 'templates/index.html'

# Route per generare l'audio
@app.route('/genera', methods=['POST'])
def genera_audio():
    cohere_api_key = os.getenv('Bvh8JLQtfFnLqV7cie8mIj4f1ICEuU8rTtHMecvO')
    
    # Inizializza il client con la tua API key di Cohere
    co = cohere.Client(cohere_api_key)  # Usa la chiave API dalla variabile d'ambiente
    # Accetta input dall'utente
    input_testo = request.form['prompt']
    # Definisci un prompt che includa il campo selezionato
    prompt_specifico = f"You are an AI assistant specializing in health, sports, and fitness. Only answer questions related to these topics: health, exercise, diet, nutrition, and wellness. {input_testo}"   # Genera il testo senza specificare il modello
    risposta_input_testo = co.generate(
        prompt=prompt_specifico,
        max_tokens=500,  # Compromesso tra dettagli e brevità
        temperature=0.5  # Per aggiungere un po' di creatività ma restando coerente
    )
    print(risposta_input_testo.generations[0].text)
    testo_finale = risposta_input_testo.generations[0].text

    # Usa gTTS per convertire il testo in parlato
    tts = gTTS(text=testo_finale, lang='en', slow=False)  # Cambia 'en' con 'it' per italiano
    audio_file = 'static/output.mp3'
    
    # Salva l'audio in un file
    tts.save(audio_file)

 # Restituisci il testo e il percorso dell'audio
    return jsonify({'testo': testo_finale, 'audio_url': f'/{audio_file}'})

# Serve il file audio
@app.route('/static/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)