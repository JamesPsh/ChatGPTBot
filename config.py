import os


class config:
    api_key = os.getenv("OPENAI_API_KEY")  # or [user api key]
    save_messages = True
    dir_save = 'messages'
    encoding = 'cp949'
