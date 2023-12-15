# from googletrans import Translator
# from google.cloud import translate
# from google_trans_new import Translator
import argostranslate
from argostranslate import package, translate


# def translate_googletrans(text, lang='es'):
#     # Create a Translator object
#     translator = Translator(service_urls=['translate.googleapis.com'])  # use api directly instead of using a token
#
#     # Translate text
#     translation = translator.translate(text, dest=lang)
#
#     # Print translated text and language
#     print(f"Detected source language: {translation.src}")
#     print(f"Translated to language: {translation.dest}")
#     print(f"Translated text: {translation.text}")
#     return translation.text


# Google translate (keyfile is required)
# def translate_google_cloud(text, target_language='es'):
#     # Create a client
#     client = translate.TranslationServiceClient()
#     translation = client.translate_text(
#         contents=[text],
#         # target_language=target_language
#     )
#     return translation.translations[0].translated_text


# def translate_googletrans_new(text, target_language):
#     translator = Translator()
#     translation = translator.translate(text, lang_tgt=target_language)
#     translated_text = translation.text
#     return translated_text


def translate_argos(text, from_code='en', to_code='es'):
    # Download and install Argos Translate model package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    available_package = list(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )[0]

    download_path = available_package.download()
    argostranslate.package.install_from_path(download_path)

    # Translate
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = list(filter(
        lambda x: x.code == from_code,
        installed_languages))[0]
    to_lang = list(filter(
        lambda x: x.code == to_code,
        installed_languages))[0]

    translation = from_lang.get_translation(to_lang)
    translated_text = translation.translate(text)
    return translated_text


def do_translate(text, source_language='en', target_language='es'):
    return translate_argos(text, source_language, target_language)
