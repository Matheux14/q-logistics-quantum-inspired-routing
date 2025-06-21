import json
import networkx as nx
import random
import math

# --------- Classique: Dijkstra ---------
def dijkstra_path(graph, start, end):
    G = nx.Graph()
    # Ajoute tous les noeuds explicitement
    for city in graph["cities"]:
        G.add_node(city)
    for r in graph["routes"]:
        if r["status"] == "ok":
            G.add_edge(r["from"], r["to"], weight=r["distance"])
    try:
        path = nx.shortest_path(G, start, end, weight='weight')
        dist = nx.shortest_path_length(G, start, end, weight='weight')
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return {"path": None, "distance": None}
    return {"path": path, "distance": dist}

# --------- Quantum-Inspired: Simulated Annealing ---------
def simulated_annealing(graph, start, end, iterations=5000, temp=1000.0, cooling=0.995):
    G = nx.Graph()
    # Ajoute tous les noeuds explicitement
    for city in graph["cities"]:
        G.add_node(city)
    for r in graph["routes"]:
        if r["status"] == "ok":
            G.add_edge(r["from"], r["to"], weight=r["distance"])
    nodes = list(G.nodes())
    current = [start]
    while current[-1] != end:
        next_steps = [n for n in G.neighbors(current[-1]) if n not in current]
        if not next_steps:
            return {"path": None, "distance": None}
        current.append(random.choice(next_steps))
    best = current[:]
    best_dist = path_distance(G, best)
    current = best[:]
    t = temp
    for _ in range(iterations):
        t *= cooling
        candidate = shuffle_path(current, G, start, end)
        cand_dist = path_distance(G, candidate)
        if cand_dist < best_dist or random.random() < math.exp((best_dist - cand_dist) / max(t,1e-9)):
            current, best = candidate, candidate
            best_dist = cand_dist
    return {"path": best, "distance": best_dist}

def shuffle_path(path, G, start, end):
    if len(path) <= 2:
        return path
    idx = random.randint(1, len(path)-2)
    neighbors = [n for n in G.neighbors(path[idx-1]) if n not in path]
    if not neighbors:
        return path
    new_path = path[:idx] + [random.choice(neighbors)]
    # Complete randomly to end
    while new_path[-1] != end:
        next_steps = [n for n in G.neighbors(new_path[-1]) if n not in new_path]
        if not next_steps:
            break
        new_path.append(random.choice(next_steps))
    return new_path

def path_distance(G, path):
    if not path or len(path) < 2:
        return float('inf')
    return sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))

# --------- Main ---------
if __name__ == "__main__":
    # Test minimal avec le sample, gestion utf-8
    with open("../samples/sample_graph.json", encoding="utf-8") as f:
        graph = json.load(f)
    start, end = graph["cities"][0], graph["cities"][-1]

    print("Classic Dijkstra:")
    print(dijkstra_path(graph, start, end))

    print("Quantum-inspired (Simulated Annealing):")
    print(simulated_annealing(graph, start, end))
