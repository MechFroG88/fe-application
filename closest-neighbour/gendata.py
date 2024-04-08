import random 
n = 10
m = 10

dataset = [
    [random.randint(0, 1000) for _ in range(n) ] for _ in range(m)
]

normalized = []

for i, row in enumerate(dataset):
    norm = sum([x**2 for x in row])**0.5
    normalized.append([round(x/norm, 3) for x in row])

print(dataset)
print(normalized)