import random
import math
import matplotlib.pyplot as plt


class AVLTree:

    class AVLNode:
        def __init__(self, data):
            self.data = data
            self.left = None
            self.right = None
            self.height = 1

        def __str__(self):
            return str(self.data)


    def __init__(self):
        self.root = None    

    def insert(self, data):
        self.root = self.insert_recursive(self.root, data)

    def insert_recursive(self, node, data):
        if not node:
            return self.AVLNode(data)
        elif data < node.data:
            node.left = self.insert_recursive(node.left, data)
        else:
            node.right = self.insert_recursive(node.right, data)

        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))

        balance = self.getBalance(node)

        # left left
        if balance > 1 and data < node.left.data:
            return self.rightRotate(node)

        # right right
        if balance < -1 and data > node.right.data:
            return self.leftRotate(node)

        # left right
        if balance > 1 and data > node.left.data:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)

        # right left
        if balance < -1 and data < node.right.data:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return node

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2

        # Update heights 
        z.height = 1 + max(self.getHeight(z.left), 
                         self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                         self.getHeight(y.right)) 
  
        # Return the new root 
        return y 

    def rightRotate(self, z):
        y = z.left 
        T3 = y.right   
        # Perform rotation 
        y.right = z 
        z.left = T3   
        # Update heights 
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right)) 
        # Return the new root 
        return y 


    def getHeight(self, node):
        if node is None:
            return 0
        return node.height
    
    def getBalance(self, node):
        if node is None:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)


    def find(self, data):
        node = self.root

        while node is not None:
            if node.data == data:
                return node
            elif node.data < data:
                node = node.left
            else:
                node = node.right

        return None


    def delete(self, data):
        self.delete_recursive(self.root, data)

    def delete_recursive(self, node, data):
        if node is None:
            return node
        elif data == node.data:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            else:
                temp = self.minValue(node.right)
                node.data = temp.data
                node.right = self.delete_recursive(node.right, temp.data)
            
        elif data < node.data:
            node.left = self.delete_recursive(node.left, data)
        else:
            node.right = self.delete_recursive(node.right, data)


        if node is None:
            return node
        
        node.height = 1 + max(self.getHeight(node.left), 
                            self.getHeight(node.right)) 

        balance = self.getBalance(node)

        # left left
        if balance > 1 and self.getBalance(node.left) >=0:
            return self.rightRotate(node)

        # right right
        if balance < -1 and self.getBalance(node.right) <= 0:
            return self.leftRotate(node)

        # left right
        if balance > 1 and self.getBalance(node.left) < 0:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)

        # right left
        if balance < -1 and self.getBalance(node.left) > 0:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return node


    def inorder(self):
            self.inorder_recursive(self.root)

    def inorder_recursive(self, node):
        if node is not None:
            self.inorder_recursive(node.left)
            print(node.data)
            self.inorder_recursive(node.right)   
    


    def inOrderSuccessor(self, node):
        if node.right is not None:
            return self.minValue(node.right)
        
        succ = None
        current = self.root
        while current is not None:
            if node.data == current.data:
                break
            elif node.data < current.data:
                succ = current
                current = current.left
            else:
                current = current.right

        return succ

    def inOrderPredecessor(self, node):
        if node.left is not None:
            return self.maxValue(node.left)

        pred = None
        current = self.root
        while current is not None:
            if node.data == current.data:
                break
            elif current.data < node.data:
                pred = current
                current = current.right
            else:
                current = current.left

        return pred


    def minValue(self, node):
        c = node
        while c is not None and c.left is not None:
            c = c.left
        return c

    def maxValue(self, node):
        c = node
        while c is not None and c.right is not None:
            c = c.right
        return c




REGULAR = 0
START = 1
END = 2
MERGE = 3
SPLIT = 4


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vertex_type = REGULAR

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)



class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.helper = None

    def find_x_intersection(self, y):
        if self.v2.y == self.v1.y:
            if self.v2.x > self.v1.x:
                return self.v2.x
            else:
                return self.v1.x        
        return (float((y - self.v1.y)*(self.v2.x-self.v1.x))/(self.v2.y-self.v1.y)) + self.v1.x

    def __eq__(self, other):
        return (self.v1 == other.v1) and (self.v2 == other.v2)




def random_polygon(n):
    vertex_list = []

    anglestep = 2*math.pi/n
    radius = n*2

    a = 0
    for _ in range(n):
        r = radius + random.randint(-radius/2, radius/2)
        angle = a + random.uniform(-anglestep/2, anglestep/2)
        x = r*math.cos(angle)
        y = r*math.sin(angle)
        vertex_list.append(Vertex(int(x), int(y)))
        a += anglestep

    return vertex_list


def find_turn(p1, p2, p3):
    val = (float(p2.y - p1.y) * (p3.x-p2.x)) - (float(p2.x-p1.x)*(p3.y-p2.y))

    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0


def get_angles(polygon):
    angles = []
    for i in range(len(polygon)):
        p1 = polygon[(i-1)%len(polygon)]
        p2 = polygon[i]
        p3 = polygon[(i+1)%len(polygon)]

        direction = find_turn(p1, p2, p3)

        x1 = p2.x - p1.x
        y1 = p2.y - p1.y
        x2 = p3.x - p2.x
        y2 = p3.y - p2.y

        dotprod = x1*x2 + y1*y2
        denominator = math.sqrt((x1**2 + y1**2)*(x2**2 + y2**2))
        angle = (math.acos(dotprod/denominator) * 180 )/ math.pi
        
        
        if direction < 1:
            angles.append(180-angle)
        else:
            angles.append(180+angle)

    return angles


def is_below(p, q):
    return (p.y < q.y or (p.y == q.y and p.x > q.x))

def is_above(p, q):
    return (p.y > q.y or (p.y == q.y and p.x < q.x))


def find_vertex_type(polygon):

    angles = get_angles(polygon)

    for i in range(len(polygon)):
        p1 = polygon[(i-1)%len(polygon)]
        p2 = polygon[i]
        p3 = polygon[(i+1)%len(polygon)]

        vertex_type = REGULAR

        if is_below(p1, p2) and is_below(p3, p2):
            if angles[i] > 180:
                vertex_type = SPLIT
            else:
                vertex_type = START
        
        elif is_above(p1, p2) and is_above(p3, p2):
            if angles[i] > 180:
                vertex_type = MERGE
            else:
                vertex_type = END
        
        polygon[i].vertex_type = vertex_type
    
    return polygon



class NodeData:
    def __init__(self, edge, x_intersection):        
        self.edge = edge
        self.x_intersection = x_intersection
        
    def __lt__(self, other):
        return self.x_intersection < other.x_intersection

    def __gt__(self, other):
        return self.x_intersection > other.x_intersection
    
    def __eq__(self, other):
        self.edge == other.edge


class StatusLineBST(AVLTree):    

    def __init__(self):
        AVLTree.__init__(self)
        self.y_position = None

    def insert(self, edge):
        if is_above(edge.v1, edge.v2):
            x_intersection = edge.v1.x
        else:
            x_intersection = edge.v2.x

        data = NodeData(edge, x_intersection)
        super().insert(data)

    def delete(self, edge):
        data = NodeData(edge, edge.find_x_intersection(self.y_position))
        super().delete(data)

    def nearest_left_edge(self, vertex):
        node = self.root
        left = None
        while node is not None:
            if vertex.x > node.data.x_intersection:
                left = node
                node = node.right
            else:
                node = node.left

        return left.data.edge

    def set_y_position(self, y_position):
        self.y_position = y_position
        self.update_x_intersection(self.root)

    def update_x_intersection(self, node):
        if node is not None:
            e = node.data.edge
            node.data.x_intersection = e.find_x_intersection(self.y_position)
            self.update_x_intersection(node.left)
            self.update_x_intersection(node.right)


def get_event_points(polygon):
    events = []
    for i in range(len(polygon)):
        events.append((i, (-polygon[i].y, polygon[i].x)))
    
    events.sort(key=lambda e: e[1])
    events = [e[0] for e in events]
    return events



# ------------------------------------
# THE MAIN ALGORITHM
# ------------------------------------
def find_diagonals(vertex_list):

    diagonals = []
    edges = [Edge(vertex_list[i], vertex_list[(i+1)%len(vertex_list)]) for i in range(len(vertex_list))]
    events = get_event_points(polygon)
    status_bst = StatusLineBST()


    for i in events:
        y_position = vertex_list[i].y
        status_bst.set_y_position(y_position)
        
        # start vertex
        if vertex_list[i].vertex_type == START:
            edges[i].helper = vertex_list[i]

            # if polygon is to the right of edge
            if is_above(edges[i].v1, edges[i].v2):
                status_bst.insert(edges[i])


        # end vertex
        elif vertex_list[i].vertex_type == END:
            if edges[i-1].helper.vertex_type == MERGE:
                diagonals.append((vertex_list[i], edges[i-1].helper))
            status_bst.delete(edges[i-1])


        # split vertex
        elif vertex_list[i].vertex_type == SPLIT:
            left_edge = status_bst.nearest_left_edge(vertex_list[i])
            diagonals.append((vertex_list[i], left_edge.helper))
            left_edge.helper = vertex_list[i]
            edges[i].helper = vertex_list[i]
            status_bst.insert(edges[i])


        # merge vertex
        elif vertex_list[i].vertex_type == MERGE:
            if edges[i-1].helper.vertex_type == MERGE:
                diagonals.append((vertex_list[i], edges[i-1].helper))
            status_bst.delete(edges[i-1])
            left_edge = status_bst.nearest_left_edge(vertex_list[i])
            if left_edge.helper.vertex_type == MERGE:
                diagonals.append((vertex_list[i], left_edge.helper))
            left_edge.helper = vertex_list[i]


        # regular vertex
        else:
            # if the interior of polygom lies to the right of vi
            if is_above(vertex_list[i], vertex_list[(i+1)%len(vertex_list)]):
                if edges[i-1].helper.vertex_type == MERGE:
                    diagonals.append((vertex_list[i], edges[i-1].helper))
                    
                status_bst.delete(edges[i-1])
                edges[i].helper = vertex_list[i]
                status_bst.insert(edges[i])
            else:
                left_edge = status_bst.nearest_left_edge(vertex_list[i])
                if left_edge.helper.vertex_type == MERGE:
                    diagonals.append((vertex_list[i], left_edge.helper))
                left_edge.helper = vertex_list[i]

    return diagonals
    


if __name__ == "__main__":
    polygon = random_polygon(25)

    # plot the polygon
    X = [v.x for v in polygon] + [polygon[0].x]
    Y = [v.y for v in polygon] + [polygon[0].y]
    plt.plot(X, Y, ".-b")

    find_vertex_type(polygon)

    diagonals = find_diagonals(polygon)

    # plot the diagonals
    for diagonal in diagonals:
        x1 = diagonal[0].x
        x2 = diagonal[1].x
        y1 = diagonal[0].y
        y2 = diagonal[1].y
        plt.plot([x1, x2], [y1, y2], "-r")

    plt.show()
