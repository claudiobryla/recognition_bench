import json

from watson_developer_cloud import VisualRecognitionV3

class Watson():
	name = 'IBM Watson Visual Recognition'

	def __init__(self, api_key=None, threshold='0.1', classifier_ids=['default'], version='2018-03-19', label_key='class', confidence_key='score'):
		self.__api = VisualRecognitionV3(version, api_key=api_key)

		self.__parameters = json.dumps({'threshold': threshold, 'classifier_ids': classifier_ids})
		
		self.__label_key = label_key
		self.__confidence_key = confidence_key

	def __normalize_labels(self, result):
		labels = result['images'][0]['classifiers'][0]['classes']

		normalized_labels = []
		for label in labels:
			normalized_labels.append({
				'name': label[self.__label_key],
				'confidence': label[self.__confidence_key]
			})

		return normalized_labels

	def classify(self, image_file):
		result = self.__api.classify(images_file=image_file, parameters=self.__parameters)

		return self.__normalize_labels(result)