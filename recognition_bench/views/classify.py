from pyramid.response import Response
from pyramid.view import (
    view_defaults,
    view_config
)

import os
import configparser
import shutil

# Services
from .services.Amazon import Amazon
from .services.Azure import Azure
from .services.Clarifai import Clarifai
from .services.Google import Google
from .services.Watson import Watson

# Preload Config
config = configparser.ConfigParser()
config.read('config.ini')

@view_defaults(route_name='classify', renderer='json')
class Classify(object):
    def __init__(self, request):
        self.request = request
        self.__config = config

    # call service helper
    def __call_service(self, service, image_file):
        return {
            'service_name': service.name,
            'labels': service.classify(image_file)
        }

    # classify uploaded image
    @view_config(request_method='POST')
    def post(self):
        image = self.request.POST.get('file')
        image_name, image_ext = os.path.splitext(image.filename)
        image_file = image.file.read()

        result = { # include image metadata in our result
            'image_name': image_name,
            'image_extension': image_ext,
            'services': []
        }

        # Amazon
        if (self.__config['amazon']['enabled'] == 'true'): # only classify when service enabled
            result['services'].append( # we're tacking this onto our results object
                self.__call_service( # use our generic helper to call the service
                    Amazon( # intialize our service
                        region = self.__config['amazon']['region'],
                        access_key = self.__config['amazon']['access_key'] or None,
                        secret_key = self.__config['amazon']['secret_key'] or None,
                        max_labels = int(self.__config['amazon']['max_labels']),
                        min_confidence = int(self.__config['amazon']['min_confidence'])
                    ), 
                    image_file # pass the image file over
                )
            )

        # Azure
        if (self.__config['azure']['enabled'] == 'true'):
            result['services'].append(
                self.__call_service(
                    Azure(
                        subscription_key = self.__config['azure']['subscription_key'],
                        base_url = self.__config['azure']['base_url']
                    ), 
                    image_file
                )
            )

        # Clarifai
        if (self.__config['clarifai']['enabled'] == 'true'):
            result['services'].append(
                self.__call_service(
                    Clarifai(
                        api_key = self.__config['clarifai']['api_key'] or None,
                        model = self.__config['clarifai']['model']
                    ), 
                    image_file
                )
            )

        # Google
        if (self.__config['google']['enabled'] == 'true'):
            result['services'].append(
                self.__call_service(
                    Google(
                        credentials_path = self.__config['google']['credentials_path'] or None
                    ), 
                    image_file
                )
            )

        # Watson
        if (self.__config['watson']['enabled'] == 'true'):
            # ToFix: Can't pass image_file directly to Watson, results in "400: No input images"
            # TemporaryFix: Save image to /tmp, read from disk
            temp_image_path = os.path.join('/tmp', image.filename)

            image.file.seek(0)
            with open(temp_image_path, 'wb') as output_image:
                shutil.copyfileobj(image.file, output_image)

            with open(temp_image_path, 'rb') as temp_image_file:
                result['services'].append(
                    self.__call_service(
                        Watson(
                            api_key = self.__config['watson']['api_key'],
                            threshold = self.__config['watson']['threshold'],
                            classifier_ids = self.__config['watson']['classifier_ids'].split(','),
                            version = self.__config['watson']['version']
                        ),
                        temp_image_file
                    )
                )

        return result