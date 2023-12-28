import pytest
import requests
from time import sleep
def test_scenario1(api_url_v1):
 response = requests.post(
        api_url_v1+"/tasks",
        headers={"Content-Type":"application/json"},
        json={
        "name":"test",
        "namespace":"default",
        "runtime":"docker",
        "image":"alpine:latest",
        "script":"sleep 10 && echo Hello World!"
        }
    )
 assert  response.status_code == 201

 reponse_data=response.json()

 response = requests.get(
    api_url_v1+"/tasks"+f"/{reponse_data['result']['id']}",
    headers={"Content-Type":"application/json"},
 )

 assert  response.status_code == 200
 reponse_data=response.json()

 assert reponse_data['result']['status'] in {"new","processing"}

 while  reponse_data['result']['status'] == "new":
     sleep(1)
     response = requests.get(
        api_url_v1+"/tasks"+f"/{reponse_data['result']['id']}",
        headers={"Content-Type":"application/json"},
     )
     reponse_data=response.json()
 assert reponse_data['result']['status'] == "processing"
 
 while  reponse_data['result']['status'] == "processing":
     sleep(10)
     response = requests.get(
         api_url_v1+"/tasks"+f"/{reponse_data['result']['id']}",
         headers={"Content-Type":"application/json"},
     )
     reponse_data=response.json() 

 assert reponse_data['result']['status'] == "success"
 assert reponse_data['result']['result'] == "Hello World!\n"
 assert  response.status_code == 200

 