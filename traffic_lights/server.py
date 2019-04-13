import pickle
import struct
import cv2 as cv
import dlib
from reco import filereco

model_detector = dlib.simple_object_detector("tld.svm")

BUFFER_SIZE = 4096


def send_all(msg):
    # print("Len:", len(msg))
    clientSocket.sendall(struct.pack('>I', len(msg)) + msg)


def recive_all(n):
    data = b''
    while len(data) < n:
        packet = clientSocket.recv(min(n - len(data), BUFFER_SIZE))
        # print("Receiving packet {}; full data is {}".format(packet, data))
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
    # print("Msglen:", msglen)
    msg = recive_all(msglen)
    # print(msg)
    return msg

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('', 9090))
sock.listen(1)

print('Sock name: {}'.format(sock.getsockname()))

clientSocket, addr = sock.accept()
print('Connected:', addr)

with clientSocket, sock:
    while True:
        all_data = recive_message()

        obj = pickle.loads(all_data)
        cv.imshow('i', obj)

        boxes = model_detector(obj)

        if boxes:
            box = boxes[0]
            (x, y, xb, yb) = [box.left(), box.top(), box.right(), box.bottom()]
            cv.imshow("Frame", obj[y:yb, x:xb])
            color = filereco(obj[y:yb, x:xb])
            print(color)
            send_all(str(color).encode())
        else:
            send_all('3'.encode())

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

print('Close')

cv.destroyAllWindows()
