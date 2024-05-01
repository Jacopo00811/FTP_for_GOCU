from ftplib import FTP

# Replace 'localhost' with the IP address or hostname of your FTP server
# ftp = FTP('localhost')
conn = FTP()
# Replace 'user' and '12345' with the username and password of your FTP server
conn.connect('localhost', 2121)
conn.login('user','12345')

# List the files on the server
print('Files on server:\n')
conn.retrlines('LIST')

filename = 'file.txt'
save_location = 'Res\\'

# Download a file from the server (replace 'filename.txt' with the name of the file you want to download)
with open(save_location + filename, 'wb') as f:
    # Use FTP's retrbinary command to download the file
    conn.retrbinary('RETR ' + filename, f.write)



# # Upload a file to the server (replace 'localfile.txt' with the path to the file you want to upload)
# with open('localfile.txt', 'rb') as f:
#     ftp.storbinary('STOR remotefile.txt', f)

# Close the FTP connection
conn.quit()
