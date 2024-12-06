import socket
import re

def main():
    # Create a server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is running on http://localhost:4221")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Receive the HTTP request
        request_data = client_socket.recv(1024).decode("utf-8")
        print(f"Request data:\n{request_data}")

        # Extract the path and body from the HTTP request
        path, body = extract_path_and_body(request_data)

        # Determine the response based on the path
        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo/"):
            # Extract the dynamic part of the path
            match = re.match(r"/echo/(.+)", path)
            if match:
                echoed_string = match.group(1)
                response_body = echoed_string
                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len(response_body)}\r\n\r\n"
                    f"{response_body}"
                ).encode("utf-8")
            else:
                response = b"HTTP/1.1 404 Not Found\r\n\r\n."
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        # Send the response
        client_socket.sendall(response)
        client_socket.close()  # Close the client socket

def extract_path_and_body(request):
    try:
        # Split the request into headers and body
        headers, _, body = request.partition("\r\n\r\n")
        
        # Extract the first line from the headers
        first_line = headers.split("\r\n")[0]
        
        # Split the first line to get the method, path, and HTTP version
        method, path, _ = first_line.split(" ")

        return path, body  # Return both the path and body
    except Exception as e:
        print(f"Error extracting path and body: {e}")
        return "", ""  # Return empty strings on error


if __name__ == "__main__":
    main()
