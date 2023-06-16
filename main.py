from gtts import gTTS
import streamlit as st
import tempfile
import os
import speech_recognition as sr
from pydub import AudioSegment
import ffmpeg
import numpy as np
import whisper
import soundfile as sf



st.title("TTS & STT Demos")
st.markdown("Choose what you want to do:")
tab1, tab2, tab3 = st.tabs(["Text To Speech", "Speech To Text Pre-Recorded", "Speech To Text Pre-Recorded 2"])

with tab1:
  def m_tts(text_val, language):
    obj = gTTS(text=text_val, lang=language, slow=False)  
    return obj

  st.subheader("Text To Speech")
  
  st.info("Step 1: Type in your text")
  text_val = st.text_area('Text to convert to speech')
  
  st.info("Step 2: Choose your language")
  language_option = st.selectbox(
    'To which language to you want to convert to? (more possible)',
    ('English', 'German', 'French', 'Spanish'))
  lang_dict = {'English':'en', 'German':'de', 'French':'fr', 'Spanish':'es'}
  language = lang_dict[language_option]
  
  st.info("Step 3: Press 'Convert To Speech'")
  col1, col2, col3 = st.columns(3)
  with col2:
    execute = st.button('Convert to Speech')   
  if (execute and (len(text_val) >= 1)):
    tts = m_tts(text_val, language)
    st.success("Success: Listen to your results!")
    # Save the audio file to a specific path
    temp_audio = os.path.join(tempfile.gettempdir(), "output.mp3")
    tts.save(temp_audio)

    # Read the audio file as bytes
    with open(temp_audio, "rb") as audio_file:
        audio_bytes = audio_file.read()

    # Play the audio in Streamlit
    st.audio(audio_bytes, format='audio/mp3')
  elif (execute):
    st.error("Enter Text First!")


with tab2:
  def transcribe_speech(audio_file):
      # Initialize the recognizer
      r = sr.Recognizer()

      # Load the audio file with pydub
      audio = AudioSegment.from_file(audio_file)

      # Export the audio as WAV to a temporary file
      temp_wav_path = os.path.join(tempfile.gettempdir(), "temp.wav")
      audio.export(temp_wav_path, format="wav")

      # Perform speech recognition
      try:
          with sr.AudioFile(temp_wav_path) as source:
              # Read the entire audio file
              audio_data = r.record(source)
              text = r.recognize_sphinx(audio_data)
          return text
      except sr.UnknownValueError:
          return "Speech recognition could not understand audio"
      except sr.RequestError as e:
          return f"Could not request results from Google Speech Recognition service: {e}"

  # Streamlit app
  st.title("Speech-to-Text with pydub and SpeechRecognition")

  # Audio file upload
  uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"], accept_multiple_files=False)

  # Perform speech-to-text conversion and display the result
  if uploaded_file:
      st.audio(uploaded_file, format='audio/wav')

      if st.button("Transcribe"):
          text_output = transcribe_speech(uploaded_file)
          st.write("Transcription:")
          st.write(text_output)

with tab3:
  st.header("Speech To Text Pre-Recorded 2")
  model = whisper.load_model("base")
  uploaded_file2 = st.file_uploader("Upload an audio file2", type=["wav", "mp3"])
  execute_stt = st.button("Transcribe")
  if execute_stt:
    st.markdown(type(uploaded_file2))
    result = model.transcribe(uploaded_file2)
    print(result["text"])
  
