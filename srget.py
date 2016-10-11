import sys
import os
from socket import socket,AF_INET,SOCK_STREAM
from urlparse import urlparse

class Downloader():
    def __init__(self):
        self.pathdown = ""
        self.host = ""
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.header = ""
        self.FileName = ""
        self.data = ""
        self.numConn = 5
        self.content_length = 0
        self.port = 80
        self.req_header = ""

    def connect(self):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.connect((self.host,self.port))
        print "Connection Established"

    def send_request(self):
        self.req_header = "GET " + self.pathdown + " HTTP/1.1\r\n" + "Host: " + self.host + "\r\n\r\n"
        self.socket.send(self.req_header)
        print "Sending request header"

    def input_splitter(self,argument):
        self.FileName = argument[2]
        print "Saving the file as: " + self.FileName
        temp = argument[-1]
        url = urlparse(temp)
        self.host = url.hostname
        self.pathdown = url.path

    def recv(self):
        data = ""
        header = ""
        print "Start Receiving file"
        while True:
            print "Loop entering"
            buff = self.socket.recv(1024)
            header += buff
            if "\r\n\r\n" in header:
                print "kao if nhoi si"
                self.header, leftover =   header.split("\r\n\r\n")
                data += leftover
                print self.header
                break
        while True:
            data_buff = self.socket.recv(1024)
            if not data_buff:
                print "exiting loop"
                break
            data += data_buff
        with open((self.FileName), 'wb+') as f:
            f.write(data)
            print "Data is" + data
            f.close()
        self.socket.close()

    # def datasize (self):
    #     header_list = self.header.split("\r\n")
    #     for fields in header_list:
    #         if "Content-Length" in fields:
    #             cl = fields.split(":")[-1]
    #             self.content_length = int(cl)

    # def file_write(self):
    #     if not os.path.exists(self.path):
    #         os.makedirs(self.path)
    #     with open(os.path.join(self.path, self.FileName), 'wb') as f:
    #         f.write(self.data)
    #         f.close()

    def DownExec(self,argument):
        s = Downloader()
        s.input_splitter(argument)
        s.connect()
        s.send_request()
        s.recv()
        s.datasize()
        # s.file_write()

if __name__ == '__main__':
    start = sys.argv
    A = Downloader()
    A.DownExec(start)




# with ()