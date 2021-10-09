import socket
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return 'Welcome to the CSC2031 Blog!'


if __name__ == '__main__':
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    app.run(host=my_host, port=free_port, debug=True)
