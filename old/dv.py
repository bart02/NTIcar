control(pi, ESC, 1500, STEER, 90)
time.sleep(0.001)
control(pi, ESC, 1400, STEER, 90)
print('stop')
time.sleep(0.1)
control(pi, ESC, 1500, STEER, 90)
time.sleep(0.001)
control(pi, ESC, 1400, STEER, 90)
print('naxad')
time.sleep(5)
control(pi, ESC, 1500, STEER, 90)
print('stop')