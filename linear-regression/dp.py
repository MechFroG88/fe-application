from mife.single.damgard import FeDamgard
from dill import dumps, loads
from parties import n, datapoints, coeff_range, error_range
from helper import recv_until

import sys
import random
import socket

end_marker = b"\n\n\n\n"

def start_listen(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.bind(('localhost', int(port)))
            s.listen()
            break
        except OSError:
            continue
    return s

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) >= 2 else 5000
    s = start_listen(port)
    masterkey = FeDamgard.generate(n * datapoints)
    
    coeff = [random.randrange(0, coeff_range) for _ in range(n)]
    constant = random.randrange(-coeff_range, coeff_range)

    print("Starting data provider on port", port, "\nCoefficients:", coeff, constant)
    xs = []
    ys = []

    for i in range(datapoints):
        x = [random.randrange(0, coeff_range) for _ in range(n)]
        y = sum([x[j] * coeff[j] for j in range(n)]) + random.randrange(-error_range, error_range) + constant
        xs += x
        ys.append(y)

    total_xy_lst = []
    for i in range(n):
        total_xy = 0
        for j in range(datapoints):
            total_xy += xs[j * n + i] * ys[j]
        total_xy_lst.append(total_xy)

    c = FeDamgard.encrypt(xs, masterkey)
    total_y = sum(ys)
    
    while True:
        conn, addr = s.accept()
        while True:
            msg = recv_until(conn, end_marker)
            if (msg.startswith(b"0:")): # Public Key
                conn.send(dumps(masterkey.get_public_key()) + end_marker)
            if (msg.startswith(b"1:")): # Ciphertext
                conn.send(dumps(c) + end_marker)
            if (msg.startswith(b"2:")): # Total y
                conn.send(dumps(total_y) + end_marker)
            if (msg.startswith(b"3:")): # Total xy
                conn.send(dumps(total_xy_lst) + end_marker)
            if (msg.startswith(b"4:")): # Decryption Key
                function_vector = loads(msg[2:])
                dk = FeDamgard.keygen_safe(function_vector, masterkey, c)
                conn.send(dumps(dk) + end_marker)
            if (msg.startswith(b"5:")): # Datapoints for debug
                conn.send(dumps((xs, ys)) + end_marker)
            if (msg.startswith(b"6:")): # Number of datapoints
                conn.send(dumps(datapoints) + end_marker)
            if (msg.startswith(b"exit")):
                conn.close()
                break
                


