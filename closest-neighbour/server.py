from mife.single.fhiding.ddh import FeDDH
from helper import recv_until
from parties import server
from dill import dumps, loads
import subprocess
import socket
import time

end_marker = b"\n\n\n\n"

def start_listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.bind(server)
            s.listen()
            break
        except OSError:
            continue
    return s

ct = []

if __name__ == "__main__":
    s = start_listen()
    print("Starting authorization server on port", server[1])
    conn, addr = s.accept()
    while True:
        msg = recv_until(conn, end_marker)
        if (msg.startswith(b"ciphertext: ")):
            ct = loads(msg[12:])
            print("Received ciphertext")
        elif (msg.startswith(b"public_key: ")):
            pub_key = loads(msg[12:])
            print("Received public key")
        elif (msg.startswith(b"find_neighbour: ")):
            dy = loads(msg[16:])
            for c in ct:
                res = FeDDH.decrypt(c, pub_key, dy, bound=(0, 10**6))
                if (res >= 10**6 - 1000):
                    conn.send(b"found: " + f"with matching {res/10**6}" + end_marker)
                    break
            else:
                conn.send(b"not found" + end_marker)




            