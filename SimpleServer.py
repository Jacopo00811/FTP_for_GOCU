import os
import hashlib
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class MyFTPHandler(FTPHandler):
    def pre_process_command(self, line, cmd, arg):
        # Override pre_process_command to handle the MD5 command
        if cmd.upper() == 'MD5':
            self.ftp_MD5(arg)
            return

        # Call the parent class method for other commands
        super().pre_process_command(line, cmd, arg)

    def ftp_MD5(self, arg):
        splitted = arg.split(' ')
        received_md5_checksum, last_file_name = splitted[0], splitted[1]
        try:
            with open(last_file_name, 'rb') as f:
                file_content = f.read()
            md5_checksum = hashlib.sha256(file_content).hexdigest()

            # Calculate MD5 checksum of the received file content
            if md5_checksum == received_md5_checksum:
                self.respond_w_warning("250 MD5 checksum matched. File received correctly.")
                print("\nThe checksums match!\n")              
            else:
                self.respond_w_warning("550 MD5 checksum mismatch. File may be corrupted.")
                print("\nThe checksums do not match!\n")                
                os.remove(last_file_name)  # Remove the corrupted file
        except Exception as e:
            self.respond_w_warning("550 Error handling MD5 command: {}".format(e))


class MyFTP_Server:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.authorizer = DummyAuthorizer()
        self.handler = MyFTPHandler
        self.server = None

    def run_server(self):
        try:
            self.authorizer.add_user('Jacopo', 'pippetto', '.', perm='elradfmwMT')
            self.authorizer.add_anonymous(os.getcwd())

            self.handler.authorizer = self.authorizer
            self.handler.banner = "Hi there! Welcome to Jacopo's FTP server"

            self.server = FTPServer((self.address, self.port), self.handler)

            # set a limit for connections
            self.server.max_cons = 256
            self.server.max_cons_per_ip = 5

            print(f"Starting FTP server on {self.address}:{self.port}")
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("Ctrl+C detected. Shutting down the FTP server.")
            if self.server:
                self.server.close_all()

def main():
    ftp_server = MyFTP_Server('172.20.10.2', 2121)
    ftp_server.run_server()

if __name__ == '__main__':
    main()
