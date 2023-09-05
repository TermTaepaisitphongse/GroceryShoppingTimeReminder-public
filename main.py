import requests, json
from personal_info import api_key, home_address, destination_address #local import, personal api key

url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={home_address}&destinations={destination_address}&units=metric&key={api_key}&avoid=tolls"

payload={}
headers = {}

def get_travel_time():
	try:
		response = requests.request("GET", url, headers=headers, data=payload)
		response_text = response.text

		jdata = json.loads(response_text)

		travel_time = jdata['rows'][0]['elements'][0]['duration']['text']
		int_travel_time = int(travel_time[:-4])

		return travel_time, int_travel_time

	except Exception as e:
		print(e)
		print('Google Maps API Failed')
		return None

if __name__ == "__main__":
	print(get_travel_time())