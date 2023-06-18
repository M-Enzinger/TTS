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
from PIL import Image
import wave


st.subheader("TTS & STT Demos")
st.markdown("Choose what you want to do:")
st.markdown("Link to Github Repository: https://github.com/M-Enzinger/TTS")
tab1, tab2, tab3 = st.tabs(["Text To Speech", "Speech To Text Pre-Recorded", "Live Transcribtion"])

#text to speech section
with tab1:
  #Text to Speech-object function
  def m_tts(text_val, language):
    obj = gTTS(text=text_val, lang=language, slow=False)
    return obj

  #users text input
  st.subheader("Text To Speech")
  st.info("Step 1: Type in your text")
  text_val = st.text_area('Text to convert to speech') + '.'
  
  #user selects language
  st.info("Step 2: Choose your language")
  language_option = st.selectbox(
    'To which language to you want to convert to? (more possible)',
    ('English', 'German', 'French', 'Spanish'))
  
  #Adding disclaimer
  if (language_option == 'English'):
    text_val += ". I know my voice doesn't sound perfect yet. I am just a demo. In the future, Max will replace me with a better voice!"
  elif (language_option == 'German'):
    text_val += ". Ich weiß, dass meine Stimme noch nicht perfekt klingt. Ich bin nur eine Demo. In Zukunft wird Max mich durch eine bessere Stimme ersetzten!"
  
  #converting language selection
  lang_dict = {'English':'en', 'German':'de', 'French':'fr', 'Spanish':'es'}
  language = lang_dict[language_option]
  
  #Execution button
  st.info("Step 3: Press 'Convert To Speech'")
  col1, col2, col3 = st.columns(3)
  with col2:
    execute_tts = st.button('Convert to Speech')   
    
  #Checking whether button has been pressed & text input is (not) empty
  if (execute_tts and (len(text_val) >= 1)):
    #calling text to speech function
    tts = m_tts(text_val, language)
    st.warning("Please wait...")
    
    #Save the audio file to a specific path
    tts_temp_audio = os.path.join(tempfile.gettempdir(), "output.mp3")
    tts.save(tts_temp_audio)

    #Read the audio file as bytes
    with open(tts_temp_audio, "rb") as audio_file:
        tts_audio_bytes = audio_file.read()

    #Play the audio in Streamlit
    st.success("Success: Listen to your results or download it as a mp3! You can edit your text and click on the button again to convert a new text.")
    st.audio(tts_audio_bytes, format='audio/mp3')
    
    #Download the file
    col1, col2, col3 = st.columns(3)
    with col2:
      st.download_button(
      label="Download Audio",
      data=tts_audio_bytes,
      file_name='Generated_Audio.mp3',
      mime='mp3',)
      
  #If text box is empty
  elif (execute_tts):
    st.error("Enter Text First!")

#Speech to text section
with tab2:
  #audio upload
  st.subheader("Speech To Text Pre-Recorded")
  st.info("Step 1: Upload a recorded audio file; You can also upload the file you generated in the 'Text To Speech' tab before!")
  audio_stt = st.file_uploader("Upload an audio file2", type=["wav", "mp3"])
  
  #user chooses model
  st.info("Step 2: Choose a model")
  stt_model_option = st.selectbox(
    "Select you prefered Model (If you need help deciding for a model press 'Help me decide'). Small, Medium & Large are exceeding the free cloud ressources.",
    ('Tiny', 'Base'), index=1)
  #converting model selection
  stt_model_dict = {'Tiny':'tiny', 'Base':'base'}
  
  #offer help to  decide for a model
  col1, col2, col3 = st.columns(3)
  with col2:
    help_me_decide_button = st.button('Help me decide')
  if help_me_decide_button:
    image_models = Image.open('files/help_me_decide_model.jpg')
    st.image(image_models, caption='Source: https://github.com/openai/whisper')
      
  #execution button
  st.info("Step 3: Click 'Transcribe'")
  col1, col2, col3 = st.columns(3)
  with col2:
    execute_stt = st.button("Transcribe")
    
  #check whether execution button has been pressed
  if execute_stt:
    #creating temp file for uploaded audio
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            fp = Path(tmp_file.name)
            fp.write_bytes(audio_stt.getvalue())
       
    #loading preselected model using the dictionary
    stt_model = whisper.load_model(stt_model_dict[stt_model_option])
    
    #transcribing
    st.warning("Please wait...")
    stt_result = stt_model.transcribe(tmp_file.name)
    
    #returning results to user
    st.success("Success! Upload a new file and/or change the model and hit 'Transribe' again for a new prediction!")
    st.markdown(stt_result["text"])
    

with tab3:
  #method to het duration of audio file
  def get_wav_duration(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        frames = wav_file.getnframes()
        frame_rate = wav_file.getframerate()
        duration = frames / float(frame_rate)
    return duration

  #file upload
  st.subheader("Live Transcribtion Simulation")
  st.info("Step 1: Upload a Wav file")
  audio_livestt = st.file_uploader("Upload an audio file2", type=["wav"])

  #user chooses model
  st.info("Step 2: Choose a model")
  stt_model_option = st.selectbox(
    "Select you prefered Model. Small, Medium & Large are exceeding the free cloud ressources.",
    ('Tiny Model', 'Base Model'), index=1)
  
  #converting model selection
  stt_model_dict = {'Tiny':'tiny', 'Base':'base'}

  #user chooses snipet unique time
  st.info("Step 3: Choose the unique time of each snippet. Overlapping time not included.")
  selected_duration = st.slider(
    'Select a range of values', 0.0, 20.0, 5.0, 0.1)

  #user chooses overlapping time
  st.info("Step 4: Choose overlapping time")
  overlapping = st.slider(
    'Select a range of values', 0.0, 2.0, 0.5, 0.1)

  #user requests transcription
  st.info("Step 5: Click 'Transcribe'")
  col1, col2, col3 = st.columns(3)
  with col2:
    live_stt_execute = st.button('blabla')

  #check whether user requested transcription
  if (live_stt_execute):
    #get audio duration
    audio_duration = get_wav_duration(audio_livestt)

    #calculate amount of splits and provide feedback to user
    n_steps = int(audio_duration / selected_duration) + 1
    st.success('Duration of the audio file: ' + str(audio_duration) + ' seconds.')
    st.success('Unique duration of each audio file of the audio file: ' + str(selected_duration) + ' seconds. Overlapping time not included. Last one might be shorter.')
    st.success('Amount of splits which are separetly analysed: ' + str(n_steps) + '.')
    st.success('Overlapping time per split: ' + str(overlapping) + ' seconds.')

    #splitting and trancribing according to the amount of splits
    for n in range(n_steps):
      #timestamp of the beginning of the snipe
      t1 = n*selected_duration*1000 #Works in milliseconds

      #timestamp of the end of the snipet, including the overlapping time
      t2 = ((n+1)*selected_duration+overlapping) * 1000

      #cutting the audio and extraxting the snippet
      newAudio = AudioSegment.from_wav(audio_livestt)
      newAudio = newAudio[t1:t2]
      newAudio_temp = os.path.join(tempfile.gettempdir(), "output.wav")
      newAudio.export(newAudio_temp, format="wav") #Exports to a wav file in the current path.

      #showing an audio player
      st.subheader('Audio snippet ' + str(n+1) + ' of ' + str(n_steps) + '.')
      st.audio(newAudio_temp, format='wav')

      #transcribing the snippet
      #loading preselected model using the dictionary
      live_stt_model = whisper.load_model(stt_model_dict[stt_model_option])
      
      #transcribing
      live_stt_result = live_stt_model.transcribe(newAudio_temp)
      
      #returning results to user
      st.markdown(live_stt_result["text"])
