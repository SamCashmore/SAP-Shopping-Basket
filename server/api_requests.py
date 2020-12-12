from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session
import base64
import requests
import json

'''
File getting data from API using OAuth2 authentication
https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html
'''

def auth():
    '''
    OAuth2 authentication - gets tokens using hard-coded ids and keys
    Returns access token
    '''

    client_id = 'sb-dd3064df-4097-411b-b32d-8cf83284e7fb!b59789|customer-order-sourcing-trial!b20218'
    client_secret = '36tXSJFZFL9WvpQEx0Xtcz8Tjzg='

    access_token_url = 'https://tc.authentication.eu10.hana.ondemand.com/oauth/token'


    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    return oauth.fetch_token(token_url=access_token_url, client_id=client_id, client_secret=client_secret)



def get_quantity_from_api(product_id):
    '''
    Product_Id can be list of ids of one value
    '''

    client_id = 'sb-dd3064df-4097-411b-b32d-8cf83284e7fb!b59789|customer-order-sourcing-trial!b20218'

    base_url = 'https://cpfs-dtrt-trial.cfapps.eu10.hana.ondemand.com/v1'
    extension_url = '/availableToSell'
    url = base_url + extension_url

    token = auth()

    client = OAuth2Session(client_id, token=token)
    # r = client.get(url)
    headers = {"Content-Type": "application/json"}

    # if isinstance(product_id, list):
    #     # List of ids
    #     ids = []
    #     for Id in product_id:
    #         ids.append({"productId": Id})
    #     body = {
    #         "items": ids
    #     }
    # else:
    #     # Individual Id
    body = {
        "items": [
            {
            "productId": product_id
            }
        ]
    }
    r = client.post(url, data=json.dumps(body), headers=headers)

    data = r.json()
    return int(data[0]['quantity'])


# print(get_quantity_from_api("DYSON-248F-TORQUE-IR"))