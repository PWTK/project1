import sys
import os
import asyncore
from socket import socket,AF_INET,SOCK_STREAM
from urlparse import urlparse

class Downloader():
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.req_header = ""
        self.pathdown = ""
        self.host = ""
        self.port = 80
        ##connect part
        self.file_name = ""
        self.extension = ""
        self.file_path = os.path.realpath(__file__).split(__file__)[0]
        self.leftover = ""
        ##file
        self.file_content_length = 0
        self.file_etag = ""
        self.file_last_modified = ""
        ##file sidecar

        self.current_byte = ""
        self.header = ""
        self.content_length = 0
        self.current_ETAG = ""
        self.current_last_modified = ""
        self.rangebyte = 0
        ##resume part

        self.numConn = 5
        #simultanouse download


    def connect(self):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.connect((self.host,self.port))
        # print "Connection Established"

    def disconnect(self):
        self.socket.close()
        # print "Connection Close"

    def send_connection_request(self):
        self.req_header = "GET " + self.pathdown + " HTTP/1.1\r\n" + "Host: " + self.host + "\r\n\r\n"
        self.socket.send(self.req_header)
        # print "Sending request header"

    def input_splitter(self, input):
        link = input[-1]
        if input[3] == "-c" and len(input) == 5:
            self.numConn = input[4]
        elif input[3] == "-c":
            self.numConn = 5
        self.file_name, self.extension = input[2].split(".")
        print "The File Is: " + self.file_name + "." + self.extension
        url = urlparse(link)
        if url.port != None:
            self.port = url.port
        self.host = url.hostname
        self.pathdown = url.path

    def get_header(self):
        data = ""
        header = ""
        while True:
            buffer = self.socket.recv(8096)
            header += buffer

            if "\r\n\r\n" in header:
                self.header, leftover = header.split("\r\n\r\n")
                self.leftover += leftover
                # print "Header Recieved"
                break


    def head_split (self):
        header_list = self.header.split("\r\n")
        for fields in header_list:
            if "ETag" in fields:
                self.current_ETAG = fields.split("ETAG:")[-1]
            if "Content-Length" in fields:
                self.content_length = int(fields.split(":")[-1])
                # print "con len: ", self.content_length
            if "Last-Modified" in fields:
                # self.last_modified = fields.split(":")[-1]
                lastmod = fields.split("Last-Modified: ")
                # print "last mod: ",lastmod
                self.current_last_modified = lastmod[-1]
                # print "self: ", self.last_modified

    def download(self,argument):

        if argument == "download":
            with open((self.file_name + ".pam"), 'wb+') as f, open((self.file_name + "_meta.txt") ,'w') as m:
                f.write(self.leftover)
                if "Content-Length" in self.header:
                    self.head_split()
                    data_total = len(self.leftover)
                    m.write(self.current_ETAG + "\r\n")
                    m.write(self.current_last_modified + "\r\n")
                    m.write(str(self.content_length) + "\r\n")

                    while self.content_length > data_total:
                        data_buff = self.socket.recv(8096)
                        f.write(data_buff)
                        data_total += len(data_buff)
                        m.write(str(data_total) + "\r\n")
                    f.close()
                    m.close()
                    os.rename(self.file_name + ".pam", self.file_name + "." + self.extension)
                    os.remove(self.file_path + self.file_name + "_meta.txt")
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
        elif argument == "Resume":
            with open((self.file_name + ".pam"), 'a') as f, open((self.file_name + "_meta.txt"), 'w') as m:
                f.write(self.leftover)
                if "Content-Length" in self.header:
                    data_total = len(self.leftover) + int(self.current_byte)
                    m.write(self.current_ETAG + "\r\n")
                    m.write(self.current_last_modified + "\r\n")
                    m.write(str(self.file_content_length) + "\r\n")

                    while int(self.file_content_length) > data_total:
                        data_buff = self.socket.recv(8096)
                        f.write(data_buff)
                        data_total += len(data_buff)
                        m.write(str(data_total) + "\r\n")
                    print "sedleao"
                    f.close()
                    m.close()
                    os.rename(self.file_name + ".pam",self.file_name + "."+self.extension)
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

    # def download(self,argument):
    #     print "yo"
    #     if argument == "download":
    #         file_con_length = self.content_length
    #         typefile = 'w'
    #         byte_continue = 0
    #     elif argument == "Resume":
    #         file_con_length = self.file_content_length
    #         typefile = 'a'
    #         byte_continue = int(self.current_byte)
    #     with open((self.file_name + ".pam"), typefile) as f, open((self.file_name + "_meta.txt"), "w") as m:
    #         f.write(self.leftover)
    #         if "Content-Length" in self.header:
    #             if argument == "download":
    #                 self.head_split()
    #             data_total = len(self.leftover) + byte_continue
    #             m.write(self.current_ETAG + "\r\n")
    #             m.write(self.current_last_modified + "\r\n")
    #             m.write(str(file_con_length) + "\r\n")
    #
    #             while file_con_length > data_total:
    #                 data_buff = self.socket.recv(8096)
    #                 f.write(data_buff)
    #                 data_total += len(data_buff)
    #                 m.write(str(data_total) + "\r\n")
    #             print "sedleao"
    #             f.close()
    #             m.close()
    #             os.rename(self.file_name + ".pam", self.file_name + "." + self.extension)
    #             os.remove(self.file_path + self.file_name + "_meta.txt")
    #             print "Download Complete"
    #         else:
    #             # print "Server do not support resume"
    #             # print "Start downloading from the beginning "
    #             total = 0
    #             while True:
    #                 data_buff = self.socket.recv(8096)
    #                 if not data_buff:
    #                     print "exiting loop"
    #                     break
    #                 total += len(data_buff)
    #                 f.write(data_buff)
    #         print "Download Complete"
    #         sys.exit()

    def check_continue(self):
        return os.path.isfile(self.file_path+self.file_name+"_meta.txt")


    def read_file(self):
        with open(self.file_name + "_meta.txt",'r') as f:
            array = []
            for line in f:
                array.append(line.split("\r\n")[0])
            self.file_content_length = array[2].split("r")[0]
            self.current_byte = array[-1]
            self.file_etag = array[0]
            self.file_last_modified = array[1]

    def header_cmp (self):

        return self.file_last_modified != self.current_last_modified or self.file_etag != self.current_ETAG or (int(self.file_content_length)-int(self.current_byte)) != self.content_length


    def send_resume_head(self):
        resume_head = "GET "
        resume_head += self.pathdown
        resume_head += " HTTP/1.1\r\n" + "Host: " + self.host
        resume_head += "\r\n" + "Range: bytes=" + self.current_byte
        resume_head += "-" +str(self.file_content_length) + "\r\n\r\n"
        self.socket.send(resume_head)

    def down_execution(self,input):
        s = Downloader()
        s.input_splitter(input)
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
                s.download("download")
                s.disconnect()
                sys.exit()
            else:

                s.disconnect()
                s.connect()
                s.send_resume_head()
                s.get_header()
                s.head_split()
                if  s.header_cmp():
                    print "File has been changed, start redownloading"
                    s.connect()
                    s.send_connection_request()
                    s.get_header()
                    s.download("download")
                    s.disconnect()
                print "Resuming Download"
                s.download("Resume")
                s.disconnect()
                sys.exit()


        else:
            s.connect()
            s.send_connection_request()
            s.get_header()
            s.download("download")
            s.disconnect()




if __name__ == '__main__':
    start = sys.argv
    A = Downloader()
    A.down_execution(start)

