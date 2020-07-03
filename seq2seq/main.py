from http.server import HTTPServer

from server.server import MyRequestHandler

if __name__ == '__main__':
    server = HTTPServer(("", 1224), MyRequestHandler)
    print("pythonic-simple-http-server started, serving at http://localhost:1224/")
    server.serve_forever()
