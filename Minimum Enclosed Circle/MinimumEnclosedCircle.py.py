# a randomized algorithm for finding the minimum area circle enclosing a given point set P.
import matplotlib.pyplot as plt
import random
from math import sqrt


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius


def get_circle_3(A, B, C):
    center = get_circle_center(
        B[0] - A[0], B[1] - A[1], C[0] - A[0], C[1] - A[1])
    center[0] += A[0]
    center[1] += A[1]
    return Circle(center, dist(center, A))


def get_circle_center(bx, by, cx, cy):
    B = bx * bx + by * by
    C = cx * cx + cy * cy
    D = bx * cy - by * cx
    return [(cy * B - by * C) / (2 * D),
            (bx * C - cx * B) / (2 * D)]


def dist(a, b):
    return sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))


def is_inside(p, c):
    return dist(c.center, p) <= c.radius

#the idea of the algorithm is to randomly remove a point from the given input set to form a circle equation. once the equation is formed, check if the point which removed is enclosed by the equation or not. if it doesn't then the point must lie on the boundary of the minimum enclosing circle.
def welzl(P, R, n):
    '''
    The base case of the algorithm is when P becomes empty or the size of the set R is equal to 3:
If P is empty, then all the points have been processed.
If |R| = 3, then 3 points have already been found that lie on the circle boundary, and since a circle can be uniquely determined using 3 points only, the recursion can be stopped.
    '''
    if n == 0 or len(R) == 3:
        return get_trivial_circle(R)
#When the algorithm reaches the base case above, it returns the trivial solution for R, being:
    i = random.randrange(0, n)
    p = P[i]
    P[i], P[n-1] = P[n-1], P[i]

    circle = welzl(P, R, n-1) #recursively checking for all the input

    if is_inside(p, circle):
        return circle

    return welzl(P, R+[p], n-1)


def get_circle_2(A, B):
    center = [(A[0] + B[0])/2.0, (A[1] + B[1])/2.0]
    return Circle(center, dist(A, B)/2.0)


def is_valid_circle(c, points):
    for p in points:
        if not is_inside(p, c):
            return False
    return True

#trivial circle
def get_trivial_circle(points):
    if len(points) == 0:
        return Circle((0, 0), 0)
    elif len(points) == 1:
        return Circle(points[0], 0)
    elif len(points) == 2:
        return get_circle_2(points[0], points[1])
    else:
        for i in range(3):
            for j in range(i+1, 3):
                circle = get_circle_2(points[0], points[1])
                if is_valid_circle(circle, points):
                    return circle

        return get_circle_3(points[0], points[1], points[2])


def generate_points(n, limit):
    return [(random.randint(-limit, limit), random.randint(-limit, limit)) for _ in range(n)]


if __name__ == "__main__":
    N = 20
    LIMIT = N*2
    points = generate_points(N, LIMIT)

    circle = welzl(points, [], len(points))
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim((-LIMIT*2, LIMIT*2))
    ax.set_ylim((-LIMIT*2, LIMIT*2))
    ax.scatter(*zip(*points))
    c = plt.Circle(circle.center, circle.radius, fill=False)
    ax.add_artist(c)

    plt.show()


#Complexity is O(N)