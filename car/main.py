from func import *
import threading
import socket
import struct
import pickle
import paho.mqtt.client as mqtt
from graph import find_route
from solve_povor import solve



mapp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
second = False
t = []

def on_connect(_client, userdata, flags, rc):
    print ("Connected with result code "+str(rc))

    client.subscribe("/fromserver/car/7")
    client.publish('/toserver/car/7', 'h', 2)


def on_message(_client, userdata, msg):
    global mapp, second, t
    m = msg.payload
    print(m)
    # if 'l' in m.decode():
    #     print('y')
    if 'l' not in m.decode():
        lastmap = mapp.copy()
        mapp = []
        for e in range(0, len(msg.payload), 2):
            mapp.append([msg.payload[e], msg.payload[e+1]])
        if len(mapp) > len(lastmap):
            mapp = lastmap
    else:
        print(mapp)
        s = m.decode().split('l')
        s, e = list(map(int, s[:2]))
        r = find_route(mapp, s, e)
        t = solve(r)
        print(r, t)
        client.disconnect()


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect('192.168.1.190', 1883, 60)

client.loop_start()




input()
print(t)

input()



clientSocket = socket.socket()

BUFFER_SIZE = 4096
clientSocket.connect(('192.168.1.139', 9090))
tektl = ''

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


def detect_t():
    global totl, clientSocket, tektl
    # model_detector = dlib.simple_object_detector("tld.svm")
    time.sleep(0.5)

    with clientSocket:
        while True:
            img = cv.resize(totl, (200, 150))
            data = pickle.dumps(img)
            send_all(data)
            msg = int(recive_message().decode())
            if msg != 3:
                tektl = msg


def constrain(val, minv, maxv):
    return min(maxv, max(minv, val))




KP = 0.22
KI = 0
KD = 0.17
last = 0
integral = 0

# constants
SIZE = (400, 300)

RECT = np.float32([[0, 299],
                   [399, 299],
                   [399, 0],
                   [0, 0]])

TRAP = np.float32([[0, 299],
                   [399, 299],
                   [320, 200],
                   [80, 200]])
TRAPINT = np.array(TRAP, dtype=np.int32)


cap = cv.VideoCapture(0)

pi, ESC, STEER = setup_gpio()
control(pi, ESC, 1500, STEER, 90)
time.sleep(1)
timeout = 0
l = 0
r = 0
povor = 0

totl = 1

traffic_thread = threading.Thread(target=detect_t, name="Traffic_light_detector", daemon=True)
traffic_thread.start()

tekpovor = 0
while True:
    try:
        ret, frame = cap.read()
        totl = frame.copy()
        # print(totl)
        # print('totl ready')
        img = cv.resize(frame, SIZE)
        binary = binarize(img)

        perspective = trans_perspective(binary, TRAP, RECT, SIZE)

        if detect_stop(perspective):
            # control(pi, ESC, 1500, STEER, 90)
            # time.sleep(0.1)
            # control(pi, ESC, 1400, STEER, 90)
            # time.sleep(0.1)
            #
            # control(pi, ESC, 1500, STEER, 90)
            # time.sleep(0.1)
            # control(pi, ESC, 1400, STEER, 90)
            # print('n')
            # time.sleep(0.4)
            print(tektl)
            if ( tektl == 0 or tektl == 1 ):
                control(pi, ESC, 1500, STEER, 90)
                print('stop')
                while (tektl != 2):
                    ret, frame = cap.read()
                    totl = frame.copy()
            povor = 1
            try:
                print(tekpovor,  t[tekpovor])
                if t[tekpovor] == 'tl':
                    l = 1
                    r = 0
                elif t[tekpovor] == 'tr':
                    l = 0
                    r = 1
                else:
                    l = 0
                    r = 0
                tekpovor += 1
            except IndexError:
                control(pi, ESC, 1500, STEER, 90)
                print('end')
                while True:
                    pass

        left, right = find_left_right(perspective)

        if r and povor:
            control(pi, ESC, 1550, STEER, 90)
            time.sleep(0.6)
            control(pi, ESC, 1550, STEER, 90 - 25)
            time.sleep(1)
            povor = 0
        elif l and povor:
            control(pi, ESC, 1550, STEER, 90)
            time.sleep(0.9)
            control(pi, ESC, 1550, STEER, 90 + 25)
            time.sleep(0.9)
            povor = 0
        else:
            err = 0 - ((left + right) // 2 - 200)
            if abs(right - left) < 100:
                err = last
            # print(err)
            pid = KP * err + KD * (err - last) + KI * integral
            last = err
            integral += err
            integral = constrain(integral, -10, 10)

        control(pi, ESC, 1540, STEER, 90 + pid)
        time.sleep(0.01)

        # if cv.waitKey(1) & 0xFF == ord('q'):
        #     break
    except KeyboardInterrupt:
        control(pi, ESC, 1500, STEER, 90)
        break

# cv.destroyAllWindows()
cap.release()
