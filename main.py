from gtts import gTTS
import streamlit as st
import tempfile
import os

def m_tts(text_val, language):
  obj = gTTS(text=text_val, lang=language, slow=False)  
  return obj


  
  
#GUI
st.title("Text to Speech Demos")
st.markdown("Choose a model to start with")
tab1, tab2, tab3 = st.tabs(["Google TTS", "Coming Soon", "Coming Soon 2"])

with tab1:
  st.subheader("Google Text To Speech")
  
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
  st.header("Coming Soon")

with tab3:
  st.header("Coming Soon As Well")
  
