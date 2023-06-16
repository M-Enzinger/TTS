from gtts import gTTS
import streamlit as st
import tempfile
import os
import speech_recognition as sr
import pydub

st.title("TTS & STT Demos")
st.markdown("Choose what you want to do:")
tab1, tab2, tab3 = st.tabs(["Text To Speech", "Speech To Text Pre-Recorded", "Speech To Text Live"])

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
st.header("Speech To Text Pre-Recorded")
  def transcribe_speech(audio_file):
    # Initialize the recognizer
    r = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    # Perform speech recognition
    try:
        text = r.recognize_sphinx(audio)
        return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service: {e}"

  if uploaded_file:
    st.audio(uploaded_file, format='audio/wav')

    if st.button("Transcribe"):
        if uploaded_file.name.endswith(".mp3"):
            # Convert MP3 to WAV
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                temp_wav_path = temp_wav.name
                audio = pydub.AudioSegment.from_mp3(uploaded_file)
                audio.export(temp_wav_path, format="wav")

            text_output = transcribe_speech(temp_wav_path)

            # Delete temporary WAV file
            os.remove(temp_wav_path)
        else:
            text_output = transcribe_speech(uploaded_file)

        st.write("Transcription:")
        st.write(text_output)

with tab3:
  st.header("Speech To Text Live")
  
