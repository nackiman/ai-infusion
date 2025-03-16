import os
import sqlite3
import time
import random
from gtts import gTTS
import pygame

# Initialize Pygame Mixer for Audio Playback
pygame.mixer.init()

def speak(text):
    """Generates and plays an MP3 speech file."""
    tts = gTTS(text=text, lang="en")
    tts.save("vex_voice.mp3")
    pygame.mixer.music.load("vex_voice.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# Create or Connect to Memory Database
conn = sqlite3.connect("vex_memory.db")
cursor = conn.cursor()

# Create Memory Table if Not Exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command TEXT,
    response TEXT
);
""")
conn.commit()

def learn_command(command, response):
    """Vex learns new commands"""
    cursor.execute("INSERT INTO memory (command, response) VALUES (?, ?)", (command, response))
    conn.commit()
    speak("I have learned a new command.")

def get_response(command):
    """Vex recalls stored responses"""
    cursor.execute("SELECT response FROM memory WHERE command = ?", (command,))
    result = cursor.fetchone()
    return result[0] if result else None

def process_command(command):
    """Vex processes commands"""
    if command == "exit":
        speak("Goodbye.")
        exit()
    
    # Check if Vex already knows the command
    response = get_response(command)
    if response:
        speak(response)
    else:
        speak("I don't know that yet. What should I say next time?")
        new_response = input("Teach Vex: ")
        learn_command(command, new_response)

# Startup Message
speak("Vex AI System Initialized.")
print("Vex AI System Initialized. Ready for commands.")

while True:
    user_command = input("You: ")  # For manual typing
    process_command(user_command)
