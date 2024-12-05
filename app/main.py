import socket

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

        # Extract the path from the HTTP request
        path = extract_path(request_data)

        # Determine the response based on the path
        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        # Send the response
        client_socket.sendall(response)
        client_socket.close()  # Close the client socket

def extract_path(request):
    try:
        # Split the request into lines and extract the first line
        lines = request.split("\r\n")
        first_line = lines[0]

        # Split the first line to get the method, path, and HTTP version
        method, path, _ = first_line.split(" ")
        return path
    except Exception as e:
        print(f"Error extracting path: {e}")
        return ""

if __name__ == "__main__":
    main()
