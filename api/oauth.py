import requests
import json

def amazon_get_oauth():
    url = "https://api.amazon.com/auth/o2/token"

    payload = "grant_type=refresh_token&refresh_token=Atzr%7CIwEBIFcejNniMjWprAGNEGufkxV03I9mLVMWOvD6NYq6YHlGolk6ZwlgGkZYBskhQLn-TNx2awIDsaraHJuFdNYkZNJDSQCBksEptOc_vmRgdoAGR530SPFg4lsYQ2TX2pCSawLmnnquJvj78e_X4bjaEohG2NHoUT--sK65fIcnX7Dq0wB0jLmGD6bk3kuWOrD6W6_ayGcznBCSfX-SEwjghPAVr9_T0jx3ytFmd6wuX1XytvxqfYIdCSTvZbG8aNwUA_6nsGvQW-mgz5fjJdI6lTUqFIPT_oaJ8RWuyMlOBdz6CqugU4Cy1QbJ_W3MJxea8dQ&client_id=amzn1.application-oa2-client.f1f1085ef8bc481bbffdd1096cc4ca93&client_secret=amzn1.oa2-cs.v1.f653279cdc0a6dc08d3a25c877beb0baf6f4a60a73c50ed59a0ee947feb2c064"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)

    (json.loads(response.text))
    return json.loads(response.text)["access_token"]

def ebay_get_oauth():
    url = "https://api.ebay.com/identity/v1/oauth2/token"

    payload = "grant_type=refresh_token&refresh_token=v%5E1.1%23i%5E1%23I%5E3%23f%5E0%23r%5E1%23p%5E3%23t%5EUl4xMF8xOjNFRDgwQ0UwMTAyMkE3Rjc5Njk3Qzg3RjJBQkE5MzQ3XzJfMSNFXjI2MA"
    headers = {
        "Content-Language": "en-US",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic RGFuaWVsTGktdGVzdGluZy1QUkQtYzU4M2UwNDAyLTA1ZmVjMDZjOlBSRC01ODNlMDQwMmUxZjUtMWI2YS00ZjEzLTg4ZmMtMDVjNw=="
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    response_text = json.loads(response.text)
    access_token = response_text["access_token"]
    return access_token