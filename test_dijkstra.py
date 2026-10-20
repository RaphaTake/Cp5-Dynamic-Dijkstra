"""Testes obrigatórios do algoritmo. Executar com: python test_dijkstra.py"""

from grafo import RUAS, criar_grafo, menor_caminho

grafo = criar_grafo()

testes = [
    ("A", "G", ["A", "D", "G"], 5),
    ("G", "A", ["G", "D", "A"], 5),  # origem e destino trocados
    ("A", "C", ["A", "D", "B", "C"], 6),
    ("E", "C", ["E", "D", "B", "C"], 8),
    ("B", "F", ["B", "D", "F"], 3),
]

for origem, destino, esperado, dist_esperada in testes:
    caminho, distancia = menor_caminho(grafo, origem, destino)
    assert caminho == esperado, (origem, destino, caminho)
    assert distancia == dist_esperada, (origem, destino, distancia)
    print(f"{origem} -> {destino}: {' -> '.join(caminho)} = {distancia} km  OK")

# Conexões registradas nos dois sentidos
for u, v, peso in RUAS:
    assert (v, peso) in grafo[u] and (u, peso) in grafo[v]
print("Arestas bidirecionais OK")

# Sem caminho: removendo todas as ruas do Cliente (G), ele fica isolado
sem_g = criar_grafo([r for r in RUAS if "G" not in r[:2]])
assert menor_caminho(sem_g, "A", "G") == ([], float("inf"))
print("A -> G sem ruas para G: sem caminho  OK")

# Desafio: desativando a rua D-G, a rota A -> G muda
sem_dg = criar_grafo([r for r in RUAS if r[:2] != ("D", "G")])
print("A -> G sem a rua D-G:", menor_caminho(sem_dg, "A", "G"))
