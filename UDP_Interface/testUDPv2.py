import socket

import numpy
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import time
import pyformulas as pf

import matplotlib.pyplot as plt


class CircularArray:
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.head = 0
        self.tail = 0
        self.is_full = False

    def append(self, value):
        self.buffer[self.tail] = value
        if self.is_full:
            self.head = (self.head + 1) % self.size
        self.tail = (self.tail + 1) % self.size
        if self.tail == self.head:
            self.is_full = True

    def get(self):
        if self.is_empty():
            return []
        if self.tail > self.head:
            return self.buffer[self.head:self.tail]
        else:
            return self.buffer[self.head:] + self.buffer[:self.tail]

    def is_empty(self):
        return not self.is_full and self.head == self.tail

    def __repr__(self):
        return f"CircularArray({self.get()})"


# Function to update the plot
def update_plot(new_y):
    fig.update_traces(y=new_y)
    pio.show(fig)


def cleanString(message):
    values_string = message.split('F')
    matrixOfValues_string = [s.split() for s in values_string]
    cleanedList = [lst for lst in matrixOfValues_string if lst]
    values = np.array(cleanedList)
    # remove_chars = ["\r", "\n", ";"]
    # cleaned_list = []
    # for s in values_string:
    #     for char in remove_chars:
    #         s = s.replace(char, "")
    #     cleaned_list.append(s)
    #     values_string = cleaned_list

    # values_string = [float(item.replace(',', '.')) for item in values_string]

    values = values.astype(float)
    return values


# Define the parameters
local_ip = '0.0.0.0'  # Listen on all available network interfaces
local_port = 61557  # The local port to listen on
buffer_size = 2048  # Maximum buffer size for incoming data

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the local IP and port
udp_socket.bind((local_ip, local_port))

print(f"Listening for UDP data on {local_ip}:{local_port}...")

input("Press Enter to Start acquisition of 10 samples...")
i = 0
baseline = []
while i < 10:
    print(".")
    data, addr = udp_socket.recvfrom(buffer_size)
    received_message = data.decode('utf-8')
    values = cleanString(received_message)
    valuesAVG = np.mean(values, axis=1)
    if len(baseline):
        baseline = np.vstack([baseline, valuesAVG])
    else:
        baseline = valuesAVG
    i = i + 1

baselineAVG = np.mean(baseline, axis=0)

ca = CircularArray(100)
toPlot = []
for k in range(100):
    toPlot = numpy.append(toPlot, 0.01 * k)

fig = plt.figure()

canvas = np.zeros((1000, 1000))
screen = pf.screen(canvas, 'Force')

start = time.time()
index =0
x = np.linspace(0, 1, 100)

while True:
    # Receive data from the remote UDP server (returns data and the sender's address)
    data, addr = udp_socket.recvfrom(buffer_size)

    # Decode the data to a string (assuming UTF-8 encoding)
    received_message = data.decode('utf-8')

    # Print the received string and the sender's address
    # print("Received message: {received_message} from {addr}")

    values_ = cleanString(received_message)
    valuesAVG = np.mean(values_, axis=1)

    normalizedCommand_ = np.abs(valuesAVG - baselineAVG)
    print(normalizedCommand_)
    normalizedCommand = 0.2  # normalizedCommand_[0]
    # print("Force Value:", normalizedCommand)
    ca.append(normalizedCommand)

    toPlot = np.append(toPlot, normalizedCommand)
    toPlot = np.delete(toPlot, 0)

    #new_x =  np.append(new_x, new_x[99]+1)
    #new_x =  np.delete(new_x, 0)
    x=index

    now = time.time() - start
    # y = np.sin(2 * np.pi * x) + np.sin(3 * np.pi * x)
    y = 0.3
    plt.xlim(index-1, index+1)
    plt.ylim(0, 1)
    plt.plot(x, y, c='black')


    fig.canvas.draw()

    image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    screen.update(image)
    index = index+1
