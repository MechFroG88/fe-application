from mife.multiclient.rom.ddh import FeDDHMultiClient
from dill import dumps, loads
from parties import m, tp
from Crypto.Util.number import bytes_to_long
from hashlib import shake_256
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

class DP:
    def __init__(self, key, val_max):
        self.key = key
        self.val_max = val_max
        self.val = 0
        self.psi_val = {}

    def bit_setVal(self, id, tag):
        rand_val = shake_256(tag + str(id).encode()).digest(self.val_max.bit_length())
        self.val = bytes_to_long(rand_val) % self.val_max

    def bit_parseVal(self):
        return [1 if i == self.val else 0 for i in range(self.val_max)]

    def bit_encrypt(self, tag):
        data = self.bit_parseVal()
        return FeDDHMultiClient.encrypt(data, tag, self.key)
    
    def psi_setVal(self, id, tag):
        self.psi_val = {}
        for i in range(self.val_max):
            rand_val = shake_256(f'psi{i}-'.encode() + tag + str(id).encode()).digest(self.val_max.bit_length())
            if (bytes_to_long(rand_val) % 2):
                self.psi_val[i] = 1
    
    def psi_parseVal(self):
        return [0 if i in self.psi_val else random.randrange(-10000, 10000) for i in range(self.val_max)]
    
    def psi_encrypt(self, tag):
        data = self.psi_parseVal()
        return FeDDHMultiClient.encrypt(data, tag, self.key)


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) >= 2 else 5000
    s = start_listen(port)

    print("Starting data provider on port", port)
    dp = None

    while True:
        conn, addr = s.accept()
        msg = recv_until(conn, end_marker)
        if (msg.startswith(b"enc_key: ")):
            enc_key = loads(msg[9:])
            dp = DP(enc_key, m)
            print("Received encryption key")
        else:
            if dp is None:
                conn.send(b"Error: No encryption key" + end_marker)
                continue
        if (msg.startswith(b"bit-tag: ")):
            tag = msg[9:]
            dp.bit_setVal(port, tag)
            print(f"DP {port} Value", dp.val)
            c = dumps(dp.bit_encrypt(tag))
            conn.send(c + end_marker)
        if (msg.startswith(b"psi-tag: ")):
            tag = msg[9:]
            dp.psi_setVal(port, tag)
            print(f"DP {port} Value", dp.psi_val)
            c = dumps(dp.psi_encrypt(tag))
            conn.send(c + end_marker)
        
        conn.close()

