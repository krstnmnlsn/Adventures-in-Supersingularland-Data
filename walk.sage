def build_isogeny_graph_over_Fpbar(p, l, steps=oo):
    """
    Given a prime p, this function returns the l-isogeny graph of supersingular
    elliptic curves over bar(F_p).

    If given, this only gives the graph up to "steps" number of edges from an
    origin curve.

    The algorithm works by first finding any supersingular j-invariant via an
    algorithm of Broker, then walking the isogeny graph by a BFS.

    References:
     - Constructing Supersingular Elliptic Curves - Reinier Broker

    STEP 1: Find a single super-singular curve.
    Given a prime p >= 5, this step finds a supersingular elliptic curve over
    F_{p^2}.
    """
    q = next(q for q in Primes() if q%4 == 3 and kronecker_symbol(-q,p) == -1)
    K = QuadraticField(-q)
    H = K.hilbert_class_polynomial()
    j0 = H.change_ring(GF(p^2)).any_root()
    """
    STEP 2: Walk along the isogeny graph.

    Two elliptic curves E1,E2 are l-isogenous (over bar(F_p)) if and only if
    x=j(E1),y=j(E2) are a root of the l-modular polynomial Phi_l. Tables of
    Phi_l can be found online (see
    https://math.mit.edu/~drew/ClassicalModPolys.html) and in Sage via
    `ClassicalModularPolynomialDatabase()`.
    """
    phi = ClassicalModularPolynomialDatabase()[l]
    def get_neighbors(j):
        """
        This function returns a list of all roots of Phi_l(j,X), repeated with
        appropiate multiplicity.
        """
        R.<x> = GF(p^2)[]
        return flatten([[j2]*k for j2,k in phi(j,x).roots()])
    G = DiGraph(multiedges=True,loops=True)
    visited = set()
    not_visited = set([j0])
    count = 0
    while not_visited:
        j1 = not_visited.pop()
        visited.add(j1)
        for j2 in get_neighbors(j1):
            G.add_edge([j1,j2])
            if j2 not in visited and j2 not in not_visited:
                not_visited.add(j2)
        count += 1
        if count == steps:
            break
    return G


