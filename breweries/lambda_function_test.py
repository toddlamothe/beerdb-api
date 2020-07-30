import json
import requests

def lambda_handler(event, context):
    data = {}
    # Pull querystring parameters if they exist, otherwise set values to empty string
    city = event["queryStringParameters"].get('city', '')
    state = event["queryStringParameters"].get('state', '')
    postalCode = event["queryStringParameters"].get('postalCode', '')
    url = buildBreweryDbUrl(city, state, postalCode)
    response = requests.get(url, data=data)
    json_response = json.loads(response.text)
    return {
        'statusCode': 200,
        'headers': { 
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : "true"
        },
        'body': json.dumps(json_response)
    }
def buildBreweryDbUrl(city, state, zip):
    prod_api_key = "f863f0e57fa16b61150837ab7753505f"
    prod_url = "https://api.brewerydb.com/v2/locations/?key=" + prod_api_key
    dev_api_key = "8ee12a2f196eb183914740dbbb5ccfff"
    dev_url = "https://sandbox-api.brewerydb.com/v2/locations/?key=" + dev_api_key
    url = prod_url + \
        "&postalCode=" + zip + "&locality=" + city + "&region=" + state
    print("url = %s" % url)
    return url


# Test lambda function handler
event = {
    "queryStringParameters": {
        "postalCode" : "05401",
        "city" : "Burlington",
        "state" : "Vermont"
    }
}
context = {}
retval_raw = lambda_handler(event, context)
# For some reason the return value from the API is json containing an element ["body"], but 
# that element appears to be a string (not a json object) that must be loaded into a json object using loads.
# whatevs.
ret_val_json = json.loads(retval_raw["body"])
if 'data' in ret_val_json:
    # print(ret_val_json["data"][0]["brewery"]["name"])
    print("%d brewerie(s) returned" % len(ret_val_json["data"]))
    print(ret_val_json["data"])
else:
        print('No breweries found')
