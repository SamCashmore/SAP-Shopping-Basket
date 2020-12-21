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
    Number of items available to sell
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

def get_coords(postcode):
    '''
    Finds coords from UK postcode
    '''
    base_url = "https://api.postcodes.io/postcodes/"
    url = base_url + postcode
    r = requests.get(url)
    data = r.json()
    if data["status"] == 200:
        longitude = data["result"]["longitude"]
        latitude = data["result"]["latitude"]
        return {
            "latitude": latitude,
            "longitude": longitude
        }
    else:
        return 'Error - invalid postcode'

def get_sourcing(product_id, quantity, postcode):
    '''
    Delivery info on a product
    Use strategyId: "test"
    Returns object: {
              "sourceId": ,
              "sourceType": 
            }
    '''
    client_id = 'sb-dd3064df-4097-411b-b32d-8cf83284e7fb!b59789|customer-order-sourcing-trial!b20218'

    base_url = 'https://cpfs-dtrt-trial.cfapps.eu10.hana.ondemand.com/v1'
    extension_url = '/sourcing'
    url = base_url + extension_url

    token = auth()

    client = OAuth2Session(client_id, token=token)
    headers = {"Content-Type": "application/json"}

    # Calculate coords from postcode - UK only
    coords = get_coords(postcode)
    if isinstance(coords, object):
        pass
    else:
        return coords

    body = {    
        "strategyId": "test",
        "items": [
            {
                "productId": product_id,
                "quantity": quantity
            }
        ],
        "destinationCoordinates": coords
    }
    
    r = client.post(url, data=json.dumps(body), headers=headers)
    data = r.json()
    return data["sourcings"][0][0]["scheduleLine"][0]["source"]

def post_reservation(product_id, quantity, postcode='TW14 8HD'):
    '''
    Use sourcing info to reserve product for 30mins according to API
    Includes default postcode, SAP CHP
    '''
    client_id = 'sb-dd3064df-4097-411b-b32d-8cf83284e7fb!b59789|customer-order-sourcing-trial!b20218'

    base_url = 'https://cpfs-dtrt-trial.cfapps.eu10.hana.ondemand.com/v1'
    extension_url = '/reservations'
    url = base_url + extension_url

    token = auth()

    client = OAuth2Session(client_id, token=token)
    headers = {"Content-Type": "application/json"}

    body = [
        {
            "items": [
                {
                    "productId": product_id,
                    "scheduleLine": [
                        {
                            "quantity": quantity,
                            "source": get_sourcing(product_id, quantity, postcode)
                        }
                    ]
                }
            ]
        }
    ]
    
    r = client.post(url, data=json.dumps(body), headers=headers)
    data = r.json()
    # return 'Product successfully reserved - Details', data
    return {
        'productId': data[0]['items'][0]['productId'],
        'quantity': int(data[0]['items'][0]['scheduleLine'][0]['quantity']),
        'source': {
            'sourceId': data[0]['items'][0]['scheduleLine'][0]['source']['sourceId'],
            'sourceType': data[0]['items'][0]['scheduleLine'][0]['source']['sourceType']
        }
    }

def get_reservations():
    '''
    Use sourcing info to get list of all reservations
    '''
    client_id = 'sb-dd3064df-4097-411b-b32d-8cf83284e7fb!b59789|customer-order-sourcing-trial!b20218'

    base_url = 'https://cpfs-dtrt-trial.cfapps.eu10.hana.ondemand.com/v1'
    extension_url = '/reservations'
    url = base_url + extension_url

    token = auth()

    client = OAuth2Session(client_id, token=token)    
    r = client.get(url)
    data = r.json()

    # This method of rearranging the output by productID can probably be made more efficient

    # Is possible to create 1 reservation for multiple items, but way my app is set up does not allow for this
    # May be worth accounting for it for error handling

    # reservations = {
    #     'dyson...': [
    #         {
    #             'resid': 123,
    #             'source': 'abc',
    #             ...
    #         }
    #     ]
    # }

    reservations = {}

    for reservation in data:
        productId = reservation['items'][0]['productId']
        reservation_details = {
                'reservationId': reservation['reservationId'],
                'quantity': reservation['items'][0]['scheduleLine'][0]['quantity'],
                'sourceId' : reservation['items'][0]['scheduleLine'][0]['source']['sourceId'],
                'sourceType' : reservation['items'][0]['scheduleLine'][0]['source']['sourceType'],
                'reservationTime': reservation['changedAt'],
                'expiryTime': reservation['expiresAt']
            }
        if productId in reservations:
            reservations[productId].append(reservation_details)
        else:
            reservations[productId] = [reservation_details]
    return reservations

# print(json.dumps(get_reservation(), indent=2))

test_data = {
  "DYSON-248F-TORQUE-IR": [
    {
      "reservationId": "4ba8ab91-76d7-4476-bcfe-62feeba3c911",
      "quantity": 1.0,
      "sourceId": "abc123",
      "sourceType": "STORE",
      "reservationTime": "2020-12-15T10:40:26.174Z",
      "expiryTime": "2020-12-22T10:40:26.174Z"
    },
    {
      "reservationId": "cfc999d4-13f0-499d-832e-90e250a36fb7",
      "quantity": 3.0,
      "sourceId": "abc123",
      "sourceType": "STORE",
      "reservationTime": "2020-12-20T18:12:31.606Z",
      "expiryTime": "2020-12-20T18:42:31.606Z"
    },
    {
      "reservationId": "5527cf57-3b70-45e5-916c-3be221e27dbf",
      "quantity": 2.0,
      "sourceId": "abc123",
      "sourceType": "STORE",
      "reservationTime": "2020-12-20T18:12:50.519Z",
      "expiryTime": "2020-12-20T18:42:50.519Z"
    }
  ],
  "2": [
    {
      "reservationId": "4ba8ab91-76d7-4476-bcfe-62feeba3c911",
      "quantity": 1.0,
      "sourceId": "abc123",
      "sourceType": "STORE",
      "reservationTime": "2020-12-15T10:40:26.174Z",
      "expiryTime": "2020-12-22T10:40:26.174Z"
    },
    {
      "reservationId": "cfc999d4-13f0-499d-832e-90e250a36fb7",
      "quantity": 3.0,
      "sourceId": "abc123",
      "sourceType": "STORE",
      "reservationTime": "2020-12-20T18:12:31.606Z",
      "expiryTime": "2020-12-20T18:42:31.606Z"
    },
    {
      "reservationId": "5527cf57-3b70-45e5-916c-3be221e27dbf",
      "quantity": 2.0,
      "sourceId": "abc123",
      "sourceType": "STORE",
      "reservationTime": "2020-12-20T18:12:50.519Z",
      "expiryTime": "2020-12-20T18:42:50.519Z"
    }
  ],
}