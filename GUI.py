from tkinter import *
from main import chat, bot_name
import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class GUI:

    def __init__(self):
        self.window = Tk()
        self.m_on = PhotoImage(file = "mon.png")
        self.m_off = PhotoImage(file = "moff.png")
        self.s_on = PhotoImage(file = "son.png")
        self.s_off = PhotoImage(file = "soff.png")
        self.m_is_on = True
        self.s_is_on = True
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chatbot")
        self.window.resizable(width = False, height = False)
        self.window.configure(width = 470, height = 550, bg = BG_COLOR)

        head_label = Label(self.window, bg = BG_COLOR, fg = TEXT_COLOR, text = "Hello, I am online. Type 'quit' to exit.", font = FONT_BOLD, pady = 10)
        head_label.place(relwidth = 1)

        line = Label(self.window, width = 450, bg = BG_GRAY)
        line.place(relwidth = 1, rely = 0.07, relheight = 0.012)

        self.text_widget = Text(self.window, width = 20, height = 2, bg = BG_COLOR, fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5)
        self.text_widget.place(relheight = 0.745, relwidth = 1, rely = 0.08)
        self.text_widget.configure(cursor = "arrow", state = DISABLED)

        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight = 1, relx = 0.974)
        scrollbar.configure(command = self.text_widget.yview)

        bottom_label = Label(self.window, bg = BG_GRAY, height = 80)
        bottom_label.place(relwidth = 1, rely = 0.825)

        self.msg_entry = Entry(bottom_label, bg = "#2C3E50", fg = TEXT_COLOR, font = FONT)
        self.msg_entry.place(relwidth = 0.74, relheight = 0.06, rely = 0.008, relx = 0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        send_button = Button(bottom_label, text = "Send", font = FONT_BOLD, width = 20, bg = BG_GRAY, command = lambda: self._on_enter_pressed(None))
        send_button.place(relx = 0.77, rely = 0.0072, relheight = 0.03, relwidth = 0.22)

        self.mic_button = Button(self.window, image = self.m_on, bd = 0, command = self.switch_mic)
        self.mic_button.place(relx = 0.77, rely = 0.925, relheight = 0.065, relwidth = 0.10)
        self.speaker_button = Button(self.window, image = self.s_on, bd = 0, command = self.switch_speaker)
        self.speaker_button.place(relx = 0.88, rely = 0.925, relheight = 0.065, relwidth = 0.10)

        self.speak("Hello, I am online. Type 'quit' to exit.")

    def switch_mic(self):
        if self.m_is_on:
            self.mic_button.config(image = self.m_off)
            self.m_is_on = False
        else:
            self.mic_button.config(image = self.m_on)
            self.m_is_on = True

    def switch_speaker(self):
        if self.s_is_on:
            self.speaker_button.config(image = self.s_off)
            self.s_is_on = False
        else:
            self.speaker_button.config(image = self.s_on)
            self.s_is_on = True

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")

    def speak(self, text):
        tts = gTTS(text = text, lang = 'en')
        filename = 'voice.mp3'
        tts.save(filename)
        playsound.playsound(filename)

    def get_audio(self):
        if self.m_is_on:
        	r = sr.Recognizer()
        	with sr.Microphone() as source:
        		audio = r.listen(source)
        		said = ""
        		try:
        		    said = r.recognize_google(audio)
        		    self._insert_message(said, "You")
        		except Exception as e:
        		    print("Exception: " + str(e))

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state = NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state = DISABLED)

        msg2 = f"{bot_name}: {chat(msg)}\n\n"
        self.text_widget.configure(state = NORMAL)
        self.text_widget.insert(END, msg2)
        if self.s_is_on:
            self.speak(msg2)
        self.text_widget.configure(state = DISABLED)

        self.text_widget.see(END)

if __name__ == "__main__":
    app = GUI()
    app.run()
