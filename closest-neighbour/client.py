from mife.single.fhiding.ddh import FeDDH
from parties import server, n, padded, dataset
from helper import recv_until
from dill import dumps, loads
import socket
import random
import time

end_marker = b"\n\n\n\n"
    
if __name__ == "__main__":
    masterkey = FeDDH.generate(n)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server)
    print("Sent public key")
    s.send(b'public_key: ' + dumps(masterkey.get_public_key()) + end_marker)

    ct = []
    
    for row in padded:
        ct.append(FeDDH.encrypt(row, masterkey))

    print("Sent ciphertext")
    s.send(b'ciphertext: ' + dumps(ct) + end_marker)

    for row in dataset:
        row = [row[i] + random.randint(-2, 2) for i in range(len(row))]
        norm = sum([x**2 for x in row])**0.5
        row = [int(round(x/norm, 3) * 1000) for x in row]
        dy = FeDDH.keygen(row, masterkey)
        s.send(b'find_neighbour: ' + dumps(dy) + end_marker)
        msg = recv_until(s, end_marker)
        print(msg)

