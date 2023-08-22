import os
import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(audio_file):
    # Ensure that the file is an audio file
    if not audio_file.lower().endswith(('.wav', '.flac', '.mp3')):
        return "Error: The file is not an audio file."

    # If the file is an MP3 file, convert it to WAV
    if audio_file.lower().endswith('.mp3'):
        audio = AudioSegment.from_mp3(audio_file)
        audio_file = audio_file.replace('.mp3', '.wav')
        audio.export(audio_file, format='wav')

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Split the audio_file path into directory and file components
    directory, filename = os.path.split(audio_file)

    # Get the filename without the extension
    filename_no_ext = os.path.splitext(filename)[0]

    # Load audio to pydub
    audio = AudioSegment.from_file(audio_file)

    # Break audio into 5-minute chunks
    chunk_length = 3 * 60 * 1000  # Length of chunks in milliseconds
    chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]

    full_transcription = ""

    # Process each chunk
    for i, chunk in enumerate(chunks):
        # Export chunk as wav file
        chunk_file = os.path.join(directory, f"{filename_no_ext}_chunk{i}.wav")
        chunk.export(chunk_file, format="wav")

        # Load chunk file into recognizer
        with sr.AudioFile(chunk_file) as source:
            # Adjust for ambient noise and record
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)

        # Try to recognize the speech using Google Web Speech API
        try:
            transcript = recognizer.recognize_google(audio_data)
            full_transcription += transcript + " "
        except sr.UnknownValueError:
            full_transcription += "Sorry, could not understand the audio in this segment. "
        except sr.RequestError as e:
            full_transcription += f"Error during speech recognition in this segment: {e} "

        # Remove chunk file after transcription
        os.remove(chunk_file)

    return full_transcription
