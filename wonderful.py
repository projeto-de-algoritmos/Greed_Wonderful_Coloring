import heapq

def get_wonderful_colors(sequence, colors):
    n = len(sequence)
    k = len(colors)

    res = [0] * n

    hs = {}
    
    for i,s in enumerate(sequence):
        if s not in hs:
            hs[s] = [i]
        else:
            hs[s].append(i)

    qtd = 0

    for _, v in hs.items():
        qtd += min(len(v), k)

    
    qtd //= k


    pq = []

    for c in colors:
        heapq.heappush(pq, (-qtd, c))

    for _, v in hs.items():
        for i in range(min(len(v), k)):
            q, c = heapq.heappop(pq)
            if q >= 0:
                continue
            res[v[i]] = c
            q += 1
            heapq.heappush(pq, (q, c))

    return res

if __name__ == '__main__':
    vec = [3, 1, 1, 1, 1, 10, 3, 10, 10, 2]
    colors = ['1', '2', '3']

    print(*get_wonderful_colors(vec, colors))
