"""Interface Streamlit: escolha de origem/destino e exibição da menor rota."""

import streamlit as st

from desenho import desenhar_grafo
from grafo import PONTOS, RUAS, criar_grafo, menor_caminho

st.set_page_config(page_title="Rotas com Dijkstra", layout="wide")
st.title("Menor rota entre pontos da cidade — Dijkstra")


def rotulo(codigo):
    return f"{codigo} — {PONTOS[codigo]}"


# ---- Desafio adicional: alterar pesos / desativar ruas ----
st.sidebar.header("Ruas (desafio adicional)")
st.sidebar.caption("Altere a distância ou desative uma rua e recalcule a rota.")

ruas_ativas = []
ruas_desativadas = []
for u, v, peso in RUAS:
    col1, col2 = st.sidebar.columns([2, 1])
    novo_peso = col1.number_input(f"{u} — {v} (km)", min_value=1, value=peso,
                                  step=1, key=f"peso_{u}{v}")
    ativa = col2.checkbox("ativa", value=True, key=f"ativa_{u}{v}")
    if ativa:
        ruas_ativas.append((u, v, novo_peso))
    else:
        ruas_desativadas.append((u, v, novo_peso))

grafo = criar_grafo(ruas_ativas)

# ---- Seleção de origem e destino ----
col_origem, col_destino = st.columns(2)
origem = col_origem.selectbox("Origem", list(PONTOS), index=0, format_func=rotulo)
destino = col_destino.selectbox("Destino", list(PONTOS), index=len(PONTOS) - 1,
                                format_func=rotulo)

calcular = st.button("Calcular rota", type="primary")

caminho = []
if calcular:
    if origem == destino:
        st.warning("Origem e destino são o mesmo ponto. Escolha pontos diferentes.")
    else:
        caminho, distancia = menor_caminho(grafo, origem, destino)
        if not caminho:
            st.error(f"Não existe caminho entre {origem} e {destino} "
                     "com as ruas ativas.")
        else:
            st.success(f"Caminho: **{' → '.join(caminho)}**")
            st.metric("Distância total", f"{distancia} km")

            trechos = [
                {"Trecho": f"{a} → {b}",
                 "Distância (km)": next(p for viz, p in grafo[a] if viz == b)}
                for a, b in zip(caminho, caminho[1:])
            ]
            st.table(trechos)

st.pyplot(desenhar_grafo(ruas_ativas, caminho, ruas_desativadas))

with st.expander("Lista de adjacência usada pelo algoritmo"):
    for vertice, vizinhos in grafo.items():
        st.write(f"**{vertice}** → {vizinhos}")
