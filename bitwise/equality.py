from mife.multiclient.rom.ddh import FeDDHMultiClient
from parties import dp, tp, n, m
from helper import recv_until
from dill import dumps, loads
import socket

end_marker = b"\n\n\n\n"
tag = b'testtag'
targetVal = 0

def get_ciphertexts():
    ciphertexts = []
    for port in dp:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', port))
        s.send(b'bit-tag: ' + tag + end_marker)
        ciphertexts.append(loads(recv_until(s, end_marker)))
    return ciphertexts


def get_public_key():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(tp)
    s.send(b'public_key: ' + end_marker)
    return loads(recv_until(s, end_marker))


def get_decrypt_key_safe(tag):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(tp)
    y = [[1 if i == targetVal else 0 for i in range(m)] for _ in range(n)]
    s.send(b'get_decrypt_key_safe: ' + dumps((tag, y)) + end_marker)
    return loads(recv_until(s, end_marker))

if __name__ == "__main__":
    c = get_ciphertexts()
    pk = get_public_key()
    for i in range(m):
        targetVal = i
        d_key = get_decrypt_key_safe(tag)
        print(f"Value {i} has {FeDDHMultiClient.decrypt_safe(c, pk, d_key, (0, n * m))}")
    

    
