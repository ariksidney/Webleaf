import json
import requests
from requests import ConnectTimeout


class RestHandler:

    def __init__(self):
        self.endpoint = '/api/v1'

    def get_auth_token(self, ip, port):
        url = 'http://{}:{}{}/new'.format(ip, port, self.endpoint)
        res = requests.post(url)
        return res.json().get('auth_token') if res.status_code == 200 else res.status_code

    def get_status(self, ip, port, token):
        url = 'http://{}:{}{}/{}/state/on'.format(ip, port, self.endpoint, token)
        try:
            res = requests.get(url, timeout=1)
        except ConnectTimeout:
            return 'Unknown'
        return  'On' if res.json().get('value') else 'Off'

    def turn_on(self, ip, port, token):
        url = 'http://{}:{}{}/{}/state'.format(ip, port, self.endpoint, token)
        res = requests.put(url, data=json.dumps({"on": {"value": True}}))
        return res

    def turn_off(self, ip, port, token):
        url = 'http://{}:{}{}/{}/state'.format(ip, port, self.endpoint, token)
        res = requests.put(url, data=json.dumps({"on": {"value": False}}))
        return res

    def get_selected_effect(self, ip, port, token):
        url = 'http://{}:{}{}/{}/effects/select'.format(ip, port, self.endpoint, token)
        return requests.get(url).json()

    def get_all_effects(self, ip, port, token):
        url = 'http://{}:{}{}/{}/effects/effectsList'.format(ip, port, self.endpoint, token)
        return requests.get(url).json()

    def set_effect(self, ip, port, token, effect):
        url = 'http://{}:{}{}/{}/effects'.format(ip, port, self.endpoint, token)
        res = requests.put(url, data=json.dumps({"select": effect}))

    def get_brightness(self, ip, port, token):
        url = 'http://{}:{}{}/{}/state/brightness'.format(ip, port, self.endpoint, token)
        return requests.get(url).json().get('value')

    def set_brightness(self, ip, port, token, brightness):
        url = 'http://{}:{}{}/{}/state'.format(ip, port, self.endpoint, token)
        res = requests.put(url, data=json.dumps({"brightness" : {"value": int(brightness)}}))
