from matplotlib import pyplot as plt

n = [10, 50, 100, 200, 500, 1000]


data = [[0.3032508850097656, 0.023482227325439455, 3.9005279541015624e-05, 0.006107425689697266], [0.1928096294403076, 0.023623184204101564, 0.00014882087707519532, 0.009425592422485352], [0.3337375640869141, 0.023453840255737306, 0.0002980232238769531, 0.012230682373046874], [0.2441256046295166, 0.023589235067367553, 0.0005635738372802735, 0.018320178985595702], [0.2407899856567383, 0.023520995140075683, 0.0014001846313476563, 0.037938928604125975], [0.26139492988586427, 0.023486631870269774, 0.0027982234954833985, 0.05982017517089844]]

# plt.plot(n, [x[0] for x in data], marker='o', label='Generate')
plt.plot(n, [x[1] for x in data], marker='o', label='Encrypt')
plt.plot(n, [x[2] for x in data], marker='o', label='Keygen')
plt.plot(n, [x[3] for x in data], marker='o', label='Decrypt')

plt.xlabel('n')
plt.ylabel('Time (s)')
plt.title('Performance of R-MCIPFE')
plt.legend()
plt.show()