# Malware Detection App
This repository contains a Flask web application that uses deep learning models for malware detection. The application allows users to upload a Portable Executable (PE) file, which is then analyzed using two different models - one using the Instruction Branches (IB) method and the other using the Ngram method.

## **Models**
The Malware Detection App uses two models for detecting malware in uploaded files:
*	BI model: This model uses the Instruction Branches method along with imports to detect malware. It is accessed via the /bi/upload endpoint.
*	NI model: This model uses the Ngram method along with imports to detect malware. It is accessed via the /ni/upload endpoint.
## **Requirements**
To install the dependencies needed to run this application, run the appropriate setup script for your platform:
*	setup.sh for Linux/MacOS
*	setup.bat for Windows
These scripts will create a virtual environment and install all necessary packages.
### Usage
To start the application, enter virtual enviroment by:

```./Scripts/Activate.ps1``` for windows or ```./Scripts/activate``` for linux.

Then run server application by:

```python maldetect_app.py```
This will start the Flask development server, which will listen for incoming requests on localhost:5000.
## API Endpoints
### POST /bi/upload
### POST /ni/upload
These endpoints accepts a multipart/form-data request with a file upload field named file. The file must be a valid PE file. Upon successful processing, the endpoint will return a JSON response with the following fields:
*	message: A message indicating the success of the request.
*	model: A string indicating that the NI model was used for this request.
*	prediction: Float number in range between 0.0 and 1.0 that represents whether file is malicious (when implementing you can choose k value (0.0-1.0) for in ```prediction > k``` to achieve higher or lover FP FN values) 
*	md5: The MD5 hash of the uploaded file.
*	sha: The SHA-256 hash of the uploaded file.
