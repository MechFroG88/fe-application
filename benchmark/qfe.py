import time
import random
from mife.single.quadratic.ddh import FeDDH

timearr = []

def run(n):
    generate = []
    encrypt = []
    keygen = []
    decrypt = []
    for _ in range(5):
        x = [random.randint(0, 10) for i in range(n)]
        y = [random.randint(0, 10) for i in range(n)]

        f = [[random.randint(0, 10) for i in range(n) ] for j in range(n)]

        start = time.time()
        key = FeDDH.generate(n)
        end = time.time()
        generate.append(end-start)

        start = time.time()
        c = FeDDH.encrypt(x, y, key)
        end = time.time()
        encrypt.append(end-start)

        start = time.time()
        sk = FeDDH.keygen(f, key)
        end = time.time()
        keygen.append(end-start)

        start = time.time()
        m = FeDDH.decrypt(c, key.get_public_key(), sk, (0, 1000 * n**2))
        end = time.time()
        decrypt.append(end-start)

        expected = 0
        for i in range(n):
            for j in range(n):
                expected += f[i][j] * x[i] * y[j]


        assert m == expected
    timearr.append([sum(generate) / len(generate), sum(encrypt)/ len(encrypt), sum(keygen)/len(keygen), sum(decrypt)/len(decrypt)])

n = [2, 3, 5, 7]

for i in n:
    run(i)


print(timearr)