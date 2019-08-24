
# For primes between 50,000 and 100,000, 1000 conjugate pairs and 1000 arbitrary
# pairs were tested with the following method. The output is stored in Pairs 
# Through Fp Random Sampling.csv.
def how_many_vertices_admit_shortest_paths_that_touch_Fp_1000(p):
    # Given a prime p, we select 1000 random pairs of vertices and comput C, the
    # number of those pairs which have a shortest path that goes through F_p. We
    # also compute Cconj, the number of times the first vertex in our pair has a
    # path to its conjugate vertex passing through F_p. We return [Cconj, C].
    
    # Build the graph.
    G = build_isogeny_graph_over_Fpbar(p,2)
    # J is a list of vertices in F_{p^2} \ F_p.
    J = Set([j for j in G.vertices() if j.pth_power() != j])
    # H is a list of vertices in F_p.
    H = [j for j in G.vertices() if j.pth_power() == j]

    # Next we iterate over 1000 random pairs of vertices. C is the number of
    # vertices pairs that hada shortest path through F_p. Cconj is the number of
    # times the first vertex in the randomly selected pair had a shortest path
    # to its conjugate vertex that went through F_p.
    C = 0
    Cconj = 0
    for _ in range(0,1000):
        j1 = J.random_element()
        j2 = J.random_element()
        jconj = j1.pth_power()
        # d = length of the shortest path from j1 to j2.
        d = G.distance(j1,j2)
        dconj = G.distance(j1, jconj)
        # If there is a shortest path between j1 and j2 passing through F_p add
        # 1 to C.
        if any(G.distance(j1,j3) + G.distance(j3,j2) == d for j3 in H):
            C += 1
        # If there is a shortest path between j1 and its conjugate pair passing
        # through F_p add 1 to Cconj.
        if any(G.distance(j1,j3) + G.distance(j3,jconj) == dconj for j3 in H):
            Cconj += 1
    return Cconj,C

# Primes between 1000 and 5000 were tested with the following method. The output
# was stored in Pairs Through Fp Small.csv.
def how_many_vertices_admit_shortest_paths_that_touch_Fp(p):
    # Given a prime p, this returns a tuple [Cconj,Tconj, C, T]. Cconj is the
    # number of times a vertex in the graph had a shortest path to its conjugate
    # vertex passing through F_p. Tconj is the total number of conjugate pairs
    # in the graph. C is the number of times a pair of vertices in the graph had
    # a shortest path passing through F_p. T is the total number of unique pairs
    # of vertices.
    
    # Load the graph G and the list of distances between vertices D.
    G, D = load_graph_data(p)
    # J is a list of vertices in F_{p^2} \ F_p.
    H = [j for j in G.vertices() if j.pth_power() == j]
    # H is a list of vertices in F_p.
    J = [j for j in G.vertices() if j not in H]
    Tconj = 0
    Cconj = 0
    T = 0
    C = 0
    # For each vertex in the graph, check if there is a shortest path between it
    # and its conjugate pair passing through F_p.
    for j1 in J:
        j2 = j1^p
        if j1 < j2:
            Tconj += 1
            # d = length of the shortest path from j1 to j2.
            dconj = D[j1][j2]
            if any(D[j1][j3] + D[j3][j2] == dconj for j3 in H):
                Cconj += 1
    # For each pair of vertices in the graph, check if there is a shortest path
    # between them that passes through F_p.
    for j1 in J:
        for j2 in J:
            if j1 < j2:
                T += 1
                # d = length of the shortest path from j1 to j2.
                d = D[j1][j2]
                if any(D[j1][j3] + D[j3][j2] == d for j3 in H):
                    C += 1
    return Cconj, Tconj, C,T

# Primes between 1000 and 5000 were tested with the following method. The output
# was stored in Pairs Through a Random Subgraph.csv.
def how_many_vertices_admit_shortest_paths_that_touch_rand_10(p):
    # Given a prime p, this returns a tuple [Cconj,Tconj, C, T]. The data is
    # collected from 10 random subsets of the graph. Cconj is the number of times
    # a vertex in the graph had a shortest path to its conjugate vertex passing
    # through one of the subgraphs. Tconj is the total number of conjugate pairs
    # in the graph. C is the number of times a pair of vertices in the graph had
    # a shortest path passing through one of the random subgraphs. T is the total
    # number of unique pairs of vertices.
    
    # Load the graph G and the list of distances between vertices D.
    G, D = load_graph_data(p)
    # Hp is a list of vertices in Fp.
    Hp = [j for j in G.vertices() if j.pth_power() == j]
    Tconj = 0
    Cconj = 0
    T = 0
    C = 0
    for _ in range(0,10):
        # For each Fp vertex, pick a corresponding random vertex in G.
        H = G.subgraph(G.random_vertex() for _ in Hp)
        J = [j for j in G.vertices() if j not in H]

        # Iterate over all conjugate pairs of vertices and count how many have a
        # shortest path through the random set of vertices H.
        for j1 in J:
            j2 = j1^p
            if j1 < j2:
                Tconj += 1
                # dconj = length of the shortest path from j1 to j2.
                dconj = D[j1][j2]
                if any(D[j1][j3] + D[j3][j2] == dconj for j3 in H):
                    Cconj += 1
        # Iterate over all pairs of vertices and count how many have a shortest
        # path through the random set of vertices H.
        for j1 in J:
            for j2 in J:
                if j1 < j2:
                    T += 1
                    # d = length of the shortest path from j1 to j2.
                    d = D[j1][j2]
                    if any(D[j1][j3] + D[j3][j2] == d for j3 in H):
                        C += 1
    return Cconj, Tconj, C,T

# The following script was used to compute distance information for some primes
# between 10253 and 65437. Primes were all 1 mod 4, and chosen to be spaced at
# least 200 apart. For each prime, the distance between 100 random pairs of
# vertices was calculated, as well as the average distance between all
# components of the Fp subgraph. The output was stored in Distances Between
# Random Pairs and Components 1 mod 4.csv.
DATA = []
count = 0
while p < 100000:
    # Check primes spaced about 200 apart that are 1 mod 4.
    p = next_prime_mod(p + 200, 4, 1)
    G = build_isogeny_graph_over_Fp2(p, 2)
    diam = G.diameter()
    # Calculate the distances between 100 random pairs of vertices.
    target = 100
    random_dist = []
    for _ in range(target):
        v = G.random_vertex()
        w = G.random_vertex()
        random_dist.append(G.distance(v,w))
    # Compute the average distance between all components of the Fp subgraph.
    dist = fp_component_distances(p, G)
    DATA.append([p,diam, dist, random_dist])

