import requests
import os
import time

CHUNK_SIZE = 1024 * 1024  # 1MB


def upload_file(filename):
    url = "http://127.0.0.1:5000/upload"
    file_size = os.path.getsize(filename)

    headers = {
        "X-Filename": os.path.basename(filename),
        "Content-Type": "application/octet-stream",
        "Content-Length": str(file_size),
    }

    with open(filename, "rb") as f:
        response = requests.post(url, data=f, headers=headers, stream=True)

    print(f"Upload status: {response.json()['success']}")
    print(f"Server message: {response.json()['message']}")


def download_file(filename):
    url = f"http://127.0.0.1:5000/download/{filename}"
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(f"downloaded_{filename}", "wb") as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        print(f"File {filename} downloaded successfully")
    else:
        print(f"Error downloading file: {response.json()['message']}")


def run():
    start_time = time.time()
    # Upload a file
    upload_file("data.zip")

    # Download a file
    download_file("data.zip")

    print(f"Time taken: {time.time() - start_time:.2f}")


if __name__ == "__main__":
    run()
