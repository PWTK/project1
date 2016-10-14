import sys
import os
from socket import socket,AF_INET,SOCK_STREAM
from urlparse import urlparse

class Downloader():
    def __init__(self):
        self.extension = ""
        self.ETAG = ""
        self.pathdown = ""
        self.last_modified = ""
        self.rangebyte = 0
        self.host = ""
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.header = ""
        self.file_name = ""
        self.leftover = ""
        self.numConn = 5
        self.content_length = 0
        self.port = 80
        self.req_header = ""
        self.current_path = os.path.realpath(__file__)
        self.current_byte = ""
        self.resume_field = {}
        self.file_path = ""

    def connect(self):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.connect((self.host,self.port))
        print "Connection Established"

    def send_connection_request(self):
        self.req_header = "GET " + self.pathdown + " HTTP/1.1\r\n" + "Host: " + self.host + "\r\n\r\n"
        self.socket.send(self.req_header)
        print "Sending request header"

    def input_splitter(self,argument):
        self.file_name , self.extension = argument[2].split(".")
        print "Saving the file as: " + self.file_name + "." + self.extension
        temp = argument[-1]
        url = urlparse(temp)
        if url.port != None:
            self.port = url.port
        self.host = url.hostname
        self.pathdown = url.path

    def get_header(self):
        data = ""
        header = ""
        while True:
            buff = self.socket.recv(8096)
            header += buff

            if "\r\n\r\n" in header:
                self.header, leftover = header.split("\r\n\r\n")
                self.leftover += leftover
                print "Header Recieved"
                break

    def recv(self):
        with open((self.file_name + ".pam"), 'wb+') as f, open((self.file_name + "_meta.txt") ,'w') as m:

            f.write(self.leftover)
            if "Content-Length" in self.header:
                self.head_split()
                data_total = len(self.leftover)
                m.write(self.ETAG + "\r\n")
                m.write(self.last_modified + "\r\n")
                while self.content_length > data_total:
                    data_buff = self.socket.recv(8096)
                    f.write(data_buff)
                    data_total += len(data_buff)
                    # print data_total
                    m.write(str(data_total) + "\r\n")
                f.close()
                os.rename(self.file_name + ".pam",self.file_name + "."+self.extension)
                m.close()
                os.remove(self.file_path+self.file_name + "_meta.txt")
                print "Download Complete"

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
        sys.exit()

    def disconnect(self):
        self.socket.close()
        print "Connection Close"

    def head_split (self):
        header_list = self.header.split("\r\n")
        for fields in header_list:
            if "ETag" in fields:
                self.ETAG = fields.split(":")[-1]
            if "Content-Length" in fields:
                self.content_length = int(fields.split(":")[-1])
                print "con len: ", self.content_length
            if "Last-Modified" in fields:
                # self.last_modified = fields.split(":")[-1]
                lastmod = fields.split("Last-Modified: ")
                print "last mod: ",lastmod
                self.last_modified = lastmod[-1]
                print "self: ", self.last_modified

    def check_continue(self):
        self.file_path = os.path.realpath(__file__).split(__file__)[0]
        return os.path.isfile(self.file_path+self.file_name+".pam")

    def read_file(self):
        file = open((self.file_name + "_meta.txt") ,'r')
        file.read()
        print "file readreadread" + file.read()

    def send_resume_head(self):
        resume_head = "GET " + self.pathdown + " HTTP/1.1\r\n" + "Host: " + self.host + "\r\n" + "Range: bytes=" + self.current_byte + "-" +str(self.content_length) + "\r\n\r\n"
        self.socket.send(resume_head)
    def down_execution(self,argument):
        s = Downloader()
        s.input_splitter(argument)
        if self.check_continue():
            s.connect()
            s.read_file()
            s.send_connection_request()
            if self.content_length == None or self.content_length not in self.header:
                print "Server does not support resuming"
                print "Redownloading the file"
                s.get_header()
                s.recv()
                s.disconnect()
            else:
                s.disconnect()
                s.connect()
                s.readfile()
                s.send_resume_head()
                s.get_header()


        else:
            s.connect()
            s.send_connection_request()
            s.get_header()
            s.recv()
            s.read_file()
            s.disconnect()
    #
    # def rename(self):
    #     with open((self.FileName),'wb+') as f:
    #



if __name__ == '__main__':
    start = sys.argv
    A = Downloader()
    A.down_execution(start)

