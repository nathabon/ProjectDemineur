def reed_salomon(liste_octets):
    PP = 301
    A = [0] * 256
    A[0] = 1
    for i in range(1, 256):
        A[i] = A[i - 1] << 1
        if A[i] > 255:
            A[i] ^= PP
    m = [256 * [0] for _ in range(256)]
    for j in range(256):
        for i in range(256):
            m[A[i]][A[j]] = A[(i + j) % 255]
    G = [1, 62, 111, 15, 48, 228]
    d = len(G) - 1
    R = liste_octets + [0, 0, 0]
    for j in range(0, len(liste_octets)):
        q = R[0]
        for i in range(d):
            R[i] = R[i + 1] ^ m[q][G[i + 1]]
        if (j + d + 1) < len(liste_octets):
            R[d] = liste_octets[j + d + 1]
        else:
            R[d] = 0
    return R[:d]
