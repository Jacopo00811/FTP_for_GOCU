# FTP_for_GOCU_Trenitalia

## Overview

This repository contains code for facilitating **FTP (File Transfer Protocol)** operations between a server machine GOCU and devices running MicroPython, particularly on **ESP8266** boards. By running the provided **SimpleServer** on the designated server machine, you can enable the FTP server.

## Usage

1. **Set up Server**: Run the **SimpleServer** on the designated server machine. This server will facilitate the **FTP communication** between the server and the client devices.

2. **Prepare the client device**:
   - For **ESP8266** or any other MicroPython compatible board, load the `boot.py` file to enable the internet connection.
   - Load the `main.py` file on the device to initiate the **FTP transfer**.
