from gtts import gTTS
import streamlit as st

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
    result = tts(text_val, language)
    if (result != Null):
      st.success("Success: Listen to your results!")
      #playing the audio
      audio_file = open('myaudio.ogg', 'rb')
      audio_bytes = audio_file.read()
      st.audio(result, format='audio/ogg')
    
    elif (text_val == Null):
      st.error("Enter Text First!")    
    else:
      st.error("Error: result == null :(")
          
  
with tab2:
  st.header("Coming Soon")

with tab3:
  st.header("Coming Soon As Well")
  
