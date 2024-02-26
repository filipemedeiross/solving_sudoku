import numpy as np


N = 9
STEP = 3

V   = np.arange(1, N + 1)

SQR = []
for idx in range(N):
    p = idx // STEP * STEP
    SQR.append((p, p + STEP))
