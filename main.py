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
  st.header("Speech To Text Pre-Recorded 2")
  model = whisper.load_model("base")
  uploaded_file2 = st.file_uploader("Upload an audio file2", type=["wav", "mp3"])
  execute_stt = st.button("Transcribe")
  if execute_stt:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file2.getvalue())
    result = model.transcribe(tmp_file.name)
    st.markdown(result["text"])
    
with tab3:
  st.header("Speech To Text Live")
  def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

  def main():
      st.header("Speech To Text Live")

      uploaded_file2 = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

      if uploaded_file2 is not None:
          audio_file = tempfile.NamedTemporaryFile(delete=False)
          audio_file.write(uploaded_file2.getvalue())
          audio_file.close()

      if uploaded_file2 is not None:
          st.audio(uploaded_file2)

          webrtc_ctx = webrtc_streamer(
              key="example",
              audio=False,
              video=False,
              client_settings={"is_streamlit_server": True},
          )

          if webrtc_ctx.audio_receiver:
              audio_receiver = webrtc_ctx.audio_receiver
              audio_file_path = Path(audio_file.name)

              with audio_file_path.open("rb") as f:
                  audio_content = f.read()

              audio_receiver.process_audio(audio_content)

              st.text("Transcription in progress:")
              st.empty()

              while True:
                  data = audio_receiver.get_intermediate_text()
                  if data:
                      st.text(data)

                  if not audio_receiver.more_data():
                      break

          if webrtc_ctx.state.playing:
              st.text("Transcription complete!")

  if __name__ == "__main__":
      main()
  
  
