from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)


def get_oauth():
    url = "https://api.amazon.com/auth/o2/token"

    payload = "grant_type=refresh_token&refresh_token=Atzr%7CIwEBIFcejNniMjWprAGNEGufkxV03I9mLVMWOvD6NYq6YHlGolk6ZwlgGkZYBskhQLn-TNx2awIDsaraHJuFdNYkZNJDSQCBksEptOc_vmRgdoAGR530SPFg4lsYQ2TX2pCSawLmnnquJvj78e_X4bjaEohG2NHoUT--sK65fIcnX7Dq0wB0jLmGD6bk3kuWOrD6W6_ayGcznBCSfX-SEwjghPAVr9_T0jx3ytFmd6wuX1XytvxqfYIdCSTvZbG8aNwUA_6nsGvQW-mgz5fjJdI6lTUqFIPT_oaJ8RWuyMlOBdz6CqugU4Cy1QbJ_W3MJxea8dQ&client_id=amzn1.application-oa2-client.f1f1085ef8bc481bbffdd1096cc4ca93&client_secret=amzn1.oa2-cs.v1.f653279cdc0a6dc08d3a25c877beb0baf6f4a60a73c50ed59a0ee947feb2c064"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)

    (json.loads(response.text))
    return json.loads(response.text)["access_token"]

def get_product_upc(upc, access_token = get_oauth()):
    url = "https://sellingpartnerapi-na.amazon.com/catalog/v0/items/"

    querystring = {"MarketplaceId":"ATVPDKIKX0DER","UPC":upc}

    payload = ""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "user-agent": "Sellraze/0.0 (Language=Go; Platform=Windows/10)",
        "x-amz-access-token": access_token,
        "x-amz-date": "20230609T123456Z"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    return json.loads(response.text)

@app.route('/product', methods=['GET'])
def get_upc():
    upc = request.args.get('upc', None)

    if upc is None:
        return "Error: No UPC field provided. Please specify an UPC."
    else:
        product_name = get_product_upc(upc)

    return product_name["payload"]["Items"][0]["AttributeSets"][0]

@app.route('/')
def home():
    return '/product : Returns a product dictionary given a UPC'

@app.route('/ping')
def about():
    return 'pong mf'