from TTS.utils.generic_utils import setup_model
from TTS.tts.utils.io import load_config
from TTS.tts.utils.io import parse_path
from TTS.tts.utils.text.symbols import phonemes, symbols
from TTS.tts.utils.synthesis import synthesis
from TTS.tts.utils.text.cleaners import custom_english_cleaners
from TTS.tts.utils.audio import AudioProcessor


def text_to_speech(text, output_file='output.wav', model_path='your_model_path', config_path='your_config_path'):
    # Cargar la configuración del modelo
    model_path = parse_path(model_path)
    config_path = parse_path(config_path)
    config = load_config(config_path)

    # Configurar el modelo
    model = setup_model(num_chars=len(phonemes), dim_input=config['input_dim'])

    # Cargar el modelo preentrenado
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    # Sintetizar voz
    mel_output, mel_length, alignment = synthesis(text, model, config, use_cuda=False, ap=None, use_gl=False)

    # Configurar el procesador de audio
    ap = AudioProcessor(**config['audio'])

    # Guardar la salida en un archivo de audio
    ap.save_wav(mel_output[0].data.cpu().numpy(), output_file)


# Ejemplo de uso:
text_to_speech("Hola, esto es una prueba de voz en español.", output_file='output.wav')