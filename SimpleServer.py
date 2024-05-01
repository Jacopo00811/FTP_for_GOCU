import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def run_ftp_server():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only anonymous user (maybe not needed)
    authorizer.add_user('Jacopo', 'pippetto', '.', perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "Hi there! Welcome to Jacopo's FTP server"
    
    # Specify a masquerade address and the range of ports to use for passive connections. Decomment in case you're behind a NAT
    # handler.masquerade_address = '151.25.42.11'
    # handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 172.20.10.2:2121
    address = ('172.20.10.2', 2121)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    try:
        # start ftp server
        while server_running:
            server.serve_forever(timeout=1, handle_exit=True)  # Check for server_running flag every second
    except KeyboardInterrupt:
        print("Ctrl+C detected. Shutting down the FTP server.")
        server.close_all()

def main():
    global server_running
    server_running = True
    run_ftp_server()

if __name__ == '__main__':
    main()
