import boto3

class Amazon():
	name = 'Amazon Rekognition'

	def __init__(self, max_labels=100, min_confidence=50, region='us-east-1', access_key=None, secret_key=None, label_key='Name', confidence_key='Confidence'):
		self.__api = boto3.client(
			'rekognition',
			region_name=region,
			aws_access_key_id=access_key,
    		aws_secret_access_key=secret_key,
		)
		
		self.__max_labels = max_labels
		self.__min_confidence = min_confidence

		self.__label_key = label_key
		self.__confidence_key = confidence_key

	def __normalize_labels(self, result):
		labels = result['Labels']

		normalized_labels = []
		for label in labels:
			normalized_labels.append({
				'name': label[self.__label_key],
				'confidence': float(label[self.__confidence_key]) / 100
			});

		return normalized_labels

	def classify(self, image_file):
		result = self.__api.detect_labels(
			Image = {
				'Bytes': image_file,
			},
			MaxLabels = self.__max_labels,
			MinConfidence = self.__min_confidence
		)

		return self.__normalize_labels(result)
