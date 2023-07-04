from flask import Flask, request
import json
from api.product_info import product_info_upc
from api.description_gen import description_gen
from api.category_aspect_gen import get_category, get_aspects

app = Flask(__name__)


from flask import request, jsonify

@app.route('/ebay_gen_clothing', methods=['POST'])
def ebay_product_gen_clothing():
    # Parse JSON from the incoming request
    data = request.get_json()

    # Extract data from JSON
    brand = data.get('brand')
    age = data.get('age')
    style = data.get('style')
    size = data.get('size')
    color = data.get('color')
    product_description = data.get('product_description')

    constructed_title = f"{brand} {age} {style} {size} {color}"
    description = description_gen(product_description)
    category_tree_str, leaf_category_id = get_category(constructed_title)
    aspects = get_aspects(leaf_category_id)

    # Return the response as JSON
    return jsonify({
        "constructed_title": constructed_title,
        "description": description,
        "category_tree_str": category_tree_str,
        "aspects": aspects
    })


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

#Comment this out when pushing to prod
# if __name__ == "__main__":
#     app.run(debug=True)
#     print("Flask server running on http://localhost:5000") 