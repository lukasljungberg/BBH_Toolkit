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

    # Sanitize the filename by normalizing the path
    # Construct the full file path
    file_path = os.path.join(BASE_DIR, filename)

    # Normalize the file path to prevent directory traversal
    # This ensures we are working with an absolute path within BASE_DIR
    file_path = os.path.abspath(file_path)

    # Check if the file path is within the allowed BASE_DIR
    #if not file_path.startswith(os.path.abspath(BASE_DIR)):
    #    return abort(403)  # Forbidden: file is outside the allowed directory

    # Check if the file exists
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return abort(404)
    
@app.route('/api/secured', methods=['GET'])
def download_file2():
    # Get the filename from the query string
    filename = request.args.get('filename')

    if not filename:
        return "No filename provided", 400

    # Sanitize the filename by normalizing the path
    # Construct the full file path
    file_path = os.path.join(BASE_DIR, filename)

    # Normalize the file path to prevent directory traversal
    # This ensures we are working with an absolute path within BASE_DIR
    file_path = os.path.abspath(file_path)

    # Check if the file path is within the allowed BASE_DIR
    if not file_path.startswith(os.path.abspath(BASE_DIR)):
        return abort(403)  # Forbidden: file is outside the allowed directory

    # Check if the file exists
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=4444)
