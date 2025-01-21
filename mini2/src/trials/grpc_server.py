import grpc
from concurrent import futures
import file_transfer_pb2
import file_transfer_pb2_grpc
import os

CHUNK_SIZE = 1024 * 1024


class FileTransferServicer(file_transfer_pb2_grpc.FileTransferServicer):
    def UploadFile(self, request_iterator, context):
        filename = None
        file_content = b""

        for chunk in request_iterator:
            if not filename:
                filename = chunk.filename
            file_content += chunk.content

        with open(f"server_files/{filename}", "wb") as f:
            f.write(file_content)

        return file_transfer_pb2.UploadStatus(
            success=True, message=f"File {filename} uploaded successfully"
        )

    def DownloadFile(self, request, context):
        filename = request.filename
        file_path = f"server_files/{filename}"

        if not os.path.exists(file_path):
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")

        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield file_transfer_pb2.FileChunk(content=chunk, filename=filename)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_transfer_pb2_grpc.add_FileTransferServicer_to_server(
        FileTransferServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    if not os.path.exists("server_files"):
        os.makedirs("server_files")
    serve()