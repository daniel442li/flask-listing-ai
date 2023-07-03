import json
import requests
from api.oauth import amazon_get_oauth

def product_info_asin(asin):
    url = "https://sellingpartnerapi-na.amazon.com/catalog/2022-04-01/items/" + asin

    querystring = {"marketplaceIds":"ATVPDKIKX0DER","includedData":"attributes,dimensions,identifiers,images,productTypes,salesRanks,summaries,relationships"}

    payload = ""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "user-agent": "Decluttr/0.0 (Language=Go; Platform=Windows/10)",
        "x-amz-access-token": amazon_get_oauth(),
        "x-amz-date": "20230609T123456Z"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    return json.loads(response.text)

def product_info_upc(upc):
    url = "https://sellingpartnerapi-na.amazon.com/catalog/2022-04-01/items/"


    querystring = {"marketplaceIds":"ATVPDKIKX0DER","identifiersType":"UPC","identifiers":upc,"includedData":"attributes,dimensions,identifiers,images,productTypes,salesRanks,summaries,relationships"}
    payload = ""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "user-agent": "Decluttr/0.0 (Language=Go; Platform=Windows/10)",
        "x-amz-access-token": amazon_get_oauth(),
        "x-amz-date": "20230609T123456Z"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    return json.loads(response.text)