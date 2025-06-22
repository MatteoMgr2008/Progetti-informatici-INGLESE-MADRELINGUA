import flask
import ollama
import logging
from flask import render_template, request

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

# Inizializzazione dell'app Flask
app=flask.Flask(__name__)

# Inizializzazione del client AI Ollama
ollama_client=ollama.Client()

# Route per la pagina principale (index.html)
@app.route("/", methods=["GET", "POST"])
def index():
    testo_risposta_AI=""
    if request.method=="POST":
        # Ottenimento del prompt immesso dall'utente
        prompt_utente=request.form["prompt_utente"]
        # Chiamata al modello (attraverso il nome) di Ollama per generare una risposta
        nome_modello_Ollama="OrangeHat_AI_chatbot"
        # Generazione di una risposta alla domanda dell'utente
        risposta_AI=ollama_client.generate(model=nome_modello_Ollama, prompt=prompt_utente)
        testo_risposta_AI=risposta_AI.get('response', '')
        logging.info("")
        logging.info("USER QUESTION TEXT:")
        logging.info(prompt_utente)
        logging.info("")
        logging.info("AI RESPONSE TEXT:")
        logging.info(testo_risposta_AI)
    return render_template("index.html", response=testo_risposta_AI)

# Avvio dell'app Flask
if __name__=="__main__":
    app.run(debug=True)