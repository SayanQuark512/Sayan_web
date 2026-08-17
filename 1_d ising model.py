import numpy as np
import matplotlib.pyplot as plt

N = 50
J = 1
npt = 1000

T_values = range(1, 201)
average_energy = []

for T in T_values:
    s = np.random.choice([-1, 1], N)
    En = []

    for t in range(npt):
        i = np.random.randint(N)
        L = s[(i-1) % N]
        R = s[(i+1) % N]

        dE = 2 * J * s[i] * (L + R)

        if dE <= 0:
            s[i] = -s[i]

        elif np.random.rand() < np.exp(-dE / T):
            s[i] = -s[i]

        E = 0
        for j in range(N):
            E = E - J * s[j] * s[(j+1) % N]

        En.append(E)

    average_energy.append(np.mean(En))

plt.plot(T_values, average_energy, label="Average Energy")
plt.xlabel("Temperature (T)")
plt.ylabel("Average Energy")

plt.show()
