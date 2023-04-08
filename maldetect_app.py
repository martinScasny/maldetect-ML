import os
import pefile
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import nn_func

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB
app.config['UPLOAD_FOLDER'] = 'uploads'

def is_pe_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_contents = file.read()
        pe = pefile.PE(data=file_contents, fast_load=True)
        return True
    except pefile.PEFormatError:
        return False

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    if not is_pe_file(file_path):
        os.remove(file_path)
        return jsonify({"error": "Uploaded file is not a valid PE file"}), 400

    prediction_result, hash = nn_func.predict(file_path)
    print(hash)
    return jsonify({"message": "PE file processed successfully", "prediction": prediction_result,
                    "md5": hash[0], "sha": hash[1]}), 200

if __name__ == '__main__':
    app.run(debug=True)
