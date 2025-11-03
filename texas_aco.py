# texas_aco.py
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict
from heapq import heappush, heappop

# ---------------------------------------
# Approximate Texas shape as boolean mask
# ---------------------------------------
def texas_mask(width=60, height=50):
    """Returns a set of blocked (x,y) coordinates forming an approximate Texas outline."""
    blocked = set()
    for y in range(height):
        for x in range(width):
            # Rough polygonal cutoff to mimic Texas shape
            if (
                y < 10 and (x < 15 or x > 45)
                or (y >= 10 and y < 20 and (x < 10 or x > 50))
                or (y >= 20 and y < 30 and (x < 5 or x > 55))
                or (y >= 30 and y < 40 and (x < 8 or x > 52))
                or (y >= 40 and x < 20)
            ):
                blocked.add((x, y))
    return blocked

# ---------------------------------------
# Grid and graph builder
# ---------------------------------------
def grid_graph(width, height, obstacles=None, diag=True):
    obstacles = obstacles or set()
    nodes, edges = [], []
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    if diag: dirs += [(1,1),(1,-1),(-1,1),(-1,-1)]
    def inside(x,y): return 0<=x<width and 0<=y<height and (x,y) not in obstacles
    for y in range(height):
        for x in range(width):
            if inside(x,y):
                nodes.append((x,y))
                for dx,dy in dirs:
                    nx, ny = x+dx, y+dy
                    if inside(nx,ny) and (x,y)<(nx,ny):
                        edges.append(((x,y),(nx,ny)))
    return nodes, edges

# ---------------------------------------
# Ant colony optimization
# ---------------------------------------
def ant_colony_path(nodes, edges, source, sink, n_ants=100, n_iter=250,
                    alpha=1.0, beta=4.0, rho=0.3, Q=100):
    nbrs = defaultdict(list)
    length = {}
    for (u,v) in edges:
        nbrs[u].append(v); nbrs[v].append(u)
        length[(u,v)] = length[(v,u)] = np.hypot(v[0]-u[0], v[1]-u[1])
    pheromone = {(u,v):1.0 for (u,v) in edges}
    pheromone.update({(v,u):1.0 for (u,v) in edges})

    best_path, best_cost = None, float('inf')
    for iteration in range(n_iter):
        all_paths=[]
        for _ in range(n_ants):
            path, cost = construct_path(source, sink, nbrs, length, pheromone, alpha, beta)
            if path:
                all_paths.append((path, cost))
                if cost < best_cost:
                    best_path, best_cost = path, cost
        # evaporate + reinforce
        for e in pheromone: pheromone[e] *= (1 - rho)
        for path, cost in all_paths:
            for i in range(len(path)-1):
                u,v = path[i], path[i+1]
                pheromone[(u,v)] += Q/cost
                pheromone[(v,u)] += Q/cost
        if iteration % 25 == 0:
            print(f"Iter {iteration:3d} | best = {best_cost:.2f}")
    return pheromone, best_path

def construct_path(source, sink, nbrs, length, pheromone, alpha, beta):
    path=[source]; visited={source}; cost=0; current=source
    for _ in range(1000):
        if current==sink: return path, cost
        choices=[]
        total=0
        for n in nbrs[current]:
            if n not in visited:
                tau=pheromone[(current,n)]**alpha
                eta=(1/length[(current,n)])**beta
                total+=tau*eta
                choices.append((n,tau*eta,length[(current,n)]))
        if not choices: return None, float('inf')
        r=random.random()*total; s=0
        for n,p,l in choices:
            s+=p
            if s>=r:
                path.append(n); visited.add(n); cost+=l; current=n; break
    return None, float('inf')

# ---------------------------------------
# Visualization
# ---------------------------------------
def draw_texas_network(pheromone, width, height, obstacles, cities, best_path):
    fig, ax = plt.subplots(figsize=(9,8))
    ax.set_xlim(-0.5, width-0.5)
    ax.set_ylim(-0.5, height-0.5)
    ax.set_aspect('equal')
    ax.invert_yaxis()

    maxP = max(pheromone.values())
    for (u,v),p in pheromone.items():
        if p < 0.5: continue
        (x1,y1),(x2,y2)=u,v
        ax.plot([x1,x2],[y1,y2],color='deepskyblue',alpha=min(1,p/maxP),lw=2*(p/maxP))
    if obstacles:
        obs = np.array(list(obstacles))
        ax.scatter(obs[:,0], obs[:,1], s=15, c='lightgray', marker='s', alpha=0.6)
    # plot cities
    for name,(x,y) in cities.items():
        ax.scatter(x,y,s=120,c='orange',edgecolors='black')
        ax.text(x+0.5,y,name,fontsize=9,ha='left',va='center')
    # best path
    if best_path:
        xs,ys = zip(*best_path)
        ax.plot(xs,ys,color='yellow',lw=4,alpha=0.9,label='Best Path')
    ax.legend(loc='upper right')
    plt.title("Ant Colony Optimization - Texas Metro Network")
    plt.axis('off')
    plt.show()

# ---------------------------------------
# Demo run
# ---------------------------------------
if __name__=="__main__":
    random.seed(10)
    W,H=60,50
    obstacles = texas_mask(W,H)

    # approximate city coords (roughly scaled)
    cities = {
        "Dallas": (35,15),
        "Houston": (40,25),
        "Austin": (33,28),
        "San Antonio": (30,33),
        "El Paso": (10,35),
        "Lubbock": (18,18),
        "Amarillo": (17,10),
        "Corpus Christi": (35,40),
        "McAllen": (30,44)
    }

    nodes,edges=grid_graph(W,H,obstacles,diag=True)
    source="El Paso"; sink="Houston"
    print(f"Running ACO from {source} to {sink}...")
    pheromone,best_path=ant_colony_path(nodes,edges,cities[source],cities[sink],
        n_ants=100,n_iter=250,alpha=1.0,beta=5.0,rho=0.25,Q=80)
    draw_texas_network(pheromone,W,H,obstacles,cities,best_path)
