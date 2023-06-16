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
from pathlib import Path



st.subheader("TTS & STT Demos")
st.markdown("Choose what you want to do:")
tab1, tab2 = st.tabs(["Text To Speech", "Speech To Text Pre-Recorded"])

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
  st.subheader("Speech To Text Pre-Recorded")
  st.info("Step 1: Upload a recorded audio file; You can also download the generated file from the 'Text To Speech' tap!")
  uploaded_file2 = st.file_uploader("Upload an audio file2", type=["wav", "mp3"])
  st.info("Step 2: Choose a model")
  model_option = st.selectbox(
    "Select you prefered Model (If you need help deciding for a model press 'Help me decide')",
    ('Tiny', 'Base', 'Small', 'Medium', 'Large'))
  model_dict = {'Tiny':'tiny', 'Base':'base', 'Small':'small', 'Medium':'medium', 'Large':"large"}
  col1, col2, col3 = st.columns(3)
  with col2:
    if st.help_model_decide('Help me decide'):
      image = Image.open('files/help_me_decide_model.jpg')
  st.info("Step 3: Click 'Transcribe'")
  col1, col2, col3 = st.columns(3)
  with col2:
    execute_stt = st.button("Transcribe")
  if execute_stt:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file2.getvalue())
    model = whisper.load_model(model_dict[model_option])
    result = model.transcribe(tmp_file.name)
    st.success("Success! Here is your result:")
    st.code(result["text"])
    

    
    
 
      
    

  
  
