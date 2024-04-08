import time
import random
from mife.single.damgard import FeDamgard

# timearr = []

# def run(n):
#     tarr = []
#     for _ in range(10):
#         x = [random.randint(-10, 10) for i in range(n)]
#         y = [random.randint(-10, 10) for i in range(n)]
#         start = time.time()
#         key = FeDamgard.generate(n)
#         c = FeDamgard.encrypt(x, key)
#         sk = FeDamgard.keygen(y, key)
#         m = FeDamgard.decrypt(c, key.get_public_key(), sk, (-100 * n**2, 100 * n**2))
#         end = time.time()
#         print(end-start)
#         tarr.append(end - start)
#         expected = sum([a * b for a, b in zip(x, y)])
#         assert m == expected
#     timearr.append(tarr)

# n = [10, 20, 50, 70, 100, 150, 1000, 10000, 20000]

# for i in n:
#     run(i)


# print(timearr)


generate = []
encrypt = []
keygen = []
decrypt = []

n = 100

for _ in range(2):
    x = [random.randint(-10, 10) for i in range(n)]
    y = [random.randint(-10, 10) for i in range(n)]
    start = time.time()
    key = FeDamgard.generate(n)
    end = time.time()
    generate.append(end-start)

    start = time.time()
    c = FeDamgard.encrypt(x, key)
    end = time.time()
    encrypt.append(end-start)

    start = time.time()
    sk = FeDamgard.keygen(y, key)
    end = time.time()
    keygen.append(end-start)

    start = time.time()
    m = FeDamgard.decrypt(c, key.get_public_key(), sk, (-100 * n**2, 100 * n**2))
    end = time.time()
    decrypt.append(end-start)

    expected = sum([a * b for a, b in zip(x, y)])
    assert m == expected

print("Generate:", sum(generate) / len(generate) * 1000)
print("Encrypt:", sum(encrypt) / len(encrypt) * 1000)
print("KeyGen:", sum(keygen) / len(keygen) * 1000)
print("Decrypt:", sum(decrypt) / len(decrypt) * 1000)

