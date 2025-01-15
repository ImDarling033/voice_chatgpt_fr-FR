################################################################
# Nick Bild
# January 2023
# https://github.com/nickbild/voice_chatgpt
#
# Voice-controlled ChatGPT prompt
################################################################
import os
import io
import sys
import asyncio
import argparse
import pyaudio
import wave
from google.cloud import speech
from google.cloud import texttospeech
from ChatGPT_lite.ChatGPT import Chatbot


gpt_response = ""


def speech_to_text(speech_file):
    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
            content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="fr-FR",
    )

    # Détecte la parole dans le fichier audio
    response = client.recognize(config=config, audio=audio)

    stt = ""
    for result in response.results:
        stt += result.alternatives[0].transcript

    return stt


def ask_chat_gpt(args, prompt):
    global gpt_response
    chat = Chatbot(args.session_token, args.bypass_node)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(chat.wait_for_ready())
    response = loop.run_until_complete(chat.ask(prompt))
    chat.close()
    loop.stop()
    
    gpt_response = response['answer']

    return


def text_to_speech(tts):
    # Instancier un client
    client = texttospeech.TextToSpeechClient()

    # Définir la saisie de texte à synthétiser
    synthesis_input = texttospeech.SynthesisInput(text=tts)

    # Construisez la requête vocale, sélectionnez le code langue ("fr-FR") et le ssml
    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Sélectionnez le type de fichier audio que vous souhaitez renvoyer
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Exécutez la requête de synthèse vocale sur la saisie de texte avec les
    # paramètres vocaux et le type de fichier audio sélectionnés
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Le "audio_content" de la réponse est binaire.
    with open("result.wav", "wb") as out:
        # Écrivez la réponse dans le fichier de sortie.
        out.write(response.audio_content)

    return


def record_wav():
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 16000
    chunk = 4096
    record_secs = 3
    dev_index = 1
    wav_output_filename = 'input.wav'

    audio = pyaudio.PyAudio()

    # Créer un flux pyaudio.
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("recording")
    frames = []

    # Parcourez le flux et ajoutez des morceaux audio au tableau de trames.
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")

    # Arrêtez le flux, fermez-le et terminez l'instanciation pyaudio.
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Enregistrez les images audio sous forme de fichier ".wav".
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--session_token_file', type=str, default="openai_session.txt")
    parser.add_argument('--bypass_node', type=str, default="https://gpt.pawan.krd")
    args = parser.parse_args()

    # Obtenez les informations d’identification OpenAI à partir du fichier.
    text_file = open(args.session_token_file, "r")
    args.session_token = text_file.read()
    text_file.close()

    # Obtenez le WAV du microphone.
    record_wav()

    # Convertir l'audio en texte.
    question = speech_to_text("input.wav")
    
    # Envoyez du texte à ChatGPT.
    print("Asking: {0}".format(question))
    asyncio.coroutine(ask_chat_gpt(args, question))
    print("Response: {0}".format(gpt_response))

    # Convertissez la réponse ChatGPT en audio.
    text_to_speech(gpt_response)

    # Écouter l'audio de la réponse.
    os.system("aplay result.wav")


if __name__ == "__main__":
    main()
