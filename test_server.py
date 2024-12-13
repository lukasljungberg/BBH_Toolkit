from flask import Flask, send_file, request, abort
import os

app = Flask(__name__)

# Directory to store files (for this example, just put some sample files here)
BASE_DIR = 'files'

@app.route('/api', methods=['GET'])
def download_file():
    # Get the filename from the query string
    filename = request.args.get('filename')

    if not filename:
        return "No filename provided", 400

    # Construct the full file path (without sanitization)
    file_path = os.path.join(BASE_DIR, filename)
    print(file_path)
    # Check if the file exists, but no sanitization is performed here
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=4444)
