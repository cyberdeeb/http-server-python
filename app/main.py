import socket  # noqa: F401

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    if extract_path(server_socket.recv(1024)) == '':
        server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        server_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    


def extract_path(request):
    lines = request.split('\r\n')
    first_line = lines[0]
    method, path, _ = first_line.split(' ')
    return path
    

if __name__ == "__main__":
    main()