from gtts import gTTS
import streamlit as st
import tempfile
import os

def tts(text_val, language):
  obj = gTTS(text=text_val, lang=language, slow=False)  
  return obj


  
  
#GUI
st.header("Text to Speech Demos")
st.subheader("Choose a model to start with")
tab1, tab2, tab3 = st.tabs(["Google TTS", "Coming Soon", "Coming Soon 2"])

with tab1:
  st.header("Google Text To Speech")
  st.info("Step 1: Type in your text")
  text_val = st.text_area('Text to convert to speech')
  language = 'de'
  st.info("Step 2: Press 'Convert To Speech'")
  if st.button('Convert to Speech'):
    tts = tts(text_val, language)
    if (tts is not None):
      st.success("Success: Listen to your results!")
      # Save the audio file to a specific path
      temp_audio = os.path.join(tempfile.gettempdir(), "output.mp3")
      tts.save(temp_audio)

      # Read the audio file as bytes
      with open(temp_audio, "rb") as audio_file:
          audio_bytes = audio_file.read()

      # Play the audio in Streamlit
      st.audio(audio_bytes, format='audio/mp3')
    
    elif (text_val is None):
      st.error("Enter Text First!")    
    else:
      st.error("Error: result == null :(")
          
  
with tab2:
  st.header("Coming Soon")

with tab3:
  st.header("Coming Soon As Well")
  
