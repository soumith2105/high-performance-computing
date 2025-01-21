import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
import os
import time

CHUNK_SIZE = 1024 * 1024  # 1MB


def upload_file(stub, filename):
    def chunk_generator():
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield file_transfer_pb2.FileChunk(
                    content=chunk, filename=os.path.basename(filename)
                )

    response = stub.UploadFile(chunk_generator())
    print(f"Upload status: {response.success}")
    print(f"Server message: {response.message}")


def download_file(stub, filename):
    request = file_transfer_pb2.DownloadRequest(filename=filename)
    response_iterator = stub.DownloadFile(request)

    with open(f"downloaded_{filename}", "wb") as f:
        for chunk in response_iterator:
            f.write(chunk.content)

    print(f"File {filename} downloaded successfully")


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = file_transfer_pb2_grpc.FileTransferStub(channel)
        start_time = time.time()
        # Upload a file
        upload_file(stub, "data.zip")

        # Download a file
        download_file(stub, "data.zip")
        print(f"Time taken: {time.time() - start_time:.2f}")


if __name__ == "__main__":
    run()
