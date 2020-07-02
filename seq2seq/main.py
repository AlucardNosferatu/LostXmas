from http.server import HTTPServer

from infer.infer_seq2seq import loop_talking
from server.server import MyRequestHandler

if __name__ == '__main__':
    # loop_talking(BaseDir='')
    server = HTTPServer(("", 1224), MyRequestHandler)
    print("pythonic-simple-http-server started, serving at http://localhost:1224/")
    server.serve_forever()
