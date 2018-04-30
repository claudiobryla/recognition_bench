import json

from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types

class Google():
	name = 'Google Vision'

	def __init__(self, credentials_path=None, label_key='description', confidence_key='score'):
		credentials = None 
		if (credentials_path): # load credentials if path specified
			credentials = service_account.Credentials.from_service_account_file(credentials_path)

		self.__api = vision.ImageAnnotatorClient(credentials=credentials)

		self.__label_key = label_key
		self.__confidence_key = confidence_key

	def __normalize_labels(self, result):
		labels = result.label_annotations

		normalized_labels = []
		for label in labels:
			normalized_labels.append({
				'name': getattr(label, self.__label_key),
				'confidence': getattr(label, self.__confidence_key)
			})

		return normalized_labels

	def classify(self, image_file):
		image = types.Image(content=image_file)
		result = self.__api.label_detection(image=image)

		return self.__normalize_labels(result)
