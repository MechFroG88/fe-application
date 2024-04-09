from mife.single.damgard import FeDamgard
from helper import recv_until
from parties import n, dp, coeff_range, error_range
from dill import dumps, loads
from matplotlib import pyplot as plt
import subprocess
import socket
import time
import random
import traceback


end_marker = b"\n\n\n\n"

def spawn_dp():
    process = []

    for i in range(len(dp)):
        p = subprocess.Popen(['python3.11', 'dp.py', str(dp[i])])
        process.append(p)
    
    time.sleep(1)
    return process
    

if __name__ == "__main__":
    epoch = 10
    rate = 0.0001

    try:
        process = spawn_dp()

        public_keys = []
        total_ys = []
        total_xys = []
        ciphertexts = []
        datapoints_lst = []
        
        #For Debug
        actual_xs = [[] for _ in range(len(dp))]
        actual_ys = [[] for _ in range(len(dp))]

        coeff = [random.randrange(0, coeff_range) for _ in range(n)]
        constant = random.randrange(-coeff_range, coeff_range) * 10

        for i in range(len(dp)):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', dp[i]))
            s.send(b"0:" + end_marker)
            msg = recv_until(s, end_marker)
            public_key = loads(msg)

            s.send(b"1:" + end_marker)
            msg = recv_until(s, end_marker)
            ciphertext = loads(msg)

            s.send(b"2:" + end_marker)
            msg = recv_until(s, end_marker)
            total_y = loads(msg)

            s.send(b"3:" + end_marker)
            msg = recv_until(s, end_marker)
            totalxy = loads(msg)

            s.send(b"5:" + end_marker)
            msg = recv_until(s, end_marker)
            xs, ys = loads(msg)

            s.send(b"6:" + end_marker)
            msg = recv_until(s, end_marker)
            datapoints = loads(msg)

            actual_xs[i] = xs
            actual_ys[i] = ys

            public_keys.append(public_key)
            ciphertexts.append(ciphertext)
            total_ys.append(total_y)
            total_xys.append(totalxy)
            datapoints_lst.append(datapoints)

            s.send(b"exit" + end_marker)
            s.close()

        print("Starting Linear Regression")

        for _ in range(epoch):
            rate = rate * 0.5
            for i in range(len(dp)):
                datapoints = datapoints_lst[i]
                predicted_y = []
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('localhost', dp[i]))

                for j in range(datapoints):
                    lst = [0 for _ in range(n * j)] + coeff + [0 for _ in range(n * (datapoints - j - 1))]
                    s.send(b"4:" + dumps(lst) + end_marker)
                    msg = recv_until(s, end_marker)
                    dec_key = loads(msg)
                    maximum = int(max(max(coeff), abs(min(coeff))))
                    y = FeDamgard.decrypt_safe(ciphertexts[i], public_keys[i], dec_key, 
                                               (-2 * coeff_range*maximum * n, 2 * coeff_range*maximum * n))
                    predicted_y.append(y + constant)

                
                maximum = int(max(max(predicted_y), abs(min(predicted_y))))

                print(coeff)

                for j in range(n):
                    lst = [predicted_y[k // n] if (k % n) == j else 0 for k in range(n * datapoints)]
                    s.send(b"4:" + dumps(lst) + end_marker)
                    msg = recv_until(s, end_marker)
                    dec_key = loads(msg)
                    xy = FeDamgard.decrypt_safe(ciphertexts[i], public_keys[i], dec_key, 
                                                (-2 * coeff_range * maximum * datapoints, 2 * coeff_range * maximum * datapoints))
                    coeff[j] -= -2 * rate / datapoints * (total_xys[i][j] - xy)
                    coeff[j] = int(round(coeff[j]))
                print(coeff)

                # print(coeff)

                constant -= -2 * rate / datapoints * (total_ys[i] - sum(predicted_y))
                constant = int(round(constant))

                s.send(b"exit" + end_marker)
                s.close()
        
        print(constant, coeff)

        for p in process:
            p.kill()
            s.close()

        
        # 2D Plot 
        for i in range(len(dp)):
            plt.scatter(actual_xs[i], actual_ys[i])

        # Draw line with coeff and constant
        x = [[i] for i in range(coeff_range)]
        y = [sum([x[i][j] * coeff[j] for j in range(n)]) + constant for i in range(coeff_range)]
        plt.plot(x, y, color='red')
        plt.show()

        # 3D Plot
        # import numpy as np
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')

        # print(actual_xs[i])

        # for i in range(len(dp)):
        #     ax.scatter([actual_xs[i][j * 2] for j in range(datapoints_lst[i])], 
        #                [actual_xs[i][j * 2 + 1]  for j in range(datapoints_lst[i])],
        #                actual_ys[i])

        # ax.plot([0, coeff_range], [0, coeff_range], 
        #         [constant, coeff_range * coeff[0] + coeff_range * coeff[1] + constant])
        # plt.show()


    except Exception as e:
        print(traceback.format_exc())
        for p in process:
            p.kill()
        s.close()
        print("Exiting")



            