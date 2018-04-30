from clarifai.rest import ClarifaiApp

class Clarifai():
	name = 'Clarifai'

	def __init__(self, api_key=None, model='general-v1.3', label_key='name', confidence_key='value'):
		clarifai = ClarifaiApp(api_key=api_key) # initialize
		self.__api = clarifai.models.get(model)

		self.__label_key = label_key
		self.__confidence_key = confidence_key

	def __normalize_labels(self, result):
		labels = result['outputs'][0]['data']['concepts']

		normalized_labels = []
		for label in labels:
			normalized_labels.append({
				'name': label[self.__label_key],
				'confidence': label[self.__confidence_key]
			})

		return normalized_labels

	def classify(self, image_file):
		result = self.__api.predict_by_bytes(image_file)

		return self.__normalize_labels(result)