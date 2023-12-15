def transcribe_audio_vosk(model, audio_path):
    SetLogLevel(0)
    sample_rate = 16000

    # Initialize Vosk recognizer
    vosk_model = Model(lang=model)
    recognizer = KaldiRecognizer(vosk_model, sample_rate)
    recognizer.SetWords(True)

    # Read audio file
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()

    # Perform recognition
    recognizer.AcceptWaveform(audio_data)
    result = recognizer.Result()

    return json.loads(result)
