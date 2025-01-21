from flask import Flask, request, Response, stream_with_context
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'server_files'
CHUNK_SIZE = 1024 * 1024  # 1MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    filename = request.headers.get('X-Filename')
    if not filename:
        return {'success': False, 'message': 'No filename provided'}, 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(file_path, 'wb') as f:
        while True:
            chunk = request.stream.read(CHUNK_SIZE)
            if len(chunk) == 0:
                break
            f.write(chunk)

    return {'success': True, 'message': f'File {filename} uploaded successfully'}, 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return {'success': False, 'message': 'File not found'}, 404

    def generate():
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    break
                yield chunk

    return Response(stream_with_context(generate()), 
                    headers={'Content-Disposition': f'attachment; filename={filename}'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)