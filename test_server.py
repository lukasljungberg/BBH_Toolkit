from flask import Flask, Response, send_file, request, abort, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Directory to store files (for this example, just put some sample files here)
BASE_DIR = 'files'
@app.route('/', methods=['GET'])
def index():
    return Response(200)

@app.route('/time', methods=['GET'])
def get_time():
    f = request.args.get('format')
    # Get the current time
    current_time = datetime.now().strftime(f)
    print(current_time)
    return Response(200)
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
    
# Dummy secret key for token validation (You can replace this with actual validation logic)
SECRET_TOKEN = "your_secret_bearer_token"

# Folder where files are expected to be stored
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def token_required(f):
    """Decorator to ensure the request has a valid Bearer token."""
    def wrapper(*args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            abort(401, description="Authorization header missing")

        # Extract the token from the header (format should be "Bearer <token>")
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            abort(401, description="Invalid Authorization header format")

        token = parts[1]

        # Validate token (replace with your actual validation logic)
        if token != SECRET_TOKEN:
            abort(403, description="Forbidden: Invalid token")

        return f(*args, **kwargs)

    return wrapper


@app.route('/upload', methods=['GET'])
@token_required
def upload_file():
    """A vulnerable endpoint that can be exploited for path traversal."""
    filename = request.args.get('filename')  # User provides the filename in the query string
    
    if not filename:
        return jsonify({"error": "Filename is required"}), 400
    
    # WARNING: This is a vulnerable operation
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Open the file without any validation or sanitation
    try:
        with open(filepath, 'r') as file:
            file_content = file.read()
        return jsonify({"file_content": file_content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=4444)
