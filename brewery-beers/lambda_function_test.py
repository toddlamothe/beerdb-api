import json
import requests

def lambda_handler(event, context):
    data = {}
    brewery_id = event['pathParameters']['breweryid']
    print("breweryId = %s" % brewery_id)
    url = buildBreweryDbUrl(brewery_id)
    print("url = %s" % url);
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
    
def buildBreweryDbUrl(brewery_key):
    # https://sandbox-api.brewerydb.com/v2/brewery/VEY3Xa/beers/?key=
    prod_api_key = "f863f0e57fa16b61150837ab7753505f"
    prod_url = "https://api.brewerydb.com/v2/brewery/%s/beers/?key=%s" % (brewery_key, prod_api_key)
    print("prod url = %s" % prod_url);
    dev_api_key = "8ee12a2f196eb183914740dbbb5ccfff"
    dev_url = "https://sandbox-api.brewerydb.com/v2/brewery/%s/beers/?key=%s" % (brewery_key, dev_api_key)
    url = prod_url;
    print("url = %s" % url)
    return url

# Test lambda function handler
event = {
    "pathParameters": {
        "breweryid" : "VEY3Xa"
    }
}

context = {}
retval_raw = lambda_handler(event, context)
# For some reason the return value from the API is json containing an element ["body"], but 
# that element appears to be a string (not a json object) that must be loaded into a json object using loads.
# whatevs.
ret_val_json = json.loads(retval_raw["body"])
if 'data' in ret_val_json:
    print("%d brewerie(s) returned" % len(ret_val_json["data"]))
    print(ret_val_json["data"])
else:
        print('No breweries found')
