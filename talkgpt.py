import tkinter as tk
import pyttsx3
import openai
import speech_recognition as sr

engine = pyttsx3.init()
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"
engine.setProperty("rate", 200)
engine.setProperty('voice', voice_id)

r = sr.Recognizer()

openai.api_key = "GOTO-OPEN-AI-WEBSITE-AND-PASTE-YOUR-APIKEY-HERE"  

def speak(text):
    engine.say(text)
    engine.runAndWait()

def hear_me():
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="es-ES")
            print("He entendido: {}".format(text))
            return text
        except sr.UnknownValueError:
            return

def generate_text(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )


    message = response.choices[0].text.strip()
    return message

class MyGUI:

    def __init__(self, master):
        self.master = master
        master.title("Habla con CHAT-GPT")

        # Crea un widget Text para la respuesta
        self.response_text = tk.Text(master, height=10, width=50)
        self.response_text.pack()

        # Crea un widget Button para enviar la pregunta
        self.ask_button = tk.Button(master, text="Preguntar", command=self.ask_question)
        self.ask_button.pack()

    def ask_question(self):
        # Obtiene la pregunta ingresada por el usuario utilizando la función hear_me()
        prompt = hear_me()

        # Genera la respuesta utilizando OpenAI
        response = generate_text(prompt)

        # Muestra la respuesta en el widget Text
        self.response_text.delete('1.0', tk.END)
        self.response_text.insert(tk.END, response)

        # Habla la respuesta utilizando el motor de texto a voz
        speak(response)


# Crea una nueva ventana
root = tk.Tk()

# Crea una nueva instancia de la clase MyGUI
gui = MyGUI(root)

# Inicia el bucle de eventos
root.mainloop()

