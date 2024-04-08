from mife.multiclient.rom.ddh import FeDDHMultiClient
from helper import recv_until
from parties import n, m, tp, dp
from dill import dumps, loads
import subprocess
import socket
import time

end_marker = b"\n\n\n\n"

def spawn_dp():
    process = []

    for i in range(len(dp)):
        p = subprocess.Popen(['python3', 'dp.py', str(dp[i])])
        process.append(p)
    
    time.sleep(1)
    return process

def start_listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.bind(tp)
            s.listen()
            break
        except OSError:
            continue
    return s

if __name__ == "__main__":
    masterKey = FeDDHMultiClient.generate(n, m)
    dpKey = [masterKey.get_enc_key(i) for i in range(n)]

    try:
        process = spawn_dp()

        for i in range(len(dp)):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', dp[i]))
            s.send(b'enc_key: ' + dumps(dpKey[i]) + end_marker)

        s = start_listen()

        print("Starting trusted party on port", tp[1])
        while True:
            conn, addr = s.accept()
            msg = recv_until(conn, end_marker)
            if (msg.startswith(b"public_key: ")):
                conn.send(dumps(masterKey.get_public_key()) + end_marker)
            elif (msg.startswith(b"get_decrypt_key: ")):
                y = loads(msg[17:])
                conn.send(dumps(FeDDHMultiClient.keygen(y, masterKey)) + end_marker)
            elif (msg.startswith(b"get_decrypt_key_safe: ")):
                tag, y = loads(msg[22:])
                conn.send(dumps(FeDDHMultiClient.keygen_safe(y, masterKey, tag)) + end_marker)

    except Exception as e:
        for p in process:
            p.kill()
        s.close()
        print("Exiting")
        exit(0)



            