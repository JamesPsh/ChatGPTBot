import os
import openai
from config import config


'''
# reference
https://platform.openai.com/docs/guides/chat
https://www.youtube.com/watch?v=b-QeMi1A2go
'''


class ChatBot:
    def __init__(self):
        self.messages = []


    def get_answer(self, user_content):
        # Save user utterance
        self.messages.append({'role': 'user', 'content': user_content})

        # generate answer
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        assistant_content = completion.choices[0].message['content'].strip()

        # Save chatbot answers
        self.messages.append({'role': 'assistant', 'content': assistant_content})

        return assistant_content


    def save_messages_to_csv(self):
        import datetime
        import pandas as pd

        # Get the current time and format it as a string
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d_%H-%M-%S')

        # Create the CSV file path with the formatted time
        idx = 0
        while True:
            path = os.path.join(config.dir_save, f'{formatted_time}_{idx}.csv')
            if not os.path.exists(path):
                break
            idx += 1

        # Write the data to the CSV file
        with open(path, 'w', encoding=config.encoding) as csvfile:
            pd.DataFrame(self.messages).to_csv(csvfile, index=False)


def main():
    chatbot = ChatBot()
    openai.api_key = config.api_key

    try:
        while True:
            # User input
            user_content = input('user: ')
            
            # Chatbot answer
            assistant_content = chatbot.get_answer(user_content)
            
            # Print answer
            print(f'GPT: {assistant_content}')

    except KeyboardInterrupt:
        print("Ctrl+C detected. Stopping the conversation.")
        if config.save_messages:
            chatbot.save_messages_to_csv()


if __name__ == '__main__':
    main()
