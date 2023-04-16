import os
import pefile
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from modules import nn_func

upload_folder = 'uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
    
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB
app.config['UPLOAD_FOLDER'] = upload_folder

def is_pe_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_contents = file.read()
        pe = pefile.PE(data=file_contents, fast_load=True)
        return True
    except pefile.PEFormatError:
        return False

def process_file(file, model):
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    if not is_pe_file(file_path):
        os.remove(file_path)
        return jsonify({"error": "Uploaded file is not a valid PE file"}), 400

    prediction_result, hash = nn_func.predict(file_path, model=model)
    used_model = "NI" if not model else "BI"
    return jsonify({"message": "PE file processed successfully", "model": used_model, "prediction": prediction_result,
                    "md5": hash[0], "sha": hash[1]}), 200

@app.route('/ni/upload', methods=['POST'])
def upload_file_ni():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    return process_file(file, model=0)

@app.route('/bi/upload', methods=['POST'])
def upload_file_bi():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    return process_file(file, model=1)

if __name__ == '__main__':
    app.run(debug=True)
