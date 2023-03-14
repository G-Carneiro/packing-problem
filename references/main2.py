import sys
from itertools import product

from pulp import LpMaximize, LpProblem, lpSum, LpVariable


class Data:
    def __init__(self, filename):
        self.container, self.boxes = self.parse_file(filename)

    def parse_file(self, filename):        
        with open(filename, 'r') as f:
            lines = f.readlines()
        self.boxes = [None]*int(lines[0].strip())
        boxes = [None]*int(lines[0].strip())
        container = [int(x) for x in lines[1].strip().split()]
        for i, line in enumerate(lines[2:]):
            boxes[i] = [int(x) for x in line.strip().split()[1:]]        
        return container, boxes

    def get_n_items(self):
        return self.boxes.__len__()

    def __str__(self):
        to_ret = "%d %d\n" % (self.container[0], self.container[1])
        for i in self.boxes:
            to_ret += "%d %d\n" % (i[0], i[1])
        return to_ret

def usage_msg():
    print("Usage: %s input-file" % sys.argv[0])
    print("<input-file> must contain a bkw instance")


def plot_solution(pos, items, container):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots()    
    rect = Rectangle((0, 0), container[0], container[1], alpha=0.1)
    ax.add_patch(rect)
    cmap = plt.cm.get_cmap('brg', len(pos))
    for i, (x, y) in pos.items():
        rect = Rectangle((x, y), items[i][0], items[i][1], facecolor=cmap(i),
                         alpha=0.2, linewidth=1, edgecolor='k')
        ax.add_patch(rect)
        cx = x + rect.get_width()/2.0
        cy = y + rect.get_height()/2.0
        ax.annotate(f"{i}", (cx, cy), color='black', weight='bold', fontsize=10, ha='center', va='center')

    plt.xlim(0, container[0])
    plt.ylim(0, container[0])
    plt.show()


def solve_model(inputfile):
    data = Data(inputfile)
    n_items = data.get_n_items()
    items_idx = list(range(n_items))
    B = set(items_idx)    
    items, container = data.boxes, data.container
    L, W = container

    model = LpProblem("cutting-packing", LpMaximize)
    a = LpVariable.dicts("a", indices=product(B, B), cat="Binary")
    b = LpVariable.dicts("b", indices=product(B, B), cat="Binary")
    c = LpVariable.dicts("c", indices=product(B, B), cat="Binary")
    d = LpVariable.dicts("d", indices=product(B, B), cat="Binary")   
    x = LpVariable.dicts("x", indices=B, cat="Continuos", 
        lowBound=0, upBound=L)
    y = LpVariable.dicts("y", indices=B, cat="Continuos", 
        lowBound=0, upBound=W)
    p = LpVariable.dicts("p", indices=B, cat="Binary")

    model += lpSum(items[i][0]*items[i][1]*p[i] for i in B)
    for i in items_idx:
        for j in items_idx[i+1:]:
            model += x[i] + items[i][0] <= x[j] + (1 - a[i, j])*L

    for i in items_idx:
        for j in items_idx[i+1:]:
            model += x[j] + items[j][0] <= x[i] + (1 - b[i, j])*L

    for i in items_idx:
        for j in items_idx[i+1:]:
            model += y[i] + items[i][1] <= y[j] + (1 - c[i, j])*W

    for i in items_idx:
        for j in items_idx[i+1:]:
            model += y[j] + items[j][1] <= y[i] + (1 - d[i, j])*W

    for i in items_idx:
        for j in items_idx[i+1:]:
            model += a[i, j] + b[i, j] + c[i, j] + d[i, j] >= p[i] + p[j] - 1

    model.solve()
    pos = {i: (x[i].varValue, y[i].varValue) for i in B if p[i].varValue > 0.5}
    plot_solution(pos, items, container)
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage_msg()
        exit(-1)

    inputfile = sys.argv[1]
    solve_model(inputfile)
    
