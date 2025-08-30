import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="3D Vetor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Vetores 3D Interativo")

# Inicializa lista de vetores na sessão
if "vetores" not in st.session_state:
    st.session_state.vetores = []

# --- Entrada de novos vetores ---

nome = st.sidebar.text_input("Nome do vetor")
coord = st.sidebar.text_input("Coordenadas (x,y,z)", value="(1,0,0)")

if st.sidebar.button("Adicionar"):
    try:
        # Converte string em tupla de floats
        coords = tuple(map(float, coord.strip("()").split(",")))
        if len(coords) != 3:
            st.error("Digite exatamente 3 coordenadas!")
        else:
            st.session_state.vetores.append({"nome": nome if nome else f"V{len(st.session_state.vetores)+1}",
                                             "coords": np.array(coords)})
    except Exception as e:
        st.error("Formato inválido! Use (x,y,z)")

# --- Lista de vetores com opção de excluir ---
to_remove = []
st.sidebar.subheader("Vetores atuais")

for i, v in enumerate(st.session_state.vetores):
    x, y, z = v["coords"]
    nome = v["nome"]

    # Mostra vetor em LaTeX no sidebar
    st.sidebar.latex(rf"{nome} = {x}\hat i + {y}\hat j + {z}\hat k")

    # Botão para excluir
    if st.sidebar.checkbox("Excluir", key=f"del_{i}"):
        to_remove.append(i)


# Remove os vetores marcados
for idx in sorted(to_remove, reverse=True):
    st.session_state.vetores.pop(idx)

# --- Plotagem ---
if st.session_state.vetores:
    sequencia = st.checkbox("Vetores em sequência?", value=False)

    fig = go.Figure()

    # Eixos unitários
    cores = ["red", "green", "blue"]
    nomes = [r"\hat i", r"\hat j", r"\hat k"]
    eixos = np.identity(3)  # unitários

    for i in range(3):
        fig.add_trace(go.Scatter3d(
            x=[0, eixos[i,0]],
            y=[0, eixos[i,1]],
            z=[0, eixos[i,2]],
            mode="lines+markers",
            line=dict(width=6, color=cores[i]),
            marker=dict(size=4, color=cores[i]),
            name=nomes[i]
        ))


    # Vetores
    origem = np.array([0,0,0])
    for v in st.session_state.vetores:
        vec = v["coords"]
        fig.add_trace(go.Scatter3d(
            x=[origem[0], origem[0]+vec[0]],
            y=[origem[1], origem[1]+vec[1]],
            z=[origem[2], origem[2]+vec[2]],
            mode="lines+markers",
            line=dict(width=6, color="gray"),
            marker=dict(size=4, color="orange"),
            name=v["nome"]
        ))
        if sequencia:
            origem = origem + vec

    # Layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-10,10]),
            yaxis=dict(range=[-10,10]),
            zaxis=dict(range=[-10,10]),
            aspectmode="cube"
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        width=700, height=700
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Adicione vetores para visualizar.")
