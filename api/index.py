from flask import Flask, request
import json

from api.product_info import product_info_upc
from api.category_aspect_gen import get_category, get_aspects
#from api.description_gen import product_gen

# from product_info import product_info_upc
# from category_aspect_gen import get_category, get_aspects
# from description_gen import product_gen

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
# template = """
#             Wrap all key points into a JSON format.
#             If it isn't in the product, you will return N/A in the JSON. NO GUESSWORK

#             """
# system_message_prompt = SystemMessagePromptTemplate.from_template(template)
# human_template = """
# You are an e-commerce assistant making listings for this product:
# {text}
# You will then extract the quantity, size, new/old, brand, color, and create maximum three tags into a JSON.
# You will then create a title with this structure: Brand + Gender + Product Type + Attributes (color, size, material) . Put nothing if you don't have information.

# and a product description that only displays key information in a bulleted list. provide a description but do not make up anything.

# """
# human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

# chat_prompt = ChatPromptTemplate.from_messages(
#         [system_message_prompt, human_message_prompt]
#     )


from flask import request, jsonify

# @app.route('/product_gen', methods=['GET'])
# def product():
#     # Parse product from the incoming request
#     product = request.args.get('product', None)

#     if product is None:
#         return "Error: No product field provided. Please specify a product."
#     else:
#         product_info = product_gen(product, chat, chat_prompt)


    # return product_info

@app.route('/product', methods=['GET'])
def get_upc():
    upc = request.args.get('upc', None)

    if upc is None:
        return "Error: No UPC field provided. Please specify an UPC."
    else:
        product_info = product_info_upc(upc)

    new_data = []
    # Go through each item in the JSON data
    for index, item in enumerate(product_info['items']):
        if index >= 10:
            break
        
        try:
            brand = item['attributes']['brand'][0]['value']
        except KeyError:
            print("Failed to find key 'brand' in item.")
            brand = 'n/a'
            
        try:
            product_name = item['attributes']['item_name'][0]['value']
        except KeyError:
            print("Failed to find key 'name' in item.")
            product_name = 'n/a'

        try:
            first_image = item['images'][0]['images'][0]['link']
        except KeyError:
            print("Failed to find key 'first_image' in item.")
            first_image = 'n/a'

        try: 
            if "product_description" in item["attributes"]:
                product_description = item["attributes"]["product_description"][0]["value"]
            else:
                product_description = [bullet["value"] for bullet in item["attributes"]["bullet_point"]]
                product_description = "\n".join(product_description)
        except:
            print("Failed to find key 'product_description' in item.")
            product_description = 'n/a'
        
        try:
            classification = item['summaries'][0]['browseClassification']['displayName']
        except KeyError:
            print(item['summaries'][0])
            print("Failed to find key 'browseClassification' in item.")
            classification = 'n/a'

        try:
            item_weight = item['attributes']['item_weight'][0]
            weight = f"{item_weight['value']} {item_weight['unit']}"
        except KeyError:
            print("Failed to find key 'weight' in item.")
            weight = 'n/a'

        try:
            item_dimensions = item['attributes']['item_dimensions'][0]
            dimensions = f"{item_dimensions['length']['value']} x {item_dimensions['width']['value']} x {item_dimensions['height']['value']} {item_dimensions['height']['unit']}"
        except KeyError:
            print("Failed to find key 'dimensions' in item.")
            dimensions = 'n/a'

        try:
            item_price = item['attributes']['list_price'][0]
            price = f"{item_price['value']} {item_price['currency']}"
        except KeyError:
            print("Failed to find key 'list_price' in item.")
            price = 'n/a'

        # Create a dictionary with the brand, name and image, and add it to your list
        entry = {
        "title": product_name,
        "smallimage": first_image,
        "brand": brand,
        "product_description": product_description,
        'classification': classification,
        'weight': weight,
        'dimensions': dimensions,
        'price': price
        }
        new_data.append(entry)
    
    new_data_json = json.dumps(new_data, indent=4)
    return new_data_json

@app.route('/')
def home():
    return '/product : Returns a product dictionary given a UPC'

@app.route('/ping')
def about():
    return 'pong mf'

# #Comment this out when pushing to prod
# if __name__ == "__main__":
#     app.run(debug=True)
#     print("Flask server running on http://localhost:5000") 