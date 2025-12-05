# coding: utf-8
import streamlit as st
import pandas as pd
from supabase import create_client, Client
import hashlib
from datetime import datetime

# ----------------- CONFIG GERAL -----------------

st.set_page_config(
    page_title="Avaliação 360 - Startup Leiria",
    page_icon="📊",
    layout="wide",
)

# ----------------- CSS / TEMA -----------------

st.markdown(
    """
    <style>
    body {
        background: radial-gradient(circle at top left, #e0f2fe 0, #f9fafb 40%, #eef2ff 100%);
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .main-header {
        background: linear-gradient(135deg, #020617, #111827);
        border-radius: 18px;
        padding: 1.3rem 1.6rem;
        color: #f9fafb;
        box-shadow: 0 10px 25px rgba(15,23,42,0.35);
        margin-bottom: 1.5rem;
    }
    .main-header-inner {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .logo-circle {
        width: 52px;
        height: 52px;
        border-radius: 999px;
        background: radial-gradient(circle at 30% 20%, #fde68a, #f97316);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.2rem;
        color: #111827;
        box-shadow: 0 6px 16px rgba(0,0,0,0.35);
    }
    .header-title h1 {
        font-size: 1.35rem;
        margin: 0;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .header-title p {
        margin: 0.2rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        border-radius: 999px;
        border: 1px solid rgba(248,250,252,0.25);
        padding: 0.15rem 0.6rem;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        background: rgba(15,23,42,0.7);
    }
    .card {
        background: #f9fafb;
        border-radius: 16px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 2px 10px rgba(15,23,42,0.06);
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
    }
    .metric-card {
        background: white;
        border-radius: 14px;
        padding: 0.9rem 1rem;
        box-shadow: 0 2px 8px rgba(15,23,42,0.06);
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 1.4rem;
        color: #111827;
    }
    .metric-card p {
        margin: 0.2rem 0 0 0;
        color: #6b7280;
        font-size: 0.85rem;
    }
    .stButton > button {
        border-radius: 999px !important;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        border: none;
        background: linear-gradient(135deg, #f97316, #ec4899);
        color: white;
        box-shadow: 0 6px 18px rgba(249,115,22,0.35);
    }
    .stButton > button:hover {
        filter: brightness(1.05);
    }
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #f97316, #ec4899) !important;
    }
    section[data-testid="stSidebar"] {
        background: #020617;
        color: #e5e7eb;
    }
    section[data-testid="stSidebar"] .css-1d391kg,
    section[data-testid="stSidebar"] .css-1lcbmhc {
        color: #e5e7eb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_header(subtitle: str | None = None):
    st.markdown(
        f"""
        <div class="main-header">
          <div class="main-header-inner">
            <div class="logo-circle">SL</div>
            <div class="header-title">
              <h1>Avaliação 360 · Startup Leiria</h1>
              <p>{subtitle or "Feedback contínuo para alinhar expectativas, desenvolver talento e fortalecer a cultura."}</p>
              <div style="margin-top:0.35rem;">
                <span class="chip">Equipa · Marketing · Projetos · Consultoria & Ecossistema</span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------- LIGAÇÃO AO SUPABASE -----------------

@st.cache_resource
def init_connection() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


supabase = init_connection()

# ----------------- UTILIZADORES BASE -----------------
# agora em dicts, menos propenso a erros

USERS = [
    # CEO
    {
        "name": "Vítor Ferreira",
        "email": "vitor.ferreira@startupleiria.com",
        "password": "1234",
        "role": "CEO",
        "team": "Consultoria & Ecossistema",
    },
    # Marketing
    {
        "name": "Francisco Aguiar",
        "email": "francisco.aguiar@startupleiria.com",
        "password": "1234",
        "role": "RESPONSAVEL",
        "team": "Marketing",
    },
    {
        "name": "Natacha Amorim",
        "email": "natacha.amorim@startupleiria.com",
        "password": "1234",
        "role": "MEMBRO",
        "team": "Marketing",
    },
    {
        "name": "Mariana Reis",
        "email": "mariana.reis@startupleiria.com",
        "password": "1234",
        "role": "MEMBRO",
        "team": "Marketing",
    },
    {
        "name": "Nicole Santos",
        "email": "hello@startupleiria.com",
        "password": "1234",
        "role": "ESTAGIARIO",
        "team": "Marketing",
    },
    # Administrativo
    {
        "name": "Ana Coelho",
        "email": "ana.coelho@startupleiria.com",
        "password": "1234",
        "role": "RESPONSAVEL",
        "team": "Administrativo",
    },
    {
        "name": "Paula Sequeira",
        "email": "paula.sequeira@startupleiria.com",
        "password": "1234",
        "role": "MEMBRO",
        "team": "Administrativo",
    },
    {
        "name": "Rita Ferreira",
        "email": "rita.ferreira@startupleiria.com",
        "password": "1234",
        "role": "MEMBRO",
        "team": "Administrativo",
    },
    {
        "name": "Bernardo Vieira",
        "email": "info@startupleiria.com",
        "password": "1234",
        "role": "ESTAGIARIO",
        "team": "Administrativo",
    },
    # Projetos
    {
        "name": "Bruno Ramalho",
        "email": "bruno.ramalho@startupleiria.com",
        "password": "1234",
        "role": "RESPONSAVEL",
        "team": "Projetos",
    },
    {
        "name": "Luís Fonseca",
        "email": "luis.fonseca@startupleiria.com",
        "password": "1234",
        "role": "MEMBRO",
        "team": "Projetos",
    },
    {
        "name": "Margarida Sousa",
        "email": "margarida.sousa@startupleiria.com",
        "password": "1234",
        "role": "MEMBRO",
        "team": "Projetos",
    },
    {
        "name": "Luís Pacheco",
        "email": "suporte@startupleiria.com",
        "password": "1234",
        "role": "ESTAGIARIO",
        "team": "Projetos",
    },
    # Consultoria & Ecossistema (núcleo)
    {
        "name": "João Ramos",
        "email": "joao.ramos@startupleiria.com",
        "password": "1234",
        "role": "RESPONSAVEL",
        "team": "Consultoria & Ecossistema",
    },
    {
        "name": "Luis Colaço",
        "email": "luis.colaco@startupleiria.com",
        "password": "1234",
        "role": "MEMBRO",
        "team": "Consultoria & Ecossistema",
    },
    {
        "name": "Sandra Ferreira",
        "email": "apoio@startupleiria.com",
        "password": "1234",
        "role": "ESTAGIARIO",
        "team": "Consultoria & Ecossistema",
    },
    {
        "name": "Cláudia Figueiredo",
        "email": "support@startupleiria.com",
        "password": "1234",
        "role": "ESTAGIARIO",
        "team": "Consultoria & Ecossistema",
    },
]

# pessoas que pertencem a MAIS do que uma equipa (multi-equipa)
EXTRA_TEAMS = {
    "vitor.ferreira@startupleiria.com": ["Marketing", "Projetos"],  # se quiseres, podes editar
    "francisco.aguiar@startupleiria.com": ["Consultoria & Ecossistema"],
    "bruno.ramalho@startupleiria.com": ["Consultoria & Ecossistema"],
    "luis.fonseca@startupleiria.com": ["Consultoria & Ecossistema"],
    "margarida.sousa@startupleiria.com": ["Consultoria & Ecossistema"],
}


def get_user_teams(user: dict) -> set:
    """Devolve o conjunto de equipas a que o utilizador pertence (principal + extra)."""
    teams = set()
    if user.get("team"):
        teams.add(user["team"])
    extra = EXTRA_TEAMS.get(user["email"], [])
    teams.update(extra)
    return teams


def hash_pwd(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def seed_users():
    """Cria utilizadores base no Supabase se ainda não existirem."""
    try:
        res = supabase.table("users").select("email").execute()
        existing_emails = {u["email"] for u in res.data}
    except Exception as e:
        st.error(f"Erro ao aceder à tabela 'users' no Supabase: {e}")
        return

    for u in USERS:
        if u["email"] not in existing_emails:
            supabase.table("users").insert(
                {
                    "name": u["name"],
                    "email": u["email"],
                    "password_hash": hash_pwd(u["password"]),
                    "role": u["role"],
                    "team": u["team"],
                }
            ).execute()


# ----------------- COMPETÊNCIAS -----------------

BEHAVIORAL_COMPETENCIES = [
    "Colaboração & Trabalho em Equipa",
    "Comunicação",
    "Responsabilidade & Fiabilidade",
    "Orientação para Resultados",
    "Proatividade & Inovação",
]

OBJECTIVE_COMPETENCIES = [
    "Foco nas Prioridades",
    "Entrega de Resultados",
]

TECHNICAL_COMPETENCIES = {
    "Marketing": [
        "Planeamento & Execução de Campanhas",
        "Conteúdos & Copywriting",
        "Gestão de Redes Sociais & Comunidade",
        "Análise de Métricas de Marketing",
        "Branding & Posicionamento",
    ],
    "Administrativo": [
        "Organização & Gestão de Tarefas",
        "Rigor & Atenção ao Detalhe",
        "Cumprimento de Procedimentos",
        "Apoio à Equipa & Atendimento",
        "Eficiência Operacional",
    ],
    "Projetos": [
        "Planeamento de Projetos",
        "Gestão de Stakeholders",
        "Execução & Qualidade das Entregas",
        "Controlo de Prazos & Orçamento",
        "Resolução de Problemas",
    ],
    "Consultoria & Ecossistema": [
        "Diagnóstico & Pensamento Crítico",
        "Desenho de Soluções & Propostas de Valor",
        "Facilitação & Formação",
        "Relação com Clientes & Parceiros",
        "Networking & Desenvolvimento de Ecossistema",
    ],
}


# ----------------- LOGIN -----------------

def login_screen():
    render_header("Autenticação simples para garantir confidencialidade nas avaliações.")

    with st.container():
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Entrar na aplicação")
            email = st.text_input("Email", placeholder="ex: vitor.ferreira@startupleiria.com")
            password = st.text_input("Password", type="password")

            if st.button("Entrar", use_container_width=True):
                res = supabase.table("users").select("*").eq("email", email).execute()
                if len(res.data) == 0:
                    st.error("Utilizador não encontrado.")
                else:
                    user = res.data[0]
                    if hash_pwd(password) == user["password_hash"]:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Password incorreta.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Dica rápida")
            st.write(
                "Para experimentar como CEO, pode usar:\n\n"
                "`vitor.ferreira@startupleiria.com`\n\nPassword: `1234`"
            )
            st.caption("Depois pode ajustar passwords ou integrar com Supabase Auth, se quiser.")
            st.markdown('</div>', unsafe_allow_html=True)


# ----------------- FORMULÁRIO DE AVALIAÇÃO -----------------

def evaluation_form(user: dict):
    render_header("Avalie colegas ou faça a sua autoavaliação, sempre com foco em desenvolvimento.")

    res = supabase.table("users").select("*").execute()
    all_users = res.data

    evaluator_teams = get_user_teams(user)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Configuração da avaliação")

    mode = st.radio(
        "Que tipo de avaliação quer fazer?",
        ["Autoavaliação (a mim próprio/a)", "Avaliar um colega"],
        horizontal=True,
    )

    evaluatee = None

    if mode.startswith("Autoavaliação"):
        evaluatee = user
        st.caption(
            "Está a fazer **autoavaliação**. "
            "Vai responder sobre as mesmas dimensões que os outros usarão para o avaliar."
        )
    else:
        colleagues = [u for u in all_users if u["email"] != user["email"]]
        if not colleagues:
            st.info("Ainda não existem outros utilizadores registados.")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        option_labels = [f"{c['name']} ({c['team']})" for c in colleagues]
        selected = st.selectbox("Pessoa a avaliar", option_labels)
        name_clean = selected.split(" (")[0]
        evaluatee = next(c for c in colleagues if c["name"] == name_clean)

        st.caption(
            f"Está a avaliar **{evaluatee['name']}** (`{evaluatee['role']}`, equipa principal **{evaluatee['team']}**)."
        )

    st.markdown('</div>', unsafe_allow_html=True)

    if evaluatee is None:
        return

    evaluatee_teams = get_user_teams(evaluatee)
    shared_teams = evaluator_teams.intersection(evaluatee_teams)
    same_team = len(shared_teams) > 0

    if not mode.startswith("Autoavaliação"):
        if same_team:
            st.success(
                "Têm equipas em comum: **"
                + ", ".join(sorted(shared_teams))
                + "**. Vai poder avaliar competências técnicas e objetivos nessas equipas."
            )
        else:
            st.info(
                "Como não partilham nenhuma equipa, esta avaliação incide apenas sobre "
                "competências **comportamentais**."
            )

    answers = []

    with st.form("avaliacao_form"):
        # COMPORTAMENTAIS — sempre
        st.markdown("### Competências comportamentais")
        for comp in BEHAVIORAL_COMPETENCIES:
            cols = st.columns([1, 3])
            with cols[0]:
                score = st.slider(comp, 1, 5, 3, key=f"beh_{comp}")
            with cols[1]:
                comment = st.text_area(
                    f"Comentário sobre «{comp}» (opcional)",
                    key=f"beh_comment_{comp}",
                    height=70,
                )
            answers.append(("Comportamentais", comp, score, comment))
            st.markdown("---")

        # TÉCNICAS — para cada equipa partilhada
        for team in sorted(shared_teams):
            if team in TECHNICAL_COMPETENCIES:
                st.markdown(f"### Competências técnicas – {team}")
                for comp in TECHNICAL_COMPETENCIES[team]:
                    cols = st.columns([1, 3])
                    with cols[0]:
                        score = st.slider(comp, 1, 5, 3, key=f"tech_{team}_{comp}")
                    with cols[1]:
                        comment = st.text_area(
                            f"Comentário sobre «{comp}» (opcional)",
                            key=f"tech_comment_{team}_{comp}",
                            height=70,
                        )
                    answers.append((f"Técnicas - {team}", comp, score, comment))
                st.markdown("---")

        # OBJETIVOS — se houver pelo menos uma equipa em comum
        if same_team:
            st.markdown("### Objetivos")
            for comp in OBJECTIVE_COMPETENCIES:
                cols = st.columns([1, 3])
                with cols[0]:
                    score = st.slider(comp, 1, 5, 3, key=f"obj_{comp}")
                with cols[1]:
                    comment = st.text_area(
                        f"Comentário sobre «{comp}» (opcional)",
                        key=f"obj_comment_{comp}",
                        height=70,
                    )
                answers.append(("Objetivos", comp, score, comment))
            st.markdown("---")

        submitted = st.form_submit_button("💾 Guardar avaliação", use_container_width=True)

    if submitted:
        now_iso = datetime.utcnow().isoformat()
        evaluation_type = "SELF" if evaluatee["email"] == user["email"] else "OTHER"

        evaluator_team_primary = user.get("team")
        evaluatee_team_primary = evaluatee.get("team")

        for category, competency, score, comment in answers:
            supabase.table("evaluations").insert(
                {
                    "evaluator": user["email"],
                    "evaluator_team": evaluator_team_primary,
                    "evaluatee": evaluatee["email"],
                    "evaluatee_team": evaluatee_team_primary,
                    "category": category,
                    "competency": competency,
                    "score": score,
                    "comment": comment,
                    "evaluation_type": evaluation_type,
                    "created_at": now_iso,
                }
            ).execute()
        st.success("✅ Avaliação guardada com sucesso.")


# ----------------- RESULTADOS INDIVIDUAIS -----------------

def my_results(user: dict):
    render_header("Veja como está a ser percecionado nas diferentes dimensões.")

    res = supabase.table("evaluations").select("*").eq("evaluatee", user["email"]).execute()
    data = res.data

    if not data:
        st.info("Ainda não existem avaliações registadas para si.")
        return

    df = pd.DataFrame(data)

    # Todas as avaliações (inclui auto)
    grouped_all = df.groupby("category")["score"].mean().reset_index()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Médias por dimensão (todas as avaliações)")
    cols = st.columns(len(grouped_all))
    for col, row in zip(cols, grouped_all.itertuples()):
        with col:
            st.markdown(
                f"<div class='metric-card'><h3>{row.score:.2f}</h3><p>{row.category}</p></div>",
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

    # Só feedback de outros (sem auto)
    if "evaluation_type" in df.columns:
        df_others = df[df["evaluation_type"] != "SELF"]
    else:
        df_others = pd.DataFrame([])

    if not df_others.empty:
        grouped_others = df_others.groupby("category")["score"].mean().reset_index()
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Médias por dimensão (apenas feedback de colegas/liderança)")
        cols = st.columns(len(grouped_others))
        for col, row in zip(cols, grouped_others.itertuples()):
            with col:
                st.markdown(
                    f"<div class='metric-card'><h3>{row.score:.2f}</h3><p>{row.category}</p></div>",
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Ainda não tem feedback de outras pessoas – só autoavaliação.")

    # Detalhe
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Detalhe das avaliações recebidas")
    cols_to_show = [
        "category",
        "competency",
        "score",
        "comment",
        "evaluator",
        "evaluator_team",
        "evaluation_type",
        "created_at",
    ]
    cols_to_show = [c for c in cols_to_show if c in df.columns]
    st.dataframe(df[cols_to_show], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- PAINEL DO CEO -----------------

def ceo_dashboard():
    render_header("Visão agregada da equipa – incluindo o próprio CEO como avaliado.")

    res = supabase.table("evaluations").select("*").execute()
    data = res.data

    if not data:
        st.info("Ainda não existem dados de avaliação.")
        return

    df = pd.DataFrame(data)

    # Médias por avaliado (tudo)
    avg_by_person = (
        df.groupby(["evaluatee", "evaluatee_team"])["score"]
        .mean()
        .reset_index()
        .sort_values("score", ascending=False)
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Média global por pessoa (todas as avaliações)")
    st.bar_chart(avg_by_person, x="evaluatee", y="score")
    st.caption("Inclui autoavaliações e feedback de colegas/liderança.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Médias por equipa (equipa principal)
    avg_by_team = df.groupby("evaluatee_team")["score"].mean().reset_index()
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Média global por equipa (equipa principal)")
    st.bar_chart(avg_by_team, x="evaluatee_team", y="score")
    st.markdown('</div>', unsafe_allow_html=True)

    # Médias por pessoa sem autoavaliação
    if "evaluation_type" in df.columns:
        df_no_self = df[df["evaluation_type"] != "SELF"]
        if not df_no_self.empty:
            avg_by_person_no_self = (
                df_no_self.groupby(["evaluatee", "evaluatee_team"])["score"]
                .mean()
                .reset_index()
                .sort_values("score", ascending=False)
            )
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Média global por pessoa (sem autoavaliação)")
            st.bar_chart(avg_by_person_no_self, x="evaluatee", y="score")
            st.markdown('</div>', unsafe_allow_html=True)

    # Tabela detalhada
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Tabela detalhada (para exportação / análise)")
    cols_to_show = [
        "evaluator",
        "evaluator_team",
        "evaluatee",
        "evaluatee_team",
        "category",
        "competency",
        "score",
        "comment",
        "evaluation_type",
        "created_at",
    ]
    cols_to_show = [c for c in cols_to_show if c in df.columns]
    st.dataframe(df[cols_to_show], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- MAIN -----------------

def main():
    seed_users()  # garante que a tabela users tem toda a equipa

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login_screen()
        return

    user = st.session_state.user

    with st.sidebar:
        st.markdown("### 👤 Utilizador")
        st.markdown(f"**{user['name']}**  \n`{user['role']}`")
        if user.get("team"):
            st.markdown(f"Equipa principal: **{user['team']}**")
        teams = get_user_teams(user)
        if len(teams) > 1:
            st.caption("Equipas em que participa: " + ", ".join(sorted(teams)))
        st.markdown("---")
        menu = ["Minhas Avaliações", "Os Meus Resultados"]
        if user["role"] == "CEO":
            menu.append("Painel do CEO")
        choice = st.radio("Navegação", menu)
        if st.button("Terminar sessão"):
            st.session_state.user = None
            st.rerun()

    if choice == "Minhas Avaliações":
        evaluation_form(user)
    elif choice == "Os Meus Resultados":
        my_results(user)
    elif choice == "Painel do CEO":
        ceo_dashboard()


if __name__ == "__main__":
    main()
