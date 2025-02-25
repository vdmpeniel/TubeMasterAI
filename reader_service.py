import synthesizer_coqui as synthesizer

def get_model_list():
    return synthesizer.get_model_list()

def get_speaker_list(model):
    return synthesizer.get_model_speaker_list(model)

def get_language_list(model):
    return synthesizer.get_model_language_list(model)

def read_out_loud(model, text, output_file_path):
    synthesizer.text_to_speech_coqui_single_speaker(
        text=text,
        output_file=output_file_path,
        model=model
    )