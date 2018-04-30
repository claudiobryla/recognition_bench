import requests

class Azure():
	name = 'Azure Computer Vision'

	def __init__(self, subscription_key=None, base_url='https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/', label_key='name', confidence_key='confidence'):
		self.__api = requests

		self.__endpoint = base_url + 'analyze'
		self.__headers = {
			'Ocp-Apim-Subscription-Key': subscription_key, 
            'Content-Type': 'application/octet-stream'
		}
		self.__params = {
			'visualFeatures': 'Tags'
		}

		self.__label_key = label_key
		self.__confidence_key = confidence_key

	def __normalize_labels(self, result):
		labels = result['tags']

		normalized_labels = []
		for label in labels:
			normalized_labels.append({
				'name': label[self.__label_key],
				'confidence': label[self.__confidence_key]
			})

		return normalized_labels

	def classify(self, image_file):
		response = self.__api.post(
			self.__endpoint,
			headers = self.__headers,
			params = self.__params,
			data = image_file
		)
		response.raise_for_status()
		result = response.json()

		return self.__normalize_labels(result)