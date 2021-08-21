import json

import requests

class RoadSafetyModel:
    def __init__(self):
        self.retrieve_data()
        pass

    def train(self):
        pass

    def retrieve_data(self):
        req = requests.get("https://www.data.qld.gov.au/api/3/action/datastore_search?resource_id=e88943c0-5968-4972-a15f-38e120d72ec0")
        if req.status_code != 200:
            print("Failed to get the data from the server")
        else:
            data_text = req.text
            data_json = json.loads(data_text)
            # print(data_json["result"]["fields"])
        pass

if __name__ == "__main__":
    rsm = RoadSafetyModel()