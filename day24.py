import numpy as np
import scipy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def checkBoundedXY(p1, v1, p2, v2, lower, upper):
    a = np.array([[v1[0], -v2[0]], [v1[1], -v2[1]]])
    b = np.array([p2[0]-p1[0], p2[1]-p1[1]])
    ans = None
    try:
        ans = np.linalg.solve(a, b)
    except:
        return False
    if np.min(ans) < 0.0:
        return False
    col = (p1+ans[0]*v1)
    if col[0] < lower or col[0] > upper or col[1] < lower or col[1] > upper:
        return False
    return True

def plot(hailstones):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    positions = np.squeeze(hailstones[:,0:1,:]).astype(np.float64)
    x, y, z = positions[:,0], positions[:, 1], positions[:, 2]
    ax.scatter(x, y, z, c="r", marker='o')
    plt.show()

def hailMary(hailstones):
    p1 = hailstones[0][0]
    v1 = hailstones[0][1]
    
    p2 = hailstones[1][0]
    v2 = hailstones[1][1]
    
    p3 = hailstones[2][0]
    v3 = hailstones[2][1]
    
    print
    print(p1)
    
def check(hailstones):
    idx = 2
    x0 = np.array([181540669791004, 404991404832784, 214854400593114])
    print("sum", np.sum(x0))
    v = np.array([136, -237, 110])
    p1 = hailstones[idx][0]
    v1 = hailstones[idx][1]
    t = (p1[0] - x0[0])/(v[0]-v1[0])
    expected = x0 + t*v
    actual = p1 + t*v1
    print("check", t)
    print("exp", expected)
    print("act", actual)
    print("dif", expected-actual)
    
def hailMary(hailstones):
    # unknowns px py pz, vx vy vz, t1 ... tn
    print(hailstones.shape)
    hailstones = hailstones[0:8,:,:]
    def equation(inVars):
        inP = np.array(inVars[0:3], dtype=np.float128)
        inV = np.array(inVars[3:6], dtype=np.float128)
        #inV = np.array([136, -237, 110], dtype=np.float128)
        t = inVars[3:]
        rockPos = inP+np.expand_dims(t,axis=1)*np.tile(inV, (len(t), 1))
        positions = np.squeeze(hailstones[:,0:1,:])
        velocities = np.expand_dims(t,axis=1)*np.squeeze(hailstones[:,1:2,:])
        hailPos = positions + velocities
        dif = hailPos - rockPos
        res = np.diag(np.dot(dif, dif.T))
        res1 = np.sum(res)
        return res1
    origHS = hailstones.copy()
    
    method = "Powell"
    options = {"maxiter": 1000000, "ftol": 1e-31, "xtol": 1.0e-11}
    # 181540669791003.78833 404991404832783.75986 214854400593114.29164
    initialGuess = np.array([181540669791004,404991404832785,214854400593114] + [1]*(hailstones.shape[0]), dtype=np.float128)
    solve = scipy.optimize.minimize(equation, initialGuess, method=method, options=options)
    print(solve)
    
    np.set_printoptions(suppress=True)
    np.set_printoptions(precision=20)
    
    resPos = solve.x[0:3]
    resVel = solve.x[3:6]
    print("min time", np.min(solve.x[6:]))
    print("stone position", resPos[0], resPos[1], resPos[2])
    #print("stone velocity", resVel[0], resVel[1], resVel[2])
    print(np.sum((solve.x[0:3])))
    
    hailstones = origHS
    mvars = [resPos[0], resPos[1], resPos[2], resVel[0], resVel[1], resVel[2]]
    minput = np.array(mvars + solve.x[6:].tolist(), dtype=np.float128)
    print("minput", minput)
    print("test", equation(minput))
    

with open("input24") as f:
    data = [[[int(nr) for nr in part.split(", ")] for part in line.split(" @ ")] for line in f.read().splitlines()]
    arr = np.array(data)
    pairs = [(idx, idx2) for idx in range(len(arr)) for idx2 in range(idx+1, len(arr))]
    #print(pairs)
    
    sample = False
    
    if not sample:
        lower = 200000000000000
        upper = 400000000000000
    else:
        lower = 7
        upper = 27
    
    results = []
    for i1, i2 in pairs:
        v1 = arr[i1][1]
        v2 = arr[i2][1]
        p1 = arr[i1][0]
        p2 = arr[i2][0]
        results.append(checkBoundedXY(p1, v1, p2, v2, lower, upper))
    print("part1", sum(results))
    
    p1 = arr[0][0]
    v1 = arr[0][1]
    #print("p0", p0)
    
    arr = arr.astype(np.float128)
    hailMary(arr)
    check(arr)
