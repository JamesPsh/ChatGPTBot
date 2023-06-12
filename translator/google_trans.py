import logging
from googletrans import Translator, LANGUAGES


'''
https://pypi.org/project/googletrans/
'''


# Setup logging
logging.basicConfig(level=logging.INFO)

def translate(text, dest='en'):

    # Check if the language codes are valid
    if dest not in LANGUAGES.keys():
        logging.error(f"Unsupported destination language code: {dest}")
        return "Error: Unsupported destination language code."

    translator = Translator()
    
    try:
        ans = translator.translate(text, dest=dest)
        logging.info(f"Translation successful. Destination: {dest}")
        return ans.text
    except Exception as e:
        logging.error(f"Translation failed with error: {e}")
        return f"Error: Translation failed. {str(e)}"


if __name__ == '__main__':
    text = '안녕하세요'
    target_language = 'en'
    
    translated_text = translate(text, target_language)
    print(f"Original Text: {text}")
    print(f"Translated Text: {translated_text}")
