import requests
import json


class Server:

	def __init__(self, URL):
		self.URL = URL
		self.CLIENT_APP_URL = URL+"server/"

		
	#Done by client
	def auth_client(self, CLIENT_CODE):
		payload = {"CLIENT_CODE": CLIENT_CODE}
		response = requests.post(f"{self.CLIENT_APP_URL}auth_client/", data = payload)
		print(response)
		response_dict = response.json()
		print(response_dict)
		AUTH_ID = response_dict["AUTH_ID"]
		return AUTH_ID


	def get_token(self, AUTH_ID, CLIENT_CODE):
		payload = {"AUTH_ID": AUTH_ID, "CLIENT_CODE": CLIENT_CODE}
		response = requests.post(f"{self.CLIENT_APP_URL}get_token/", data = payload)
		response_dict = response.json()
		AUTH_TOKEN = response_dict["AUTH_TOKEN"]
		return AUTH_TOKEN


	def save_auth(self, AUTH=None, AUTH_ID=None, CLIENT_CODE=None, AUTH_TOKEN=None):
		if AUTH != None: # Json 
			AUTH_DICT = json.loads(AUTH)
			self.AUTH_ID = AUTH_DICT["AUTH_ID"]
			self.CLIENT_CODE = AUTH_DICT["CLIENT_CODE"]
			self.AUTH_TOKEN = AUTH_DICT["AUTH_TOKEN"]
		if AUTH_ID != None:
			self.AUTH_ID = AUTH_ID
		if CLIENT_CODE != None:
			self.CLIENT_CODE = CLIENT_CODE
		if AUTH_TOKEN != None:
			self.AUTH_TOKEN = AUTH_TOKEN


	def get_tasks(self, SCRIPTS_REQUIRED):
		payload = {"AUTH_ID": self.AUTH_ID, "CLIENT_CODE": self.CLIENT_CODE, "AUTH_TOKEN": self.AUTH_TOKEN, "SCRIPTS_REQUIRED": SCRIPTS_REQUIRED}
		response = requests.post(f"{self.CLIENT_APP_URL}get_tasks/", data = payload)
		response = response.json()
		return response["PARAMETER_DICT"], response["ALL_SHEET_VALUES"], response["SCRIPTS"]


	#Done by client and script
	def send_data(self, SCRIPT_NAME, ROW_PARAMETER_DICT, FILES=None, ALL_SHEET_VALUES = ""):
		ROW_PARAMETERS = json.dumps(ROW_PARAMETER_DICT)
		payload = {"AUTH_ID": self.AUTH_ID, "CLIENT_CODE": self.CLIENT_CODE, "AUTH_TOKEN": self.AUTH_TOKEN, "SCRIPT_NAME": SCRIPT_NAME ,"ROW_PARAMETERS": ROW_PARAMETERS, "ALL_SHEET_VALUES": ALL_SHEET_VALUES}
		requests.post(f"{self.CLIENT_APP_URL}send_data/", data = payload)
		

