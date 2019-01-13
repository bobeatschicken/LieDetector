def transcribe_model_selection(speech_file, model):
    """Transcribe the given audio file synchronously with
    the selected model."""
    from google.cloud import speech
    client = speech.SpeechClient()
    print (speech_file)
    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US',
        model=model)

    response = client.recognize(config, audio)
    transcript = ''
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        transcript = alternative.transcript
    return transcript
