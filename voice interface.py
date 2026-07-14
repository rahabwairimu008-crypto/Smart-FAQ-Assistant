"""
voice_interface.py
Voice input/output layer for the Smart FAQ Assistant, per the project
brief's "Voice and Text Interface" requirement.

- Speech-to-text: uses SpeechRecognition + Google's free Web Speech API
  (requires an internet connection; no API key needed for light use).
- Text-to-speech: uses pyttsx3, which works fully OFFLINE (uses the
  system's built-in speech engine: espeak/espeak-ng on Linux, SAPI5 on
  Windows, NSSpeechSynthesizer on macOS).

Run directly for a voice-only Q&A loop:
    python3 voice_interface.py
"""

import speech_recognition as sr
import pyttsx3

from main import handle_query


def speak(text: str):
    """Speak text out loud using the offline TTS engine."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)  # slightly slower than default for clarity
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def listen_from_microphone(timeout: int = 6, phrase_time_limit: int = 12) -> str:
    """
    Record from the default microphone and transcribe it to text using
    Google's Web Speech API (requires internet).

    Returns the transcribed text, or an empty string if nothing could be
    understood.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... (speak your question now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
        except sr.WaitTimeoutError:
            print("No speech detected in time.")
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition service error (check your internet "
              f"connection): {e}")
        return ""


def run_voice_loop():
    """Continuous voice Q&A loop: listen -> process -> speak the answer."""
    print("Smart FAQ Assistant - Voice Mode (DeKUT SCIT)")
    print("Say 'exit' or 'quit' to stop.\n")
    speak("Welcome to the DeKUT SCIT Smart FAQ Assistant. Ask your question after the beep.")

    while True:
        question = listen_from_microphone()

        if not question:
            continue

        if question.strip().lower() in ("exit", "quit", "stop"):
            speak("Goodbye.")
            break

        result = handle_query(question)
        print(f"Category : {result['category_label']}")
        print(f"Answer   : {result['response']}\n")
        speak(result["response"])


if __name__ == "__main__":
    run_voice_loop()