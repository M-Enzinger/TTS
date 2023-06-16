from gtts import gTTS
import streamlit as st
import tempfile
import os

def m_tts(text_val, language):
  obj = gTTS(text=text_val, lang=language, slow=False)  
  return obj


  
  

st.title("Text to Speech Demos")
st.markdown("Choose a model to start with")
tab1, tab2, tab3 = st.tabs(["Google TTS", "Speech To Text Pre-Recorded", "Speech To Text Live"])

with tab1:
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
  st.header("Speech To Text Pre-Recorded")

with tab3:
  st.header("Speech To Text Live")
  
