import time
import random
from mife.multiclient.rom.ddh import FeDDHMultiClient

timearr = []

def run(n):
    generate = []
    encrypt = []
    keygen = []
    decrypt = []
    for _ in range(5):
        m = 10
        x = [[random.randint(-10, 10) for j in range(m)] for i in range(n)]
        y = [[random.randint(-10, 10) for j in range(m)] for i in range(n)]

        tag = b'helloworld'

        start = time.time()
        key = FeDDHMultiClient.generate(n, m)
        end = time.time()
        generate.append(end-start)

        start = time.time()
        cs = [FeDDHMultiClient.encrypt(x[i], tag, key.get_enc_key(i)) for i in range(n)]
        end = time.time()
        encrypt.append((end-start) / n)

        start = time.time()
        sk = FeDDHMultiClient.keygen(y, key)
        end = time.time()
        keygen.append(end-start)

        start = time.time()
        m = FeDDHMultiClient.decrypt(cs, tag, key.get_public_key(), sk, (-200 * n*m, 200 * n*m))
        end = time.time()
        decrypt.append(end-start)

        expected = 0
        for i in range(n):
            expected += sum([a * b for a, b in zip(x[i], y[i])])

        assert m == expected
        print(end - start)
    timearr.append([sum(generate) / len(generate), sum(encrypt)/ len(encrypt), sum(keygen)/len(keygen), sum(decrypt)/len(decrypt)])

n = [10, 50, 100, 200, 500, 1000]

for i in n:
    run(i)


print(timearr)