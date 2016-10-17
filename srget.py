import sys
import os
from socket import socket,AF_INET,SOCK_STREAM
from urlparse import urlparse

class Downloader():
    def __init__(self):
        self.file_etag = ""
        self.file_last_modified = ""
        self.current_byte = ""
        self.file_content_length = 0
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
        print self.file_name
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
        with open((self.file_name + ".pam"), 'ab+') as f, open((self.file_name + "_meta.txt") ,'w') as m:

            f.write(self.leftover)
            if "Content-Length" in self.header:
                self.head_split()
                data_total = len(self.leftover)
                m.write(self.ETAG + "\r\n")
                m.write(self.last_modified + "\r\n")
                m.write(str(self.content_length) + "\r\n")
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
                # print "Server do not support resume"
                # print "Start downloading from the beginning "
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
                print self.content_length
                # print "con len: ", self.content_length
            if "Last-Modified" in fields:
                # self.last_modified = fields.split(":")[-1]
                lastmod = fields.split("Last-Modified: ")
                # print "last mod: ",lastmod
                self.last_modified = lastmod[-1]
                # print "self: ", self.last_modified

    def check_continue(self):
        self.file_path = os.path.realpath(__file__).split(__file__)[0]
        return os.path.isfile(self.file_path+self.file_name+".pam")


    def read_file(self):
        with open(self.file_name + "_meta.txt",'r') as f:
            array = []
            for line in f:
                array.append(line.split("\r\n")[0])
            self.file_content_length = array[2].split("r")[0]
            print "hia ni kue", self.file_content_length
            self.current_byte = array[-1]
            self.file_etag = array[0]
            self.file_last_modified = array[1]
    def header_cmp (self):
        # print self.file_last_modified, self.last_modified
        # print self.file_etag, self.ETAG
        # print self.file_content_length, self.content_length
        return self.file_last_modified != self.last_modified or self.file_etag != self.ETAG


    def send_resume_head(self):
        resume_head = "GET " + self.pathdown + " HTTP/1.1\r\n" + "Host: " + self.host + "\r\n" + "Range: bytes=" + self.current_byte + "-" +str(self.content_length) + "\r\n\r\n"
        self.socket.send(resume_head)
    def down_execution(self,argument):
        s = Downloader()
        s.input_splitter(argument)
        print self.check_continue()
        if s.check_continue():
            print "Old file have been found, trying to resume"
            s.connect()
            s.read_file()
            s.send_connection_request()
            s.get_header()
            s.head_split()
            if s.content_length == 0 or s.content_length == None:

                print "Server does not support resuming"
                print "Redownloading the file"
                s.get_header()
                s.recv()
                s.disconnect()
            else:
                print "Resuming download"
                s.disconnect()
                s.connect()
                s.send_resume_head()
                s.get_header()
                s.head_split()

                if s.header_cmp():
                    print "File has been changed, start redownloading"
                    s.connect()
                    s.send_connection_request()
                    s.get_header()
                    s.recv()
                    s.disconnect()
                else:
                    s.recv()
                    s.disconnect()



        else:
            s.connect()
            s.send_connection_request()
            s.get_header()
            s.recv()
            s.disconnect()



if __name__ == '__main__':
    start = sys.argv
    A = Downloader()
    A.down_execution(start)

