import os
from http.server import HTTPServer

from data.data_tool import get_file_list
from server.server import MyRequestHandler

if __name__ == '__main__':
    file_list = os.listdir('train/check_points/')
    if len(file_list) > 0:
        epoch_list = get_file_list('train/check_points/')
        epoch_last = epoch_list[-1]
    MyRequestHandler.weight_name = epoch_last
    MyRequestHandler.load_weight(MyRequestHandler.weight_name)
    server = HTTPServer(("", 1224), MyRequestHandler)
    print("pythonic-simple-http-server started, serving at http://localhost:1224/")
    server.serve_forever()
