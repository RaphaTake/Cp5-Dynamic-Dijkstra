"""Desenho do grafo da cidade com NetworkX + Matplotlib (apenas visualização)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

# Posições fixas para lembrar o mapa do enunciado
POSICOES = {
    "A": (0, 0),
    "B": (1, 1),
    "C": (2.5, 1),
    "D": (1.5, 0),
    "E": (1, -1),
    "F": (2.5, -1),
    "G": (3.5, 0),
}


def desenhar_grafo(ruas, caminho=None, ruas_desativadas=()):
    """Retorna uma figura do grafo com o caminho destacado em vermelho."""
    caminho = caminho or []
    arestas_caminho = {frozenset(par) for par in zip(caminho, caminho[1:])}

    G = nx.Graph()
    G.add_nodes_from(POSICOES)
    for u, v, peso in ruas:
        G.add_edge(u, v, weight=peso)

    fig, ax = plt.subplots(figsize=(9, 5))

    normais = [e for e in G.edges if frozenset(e) not in arestas_caminho]
    destacadas = [e for e in G.edges if frozenset(e) in arestas_caminho]

    nx.draw_networkx_edges(G, POSICOES, edgelist=normais, width=1.5,
                           edge_color="black", ax=ax)
    nx.draw_networkx_edges(G, POSICOES, edgelist=destacadas, width=5,
                           edge_color="red", ax=ax)

    # Ruas desativadas aparecem tracejadas e cinza
    if ruas_desativadas:
        D = nx.Graph()
        D.add_edges_from((u, v) for u, v, _ in ruas_desativadas)
        nx.draw_networkx_edges(D, POSICOES, width=1.5, style="dashed",
                               edge_color="lightgray", ax=ax)

    cores = ["red" if v in caminho else "skyblue" for v in G.nodes]
    nx.draw_networkx_nodes(G, POSICOES, node_color=cores, node_size=1200, ax=ax)
    nx.draw_networkx_labels(G, POSICOES, font_size=14, font_weight="bold", ax=ax)

    rotulos = {(u, v): f"{d['weight']} km" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, POSICOES, edge_labels=rotulos,
                                 font_size=10, ax=ax)

    ax.set_title("Mapa simplificado da cidade — pesos em km")
    ax.axis("off")
    fig.tight_layout()
    return fig
