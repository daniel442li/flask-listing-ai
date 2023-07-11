from dotenv import load_dotenv, find_dotenv
import json
load_dotenv(find_dotenv())

import time



def product_gen(prod, chat, chat_prompt):
    
    a = time.time()

    # get a chat completion from the formatted messages
    x = chat(
        chat_prompt.format_prompt(
        text=prod
        ).to_messages()
    )

    return json.loads(x.content)


