import json
import requests
import yaml
from fastapi import FastAPI,Request

app = FastAPI()


def get_tokens(authorization_code):

    url = "https://hydra.enkinineveh.space/oauth2/token"

    payload = 
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)



@app.post("/add_claims")
async def hello(request: Request):
    data = await request.body()
    print(data)
    # We can check if client is kubernetes related so we don't confuse ourselves with other clients
    return {
        "session": {
            "access_token": {
                "groups": "system:nodes",
            },
            "id_token": {
                "groups": "system:nodes",
            },
        }
    }


@app.get("/generate_config")
async def generate_config(request: Request):
    with open("kubeconfig.json", "r") as kubeconfig_file:
        config = json.loads(kubeconfig_file) 
        config['users'][0]['auth-provider']['config']['client-id'] = ''
        config['users'][0]['auth-provider']['config']['client-secret'] = ''
        config['users'][0]['auth-provider']['config']['id-token'] = 
        config['users'][0]['auth-provider']['config']['idp-issuer-url'] = 
        config['users'][0]['auth-provider']['config']['refresh-token'] = 

        config['clusters'][0]['cluster']['server'] = ""

        config_yaml = yaml.dump(config)
        return config_yaml