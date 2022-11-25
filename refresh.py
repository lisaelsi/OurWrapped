from secrets import REFRESH_TOKEN as refresh_token, BASE_64 as base_64
import requests
import json

class Refresh:

    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):
        query = 'https://accounts.spotify.com/api/token'

        response = requests.post(
            query,
            data = {'grant_type':'refresh_token', 'refresh_token':refresh_token},
            headers={'Authorization':'Basic ' + base_64}
        )

        data = response.json()
    
        return data["access_token"]
        print(response.json())

a = Refresh()
a.refresh()