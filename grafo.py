"""Representação do grafo da cidade e algoritmo de Dijkstra (sem interface)."""

import heapq

# Pontos da cidade (código -> descrição)
PONTOS = {
    "A": "Depósito",
    "B": "Cruzamento B",
    "C": "Cruzamento C",
    "D": "Cruzamento D",
    "E": "Cruzamento E",
    "F": "Cruzamento F",
    "G": "Cliente",
}

# Ruas (origem, destino, distância em km)
RUAS = [
    ("A", "B", 4),
    ("A", "D", 2),
    ("A", "E", 7),
    ("B", "C", 3),
    ("B", "D", 1),
    ("C", "D", 6),
    ("C", "G", 5),
    ("D", "E", 4),
    ("D", "F", 2),
    ("D", "G", 3),
    ("E", "F", 3),
    ("F", "G", 2),
]


class GrafoPonderado:
    def __init__(self):
        self.adjacencia = {}

    def adicionar_vertice(self, vertice):
        if vertice not in self.adjacencia:
            self.adjacencia[vertice] = []

    def adicionar_aresta(self, u, v, peso):
        if u in self.adjacencia and v in self.adjacencia:
            self.adjacencia[u].append((v, peso))
            self.adjacencia[v].append((u, peso))  # Ruas de mão dupla

    def mostrar_grafo(self):
        for vertice, vizinhos in self.adjacencia.items():
            print(f"{vertice} -> {vizinhos}")


def criar_grafo(ruas=RUAS):
    """Monta a lista de adjacência a partir da lista de ruas."""
    grafo = GrafoPonderado()
    for v in PONTOS:
        grafo.adicionar_vertice(v)
    for u, v, peso in ruas:
        grafo.adicionar_aresta(u, v, peso)
    return grafo.adjacencia


def dijkstra(adj_list, inicio, destino):
    """Calcula as menores distâncias a partir de `inicio`.

    Retorna (distancias, predecessores).
    """
    distancias = {v: float("inf") for v in adj_list}
    distancias[inicio] = 0
    predecessores = {v: None for v in adj_list}
    visitados = set()
    heap = [(0, inicio)]

    while heap:
        dist_atual, atual = heapq.heappop(heap)

        # Entrada antiga na fila: o vértice já foi fechado com distância menor
        if atual in visitados:
            continue
        visitados.add(atual)

        if atual == destino:
            break

        for vizinho, peso in adj_list[atual]:
            nova_dist = dist_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                predecessores[vizinho] = atual
                heapq.heappush(heap, (nova_dist, vizinho))

    return distancias, predecessores


def reconstruir_caminho(predecessores, inicio, destino):
    """Volta do destino até o início seguindo os predecessores.

    Retorna uma lista vazia se o destino não for alcançável.
    """
    caminho = []
    atual = destino
    while atual is not None:
        caminho.insert(0, atual)
        atual = predecessores[atual]

    if caminho[0] != inicio:
        return []
    return caminho


def menor_caminho(adj_list, inicio, destino):
    """Atalho: retorna (caminho, distância total) ou ([], inf) se não houver caminho."""
    distancias, predecessores = dijkstra(adj_list, inicio, destino)
    caminho = reconstruir_caminho(predecessores, inicio, destino)
    return caminho, distancias[destino]


if __name__ == "__main__":
    grafo = GrafoPonderado()
    grafo.adjacencia = criar_grafo()
    grafo.mostrar_grafo()
    print(menor_caminho(grafo.adjacencia, "A", "G"))
