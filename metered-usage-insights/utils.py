import requests

NODE_IP = '54.177.249.42'
NODE_PORT = '8000'

def get_resource_types(client_id=None):
	url = f'http://{NODE_IP}:{NODE_PORT}/metricsql/resource-types'
	res = requests.get(url).json()

	return res
