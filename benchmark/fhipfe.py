import time
import random
from mife.single.fhiding.ddh import FeDDH

timearr = []

def run(n):
    generate = []
    encrypt = []
    keygen = []
    decrypt = []
    for _ in range(5):
        x = [random.randint(-10, 10) for i in range(n)]
        y = [random.randint(-10, 10) for i in range(n)]

        start = time.time()
        key = FeDDH.generate(n)
        end = time.time()
        generate.append(end-start)

        start = time.time()
        c = FeDDH.encrypt(x, key)
        end = time.time()
        encrypt.append(end-start)

        start = time.time()
        sk = FeDDH.keygen(y, key)
        end = time.time()
        keygen.append(end-start)

        start = time.time()
        m = FeDDH.decrypt(c, key.get_public_key(), sk, (-100 * n**2, 100 * n**2))
        end = time.time()
        decrypt.append(end-start)
        expected = sum([a * b for a, b in zip(x, y)])
        assert m == expected
        print(end- start)
    timearr.append([sum(generate) / len(generate), sum(encrypt)/ len(encrypt), sum(keygen)/len(keygen), sum(decrypt)/len(decrypt)])

n = [10, 20, 30, 50]

for i in n:
    run(i)


print(timearr)