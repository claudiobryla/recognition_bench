# Recognition Bench
Recognition Bench is a quick tool that can be used to compare the results of popular image recognition services. It allows any developer to compare image recognition services without the overhead of having to learn each service's API and it also provides a simple web interface for uploading and classifying images so that anyone with a web browser can use it.

### Background
A recent project required me to classify a large number of images within a specific domain. I was getting mixed results between services and wanted to see who could provide us the results we were expecting most consistently. I developed this tool as a quick and simple way to compare all of the services without having to upload and record the results multiple times.

If you're facing a similar problem, you should be able to leverage this tool to help you make a decision on an image classification service.

The source code of this tool also provides an example of how to make use of the Python SDKs for a number of image recognition services.

### Requirements
* Python 3

### Installation
These instructions will walk you through running the app in dev mode.
1. Set your current path to the project: ```cd /path/to/recognition_bench```
2. Set up your virtual environment: ```python3 -m venv env``` 
3. Install dependencies ```env/bin/pip install --upgrade pip setuptools pyramid boto3 requests clarifai google-cloud-vision watson_developer_cloud```
4. Install the project ```env/bin/python setup.py develop```
4. Copy the config sample ```cp config.ini.sample config.ini```
5. Set ```enabled=true``` for all of the services you'll want to test.
6. You'll need to obtain API keys for each of the services you want to use* (most of these services offer a free trial). You can find the instructions on how to obtain these keys below: 
	* Amazon Rekognition: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey
	* Microsoft Azure: https://azure.microsoft.com/en-ca/try/cognitive-services/?api=computer-vision
	* Clarifai: https://clarifai.com/developer/guide/authentication#authentication
	* Google Vision: https://cloud.google.com/vision/docs/libraries (see "Setting Up Authentication")
	* IBM Watson: https://www.ibm.com/support/knowledgecenter/en/SS3UMF/dch/admin/apikey_auth_admin.html
7. Fill out the API credentials for all of the services you have enabled. Additionally, you can either leave the additional configurations as their defaults or change them (a few services allow for additional arguments when making requests).
8. Start the app ```env/bin/pserve development.ini```
9. Once everything is running, head to http://localhost:6543/ and drop an image into the uploader.

### Project Information
* This project is built using Pyramid.

* ```recognition_bench/views/services/```: Contains the API logic for each service. When possible, we make use of the SDK provided by the service. These files include three methods: the constructor, classify and __normalize_labels. The constructor sets up the API (usually intializes an SDK with credentials), ```classify``` makes the request, and ```__normalize_labels``` parses the results and returns them in a consistent data structure. 

* ```views/classify```: Provides the /classify endpoint and passes an image file to each service.

* ```views/upload.py```: Renders the default web interface.

* You can create your own interface by making a POST request to /classify.

### Todos
* Multi-file upload support
* Improve error handling
* Add tests
* Simplify installation process
* Support for more services

### License
Copyright (c) 2018, Claudio Bryla
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.