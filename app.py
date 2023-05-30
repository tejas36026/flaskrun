from flask import Flask, jsonify, request
import speech_recognition as sr
from pydub import AudioSegment
from flask_cors import CORS
from moviepy.editor import VideoFileClip

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://chat.openai.com"]}})

@app.route("/", methods=["POST"])
def transcribe():
    # Get the uploaded file from the request
    file = request.files["file"]
    
    # Save the uploaded file to disk with its original filename
    filename = file.filename
    file.save(filename)
    
    # Convert the audio file to a WAV file using pydub
    audio_format = filename.split(".")[-1]
    if audio_format == "mp3":
        audio = AudioSegment.from_mp3(filename)
    elif audio_format == "wav":
        audio = AudioSegment.from_wav(filename)
    elif audio_format == "aiff":
        audio = AudioSegment.from_file(filename, format="aiff")
    elif audio_format == "aac":
        audio = AudioSegment.from_file(filename, format="aac")
    elif audio_format == "flac":
        audio = AudioSegment.from_file(filename, format="flac")
    elif audio_format == "ogg":
        audio = AudioSegment.from_ogg(filename)
    elif audio_format == "mp4":
        video = VideoFileClip(filename)
        audio = video.audio
    # Export the converted audio as a WAV file
    # Export the converted audio as a WAV file
    if audio_format == "mp4":
        audio.write_audiofile("my_audio.wav")
    else:
        audio.export("my_audio.wav", format="wav")

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable
    with sr.AudioFile('my_audio.wav') as source:
        audio_text = r.listen(source)

    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        # using google speech recognition
        text = r.recognize_google(audio_text)
        print('Converting audio transcripts into text ...')
        print(text)
        return jsonify({"transcription": text})
    except sr.RequestError as e:
        print(f"An error occurred while transcribing the audio: {e}")
        return jsonify({"error": f"An error occurred while transcribing the audio: {e}"})
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return jsonify({"error": "Google Speech Recognition could not understand audio"})
    except:
        print('Sorry.. run again...')
        return jsonify({"error": "An error occurred while transcribing the audio"})

@app.errorhandler(Exception)
def handle_exception(e):
    # Return a JSON error response for unhandled exceptions
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()