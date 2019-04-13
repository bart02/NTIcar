import socket
import struct
import pickle
import cv2 as cv

clientSocket = socket.socket()

BUFFER_SIZE = 4096

def send_all(msg):
    clientSocket.sendall(struct.pack('>I', len(msg)) + msg)


def recive_all(n):
    data = b''
    while len(data) < n:
        packet = clientSocket.recv(min(n - len(data), BUFFER_SIZE))
        if not packet:
            return None
        data += packet
    return data


def recive_message():
    raw_msglen = recive_all(4)
    if not raw_msglen:
        print("No valid msg")
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    msg = recive_all(msglen)
    return msg


clientSocket.connect(('192.168.1.139', 9090))

cap = cv.VideoCapture(0)

with clientSocket:
    while True:
        ret, frame = cap.read()
        img = cv.resize(frame, (200, 150))
        data = pickle.dumps(img)
        send_all(data)
        print(recive_message())

print('Close')
