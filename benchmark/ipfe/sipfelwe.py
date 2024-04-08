import time
import random
from mife.single.selective.lwe import FeLWE

# timearr = []

# def run(n):
#     tarr = []
#     for _ in range(10):
#         x = [random.randint(-10, 10) for i in range(n)]
#         y = [random.randint(-10, 10) for i in range(n)]
#         start = time.time()
#         key = FeLWE.generate(n, 4, 4)
#         c = FeLWE.encrypt(x, key)
#         sk = FeLWE.keygen(y, key)
#         m = FeLWE.decrypt(c, key.get_public_key(), sk)
#         end = time.time()
#         print(end-start)
#         tarr.append(end - start)
#         expected = sum([a * b for a, b in zip(x, y)])
#         assert m == expected
#     timearr.append(tarr)

# n = [10, 20, 50, 70, 100, 150]

# for i in n:
#     run(i)

# print(timearr)

generate = []
encrypt = []
keygen = []
decrypt = []

n = 100

for _ in range(10):
    x = [random.randint(-10, 10) for i in range(n)]
    y = [random.randint(-10, 10) for i in range(n)]

    start = time.time()
    key = FeLWE.generate(n, 4, 4)
    end = time.time()
    generate.append(end-start)

    start = time.time()
    c = FeLWE.encrypt(x, key)
    end = time.time()
    encrypt.append(end-start)

    start = time.time()
    sk = FeLWE.keygen(y, key)
    end = time.time()
    keygen.append(end-start)

    start = time.time()
    m = FeLWE.decrypt(c, key.get_public_key(), sk)
    end = time.time()
    decrypt.append(end-start)

    expected = sum([a * b for a, b in zip(x, y)])
    assert m == expected

print("Generate:", sum(generate) / len(generate) * 1000)
print("Encrypt:", sum(encrypt) / len(encrypt) * 1000)
print("KeyGen:", sum(keygen) / len(keygen) * 1000)
print("Decrypt:", sum(decrypt) / len(decrypt) * 1000)

