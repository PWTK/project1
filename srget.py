import sys
import os
from socket import socket,AF_INET,SOCK_STREAM
from urlparse import urlparse

class Downloader():
    def __init__(self):
        self.ETAG = ""
        self.pathdown = ""
        self.modified_date = ""
        self.rangebyte= 0
        self.host = ""
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.header = ""
        self.file_name = ""
        self.data = ""
        self.numConn = 5
        self.content_length = 0
        self.port = 80
        self.req_header = ""
        self.current_path = os.path.realpath(__file__)
        self.current_byte = ""
        self.resume_field = {}
    def connect(self):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.connect((self.host,self.port))
        print "Connection Established"

    def send_connection_request(self):
        self.req_header = "GET " + self.pathdown + " HTTP/1.1\r\n" + "Host: " + self.host + "\r\n\r\n"
        self.socket.send(self.req_header)
        print "Sending request header"

    def input_splitter(self,argument):
        self.file_name = argument[2]
        print "Saving the file as: " + self.file_name
        temp = argument[-1]
        url = urlparse(temp)
        if url.port != None:
            self.port = url.port
        self.host = url.hostname
        self.pathdown = url.path
    # def meta_write(self):
    #
    # def file_check(self):

    def recv(self):
        data = ""
        header = ""
        while True:
            buff = self.socket.recv(8096)
            header += buff

            if "\r\n\r\n" in header:
                self.header, leftover =   header.split("\r\n\r\n")
                data += leftover
                print "Header Recieved"
                break

        with open((self.file_name), 'wb+') as f, open(("meta.txt") ,'w') as m:

            f.write(leftover)
            if "Content-Length" in self.header:
                self.datasize()
                data_total = len(leftover)
                print self.content_length, data_total
                m.write("etag" + "\r\n")
                m.write("modified" + "\r\n")
                while self.content_length > data_total:
                    data_buff = self.socket.recv(8096)
                    f.write(data_buff)

                    data_total += len(data_buff)
                    print data_total
                    m.write(str(data_total) + "\r\n")
                f.close()
                m.close()
            else:
                print "Server do not support resume"
                print "Start downloading from the beginning "
                total = 0
                while True:
                    data_buff = self.socket.recv(8096)
                    if not data_buff:
                        print "exiting loop"
                        break
                    total += len(data_buff)
                    f.write(data_buff)
                f.close()
                print "Download Complete"
        self.socket.close()
        sys.exit()

    def datasize (self):
        header_list = self.header.split("\r\n")
        for fields in header_list:
            if "Content-Length" in fields:
                cl = fields.split(":")[-1]
                self.content_length = int(cl)

    def resume_head

    def down_execution(self,argument):
        s = Downloader()
        s.input_splitter(argument)
        s.connect()
        s.send_connection_request()
        s.recv()
    #
    # def rename(self):
    #     with open((self.FileName),'wb+') as f:
    #
    # # def get_continue_header(self,argument):
    # #     if "Content-Length" in self.header:
    # #
    # #
    # #     else
    # #
    # # def calRangebyte (self):
    # #
    # # def checkContinuue ()

if __name__ == '__main__':
    start = sys.argv
    A = Downloader()
    A.down_execution(start)

