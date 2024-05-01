import time
import ntptime # type: ignore
import socket

UTC_OFFSET = 2*60*60

def set_time():
    try:
        ntptime.settime()
    except:
        print("Error while setting time")
        pass

def query_time():
    try:
        return time.localtime(ntptime.time()+UTC_OFFSET)
    except:
        print("Error while querying time")
        pass


class FTPClient:
    def __init__(self, server, port=21):
        self.server = server
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            sock_addr = socket.getaddrinfo(self.server, self.port)[0][-1]
            print(f"\nTrying to connect to {sock_addr}")
            self.sock.connect(sock_addr)
            print(f"Connected to {self.server}:{self.port}!!")
            print(f"The server response is: {self._receive_response()}") # Visual check for connection
        except Exception as e:
            print(f"Error while connecting to server: {e}")
            pass

    def send_command(self, command):
        self.sock.sendall(command.encode() + b'\r\n')
        return self._receive_response()

    def _receive_response(self):
        response = b''
        while True:
            data = self.sock.recv(4096)
            if not data:
                break
            response += data
            if response.endswith(b'\r\n'):
                break
        return response.decode()

    def login(self, username, password):
        self.send_command('USER {}'.format(username))
        self.send_command('PASS {}'.format(password))

    def quit(self):
        self.send_command('QUIT')
        self.sock.close()

    def ftp_create_directory(self, directory):
        try:
            if self.sock:
                response = self.send_command('MKD {}'.format(directory))
                # print(response)
                if response.startswith('257'):
                    print(f"Directory {directory} created successfully")
                else:
                    print(f"Error creating directory {directory}")
        except Exception as e:
            print("Error creating directory on FTP server:", e)

    def ftp_upload_file(self, local_file_path, remote_file_path):
        try:
            if self.sock:
                response = self.send_command('PASV')  # Request passive mode
                # print(response)
                if response.startswith('227'):
                    # Split the response to get the data port
                    port_parts = response.split('(')[-1].split(')')[0].split(',')
                    # Calculate the port number using the formula (p1 * 256) + p2.
                    data_port = int(port_parts[-2]) * 256 + int(port_parts[-1]) 
                    # print(f"Data port: {data_port}")
                    # print(f"Port parts: {port_parts}")
                    
                    # Connect to the data port
                    data_sock = socket.socket()
                    data_sock.connect((self.server, data_port))
                    
                    # Open the local file for reading
                    with open(local_file_path, 'rb') as f:
                        data = f.read()
                    
                    print(f"Uploading local file {local_file_path} to the server...")
                    # Send the STOR command to store the file
                    self.send_command('STOR {}'.format(remote_file_path))
                    
                    # Send the file data
                    data_sock.sendall(data)
                    data_sock.close()
                    print("File uploaded successfully to FTP server")
                else:
                    print("Error entering passive mode")
        except Exception as e:
            print("Error uploading file to FTP server:", e)

set_time()
actual_time = query_time()
print(f"\nToday is {actual_time[2]}/{actual_time[1]}/{actual_time[0]} and it is {actual_time[3]}:{actual_time[4]}:{actual_time[5]}")

ftp = FTPClient('172.20.10.2', 2121)
ftp.connect()
ftp.login('Jacopo', 'pippetto')
ftp.ftp_create_directory("Test")
ftp.ftp_upload_file("Files/Test.txt", "Test\\file.txt")
ftp.quit()