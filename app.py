# coding: utf-8
import streamlit as st
import pandas as pd
from supabase import create_client, Client
import hashlib
from datetime import datetime

# ----------------- CONFIG GERAL -----------------

st.set_page_config(
    page_title="Avaliação 360° - Startup Leiria",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- CSS -----------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
        border-radius: 24px;
        padding: 2rem 2.5rem;
        color: white;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 15s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.3; }
    }
    
    .main-header-inner {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .logo-circle {
        width: 70px;
        height: 70px;
        border-radius: 20px;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 1.8rem;
        color: #1e3a8a;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        flex-shrink: 0;
    }
    
    .header-title h1 {
        font-size: 2rem;
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    
    .header-title p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 0.3rem 0.9rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.5rem;
    }
    
    .card {
        background: white;
        border-radius: 20px;
        padding: 1.8rem 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .card h3 {
        color: #1e3a8a;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #bae6fd;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        border-color: #7dd3fc;
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        color: #334155;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .metric-card .subtitle {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 400;
    }
    
    .stButton > button {
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        border: none !important;
        background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(124,58,237,0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-size: 0.9rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(124,58,237,0.6) !important;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #7c3aed 0%, #db2777 100%) !important;
    }
    
    .badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0.25rem;
    }
    
    .badge-success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .badge-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .badge-info {
        background: #dbeafe;
        color: #1e3a8a;
    }
    
    .badge-danger {
        background: #fee2e2;
        color: #991b1b;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #7c3aed 100%);
        color: white;
    }
    
    section[data-testid="stSidebar"] .css-1d391kg,
    section[data-testid="stSidebar"] .css-1lcbmhc,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        background: #f1f5f9;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%);
        color: white !important;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #7c3aed 0%, #db2777 100%) !important;
    }
    
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 12px;
        font-weight: 600;
        color: #1e3a8a;
    }
    
    .alert-success {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-info {
        background: #dbeafe;
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
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
              <h1>🎯 Avaliação 360° · Startup Leiria</h1>
              <p>{subtitle or "Sistema de feedback contínuo para desenvolvimento e alinhamento da equipa"}</p>
              <div>
                <span class="chip">💼 Equipa</span>
                <span class="chip">📱 Marketing</span>
                <span class="chip">🚀 Projetos</span>
                <span class="chip">🤝 Consultoria</span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------- SUPABASE -----------------

@st.cache_resource
def init_connection() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


supabase = init_connection()

# ----------------- USERS -----------------

USERS = [
    {"name": "Vítor Ferreira", "email": "vitor.ferreira@startupleiria.com", "password": "1234", "role": "CEO", "team": "Consultoria & Ecossistema"},
    {"name": "Francisco Aguiar", "email": "francisco.aguiar@startupleiria.com", "password": "1234", "role": "RESPONSAVEL", "team": "Marketing"},
    {"name": "Natacha Amorim", "email": "natacha.amorim@startupleiria.com", "password": "1234", "role": "MEMBRO", "team": "Marketing"},
    {"name": "Mariana Reis", "email": "mariana.reis@startupleiria.com", "password": "1234", "role": "MEMBRO", "team": "Marketing"},
    {"name": "Nicole Santos", "email": "hello@startupleiria.com", "password": "1234", "role": "ESTAGIARIO", "team": "Marketing"},
    {"name": "Ana Coelho", "email": "ana.coelho@startupleiria.com", "password": "1234", "role": "RESPONSAVEL", "team": "Administrativo"},
    {"name": "Paula Sequeira", "email": "paula.sequeira@startupleiria.com", "password": "1234", "role": "MEMBRO", "team": "Administrativo"},
    {"name": "Rita Ferreira", "email": "rita.ferreira@startupleiria.com", "password": "1234", "role": "MEMBRO", "team": "Administrativo"},
    {"name": "Bernardo Vieira", "email": "info@startupleiria.com", "password": "1234", "role": "ESTAGIARIO", "team": "Administrativo"},
    {"name": "Bruno Ramalho", "email": "bruno.ramalho@startupleiria.com", "password": "1234", "role": "RESPONSAVEL", "team": "Projetos"},
    {"name": "Luís Fonseca", "email": "luis.fonseca@startupleiria.com", "password": "1234", "role": "MEMBRO", "team": "Projetos"},
    {"name": "Margarida Sousa", "email": "margarida.sousa@startupleiria.com", "password": "1234", "role": "MEMBRO", "team": "Projetos"},
    {"name": "Luís Pacheco", "email": "suporte@startupleiria.com", "password": "1234", "role": "ESTAGIARIO", "team": "Projetos"},
    {"name": "João Ramos", "email": "joao.ramos@startupleiria.com", "password": "1234", "role": "RESPONSAVEL", "team": "Consultoria & Ecossistema"},
    {"name": "Luis Colaço", "email": "luis.colaco@startupleiria.com", "password": "1234", "role": "MEMBRO", "team": "Consultoria & Ecossistema"},
    {"name": "Sandra Ferreira", "email": "apoio@startupleiria.com", "password": "1234", "role": "ESTAGIARIO", "team": "Consultoria & Ecossistema"},
    {"name": "Cláudia Figueiredo", "email": "support@startupleiria.com", "password": "1234", "role": "ESTAGIARIO", "team": "Consultoria & Ecossistema"},
]

EXTRA_TEAMS = {
    "vitor.ferreira@startupleiria.com": ["Marketing", "Projetos"],
    "francisco.aguiar@startupleiria.com": ["Consultoria & Ecossistema"],
    "bruno.ramalho@startupleiria.com": ["Consultoria & Ecossistema"],
    "luis.fonseca@startupleiria.com": ["Consultoria & Ecossistema"],
    "margarida.sousa@startupleiria.com": ["Consultoria & Ecossistema"],
}

# ----------------- COMPETÊNCIAS -----------------

BEHAVIORAL_COMPETENCIES = [
    "Colaboração & Trabalho em Equipa",
    "Comunicação",
    "Responsabilidade & Fiabilidade",
    "Orientação para Resultados",
    "Proatividade",
    "Inovação",
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

INTERN_COMPETENCIES = [
    "Colaboração & Trabalho em Equipa",
    "Comunicação",
    "Responsabilidade & Fiabilidade",
    "Proatividade",
]

# ----------------- HELPERS -----------------

def get_user_teams(user: dict) -> set:
    teams = set()
    if user.get("team"):
        teams.add(user["team"])
    extra = EXTRA_TEAMS.get(user["email"], [])
    teams.update(extra)
    return teams


def hash_pwd(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def seed_users():
    try:
        res = supabase.table("users").select("email").execute()
        existing_emails = {u["email"] for u in res.data}
    except Exception as e:
        st.error(f"❌ Erro ao aceder à tabela 'users': {e}")
        return

    for u in USERS:
        if u["email"] not in existing_emails:
            supabase.table("users").insert({
                "name": u["name"],
                "email": u["email"],
                "password_hash": hash_pwd(u["password"]),
                "role": u["role"],
                "team": u["team"],
            }).execute()


def get_user_by_email(email: str) -> dict | None:
    res = supabase.table("users").select("*").eq("email", email).execute()
    return res.data[0] if res.data else None


def get_all_users() -> list:
    res = supabase.table("users").select("*").execute()
    return res.data


def get_evaluations_by_evaluator(email: str) -> list:
    res = supabase.table("evaluations").select("*").eq("evaluator", email).execute()
    return res.data


def get_evaluations_by_evaluatee(email: str) -> list:
    res = supabase.table("evaluations").select("*").eq("evaluatee", email).execute()
    return res.data


def get_draft(evaluator_email: str, evaluatee_email: str) -> dict | None:
    try:
        res = (
            supabase.table("evaluation_drafts")
            .select("*")
            .eq("evaluator", evaluator_email)
            .eq("evaluatee", evaluatee_email)
            .execute()
        )
        return res.data[0] if res.data else None
    except:
        return None


def save_draft(evaluator_email: str, evaluatee_email: str, draft_data: dict):
    try:
        existing = get_draft(evaluator_email, evaluatee_email)
        now_iso = datetime.utcnow().isoformat()
        
        if existing:
            supabase.table("evaluation_drafts").update({
                "draft_data": draft_data,
                "updated_at": now_iso
            }).eq("id", existing["id"]).execute()
        else:
            supabase.table("evaluation_drafts").insert({
                "evaluator": evaluator_email,
                "evaluatee": evaluatee_email,
                "draft_data": draft_data,
                "created_at": now_iso,
                "updated_at": now_iso,
            }).execute()
    except Exception as e:
        st.warning(f"Não foi possível guardar o rascunho: {e}")


def delete_draft(evaluator_email: str, evaluatee_email: str):
    try:
        supabase.table("evaluation_drafts").delete().eq(
            "evaluator", evaluator_email
        ).eq("evaluatee", evaluatee_email).execute()
    except:
        pass


def change_password(email: str, new_password: str) -> bool:
    try:
        supabase.table("users").update({
            "password_hash": hash_pwd(new_password)
        }).eq("email", email).execute()
        return True
    except:
        return False


def validate_password_strength(password: str) -> tuple[bool, str]:
    if len(password) < 6:
        return False, "Password deve ter pelo menos 6 caracteres"
    if password in ["1234", "123456", "password"]:
        return False, "Password muito fraca. Escolha algo mais seguro"
    return True, "Password válida"


# ----------------- LOGIN -----------------

def login_screen():
    render_header("Autenticação segura para garantir confidencialidade nas avaliações")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Entrar na aplicação")
        
        email = st.text_input(
            "Email corporativo",
            placeholder="nome.apelido@startupleiria.com",
        )
        password = st.text_input("Password", type="password")

        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚀 Entrar", use_container_width=True):
                if not email or not password:
                    st.error("⚠️ Preencha todos os campos")
                else:
                    user = get_user_by_email(email)
                    if not user:
                        st.error("❌ Utilizador não encontrado")
                    elif hash_pwd(password) != user["password_hash"]:
                        st.error("❌ Password incorreta")
                    else:
                        st.session_state.user = user
                        st.success("✅ Login com sucesso!")
                        st.rerun()
        
        with col_btn2:
            with st.expander("💡 Dica de teste"):
                st.caption("**CEO:** vitor.ferreira@startupleiria.com")
                st.caption("**Responsável:** francisco.aguiar@startupleiria.com")
                st.caption("**Estagiário:** hello@startupleiria.com")
                st.caption("Password: `1234`")
        
        st.markdown('</div>', unsafe_allow_html=True)


# ----------------- ALTERAR PASSWORD -----------------

def change_password_screen(user: dict):
    render_header("Altere a sua password para maior segurança")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔑 Alterar Password")
        
        st.markdown('<div class="alert-info">', unsafe_allow_html=True)
        st.markdown("🔒 **Política de segurança:**")
        st.markdown("- Mínimo 6 caracteres")
        st.markdown("- Evite passwords óbvias (1234, 123456, etc.)")
        st.markdown("- Use combinação de letras e números")
        st.markdown('</div>', unsafe_allow_html=True)

        with st.form("change_password_form"):
            current_password = st.text_input("Password atual", type="password")
            new_password = st.text_input("Nova password", type="password")
            confirm_password = st.text_input("Confirmar nova password", type="password")
            
            submitted = st.form_submit_button("🔐 Alterar Password", use_container_width=True)
            
            if submitted:
                if not current_password or not new_password or not confirm_password:
                    st.error("⚠️ Preencha todos os campos")
                elif hash_pwd(current_password) != user["password_hash"]:
                    st.error("❌ Password atual incorreta")
                elif new_password != confirm_password:
                    st.error("❌ As passwords não coincidem")
                else:
                    is_valid, msg = validate_password_strength(new_password)
                    if not is_valid:
                        st.error(f"❌ {msg}")
                    else:
                        if change_password(user["email"], new_password):
                            st.markdown('<div class="alert-success">', unsafe_allow_html=True)
                            st.markdown("### ✅ Password alterada com sucesso!")
                            st.markdown("Use a nova password no próximo login.")
                            st.markdown('</div>', unsafe_allow_html=True)
                            user["password_hash"] = hash_pwd(new_password)
                            st.session_state.user = user
                            st.balloons()
                        else:
                            st.error("❌ Erro ao alterar password")
        
        st.markdown('</div>', unsafe_allow_html=True)


# ----------------- FORMULÁRIO AVALIAÇÃO -----------------

def evaluation_form(user: dict):
    render_header("Faça avaliações construtivas e ajude a equipa a crescer")

    all_users = get_all_users()
    evaluator_teams = get_user_teams(user)

    tab1, tab2, tab3 = st.tabs(["📝 Nova Avaliação", "📊 Minhas Avaliações", "⏳ Rascunhos"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Configurar avaliação")

        col1, col2 = st.columns(2)

        with col1:
            mode = st.radio(
                "Tipo de avaliação",
                ["🪞 Autoavaliação", "👥 Avaliar colega"],
                horizontal=True,
            )

        evaluatee = None

        if mode == "🪞 Autoavaliação":
            evaluatee = user
            with col2:
                st.info("✅ Autoavaliação selecionada")
        else:
            colleagues = [u for u in all_users if u["email"] != user["email"]]
            
            if not colleagues:
                st.warning("⚠️ Ainda não existem outros utilizadores")
                st.markdown('</div>', unsafe_allow_html=True)
                return

            evaluated_emails = set()
            my_evals = get_evaluations_by_evaluator(user["email"])
            for ev in my_evals:
                evaluated_emails.add(ev["evaluatee"])

            options_data = []
            for c in colleagues:
                already_evaluated = c["email"] in evaluated_emails
                status = "✅" if already_evaluated else "⭕"
                label = f"{status} {c['name']} - {c['team']} ({c['role']})"
                options_data.append({"label": label, "user": c, "evaluated": already_evaluated})

            selected_label = st.selectbox(
                "Pessoa a avaliar",
                [opt["label"] for opt in options_data],
                help="✅ = Já avaliado | ⭕ = Pendente",
            )
            
            evaluatee = next(opt["user"] for opt in options_data if opt["label"] == selected_label)
            already_done = next(opt["evaluated"] for opt in options_data if opt["label"] == selected_label)

            with col2:
                if already_done:
                    st.warning(f"⚠️ Já avaliou **{evaluatee['name']}**")
                else:
                    st.success(f"✅ Primeira avaliação de **{evaluatee['name']}**")

        st.markdown('</div>', unsafe_allow_html=True)

        if evaluatee is None:
            return

        is_intern = evaluatee.get("role") == "ESTAGIARIO"
        evaluatee_teams = get_user_teams(evaluatee)
        shared_teams = evaluator_teams.intersection(evaluatee_teams)
        same_team = len(shared_teams) > 0

        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            role_badge = "badge-warning" if is_intern else "badge-info"
            st.markdown(
                f"<div class='badge {role_badge}'>👤 {evaluatee['role']}</div>",
                unsafe_allow_html=True,
            )
        
        with col2:
            if same_team:
                st.markdown(
                    f"<div class='badge badge-success'>🤝 Equipas: {', '.join(sorted(shared_teams))}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div class='badge badge-warning'>⚠️ Sem equipas em comum</div>",
                    unsafe_allow_html=True,
                )
        
        with col3:
            if is_intern:
                st.markdown(
                    "<div class='badge badge-info'>📋 Avaliação Simplificada</div>",
                    unsafe_allow_html=True,
                )
        
        st.markdown('</div>', unsafe_allow_html=True)

        draft = get_draft(user["email"], evaluatee["email"])
        if draft:
            st.markdown('<div class="alert-info">', unsafe_allow_html=True)
            st.markdown(
                f"💾 **Rascunho encontrado!** Última alteração: {draft['updated_at'][:19].replace('T', ' ')}"
            )
            col1, col2 = st.columns([3, 1])
            with col1:
                load_draft = st.checkbox("Carregar rascunho anterior")
            with col2:
                if st.button("🗑️ Eliminar rascunho"):
                    delete_draft(user["email"], evaluatee["email"])
                    st.success("Rascunho eliminado!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            load_draft = False

        if is_intern:
            total_questions = len(INTERN_COMPETENCIES)
        else:
            total_questions = len(BEHAVIORAL_COMPETENCIES)
            for team in sorted(shared_teams):
                if team in TECHNICAL_COMPETENCIES:
                    total_questions += len(TECHNICAL_COMPETENCIES[team])
            if same_team:
                total_questions += len(OBJECTIVE_COMPETENCIES)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Progresso da avaliação")
        st.progress(0.0, text=f"0 de {total_questions} competências")
        st.markdown('</div>', unsafe_allow_html=True)

        answers = []

        with st.form("avaliacao_form", clear_on_submit=False):
            if is_intern:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 🌱 Competências Comportamentais (Estagiário)")
                
                for i, comp in enumerate(INTERN_COMPETENCIES):
                    with st.expander(f"📌 {comp}", expanded=(i == 0)):
                        cols = st.columns([2, 3])
                        with cols[0]:
                            default_val = 3
                            if load_draft and draft:
                                draft_key = f"intern_{comp}"
                                if draft_key in draft["draft_data"]:
                                    default_val = draft["draft_data"][draft_key]["score"]
                            
                            score = st.slider(
                                "Classificação",
                                1,
                                5,
                                default_val,
                                key=f"intern_{comp}",
                                help="1=Insuficiente | 5=Excelente",
                            )
                            
                            emojis = ["😟", "😐", "🙂", "😊", "🤩"]
                            st.markdown(
                                f"<div style='text-align:center;font-size:2rem;'>{emojis[score-1]}</div>",
                                unsafe_allow_html=True,
                            )
                        
                        with cols[1]:
                            default_comment = ""
                            if load_draft and draft:
                                draft_key = f"intern_{comp}"
                                if draft_key in draft["draft_data"]:
                                    default_comment = draft["draft_data"][draft_key].get("comment", "")
                            
                            comment = st.text_area(
                                "Comentário (opcional)",
                                value=default_comment,
                                key=f"intern_comment_{comp}",
                                height=100,
                            )
                        
                        answers.append(("Comportamentais - Estagiário", comp, score, comment))
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            else:
                tabs = []
                tab_names = ["🌱 Comportamentais"]
                
                if same_team:
                    for team in sorted(shared_teams):
                        if team in TECHNICAL_COMPETENCIES:
                            tab_names.append(f"🛠 {team}")
                    tab_names.append("🎯 Objetivos")
                
                tabs = st.tabs(tab_names)
                
                with tabs[0]:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    
                    for comp in BEHAVIORAL_COMPETENCIES:
                        with st.expander(f"📌 {comp}"):
                            cols = st.columns([2, 3])
                            with cols[0]:
                                default_val = 3
                                if load_draft and draft:
                                    draft_key = f"beh_{comp}"
                                    if draft_key in draft["draft_data"]:
                                        default_val = draft["draft_data"][draft_key]["score"]
                                
                                score = st.slider(
                                    "Classificação",
                                    1,
                                    5,
                                    default_val,
                                    key=f"beh_{comp}",
                                )
                                
                                emojis = ["😟", "😐", "🙂", "😊", "🤩"]
                                st.markdown(
                                    f"<div style='text-align:center;font-size:2rem;'>{emojis[score-1]}</div>",
                                    unsafe_allow_html=True,
                                )
                            
                            with cols[1]:
                                default_comment = ""
                                if load_draft and draft:
                                    draft_key = f"beh_{comp}"
                                    if draft_key in draft["draft_data"]:
                                        default_comment = draft["draft_data"][draft_key].get("comment", "")
                                
                                comment = st.text_area(
                                    "Comentário (opcional)",
                                    value=default_comment,
                                    key=f"beh_comment_{comp}",
                                    height=100,
                                )
                            
                            answers.append(("Comportamentais", comp, score, comment))
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if same_team:
                    tab_idx = 1
                    for team in sorted(shared_teams):
                        if team in TECHNICAL_COMPETENCIES:
                            with tabs[tab_idx]:
                                st.markdown('<div class="card">', unsafe_allow_html=True)
                                
                                for comp in TECHNICAL_COMPETENCIES[team]:
                                    with st.expander(f"🔧 {comp}"):
                                        cols = st.columns([2, 3])
                                        with cols[0]:
                                            default_val = 3
                                            if load_draft and draft:
                                                draft_key = f"tech_{team}_{comp}"
                                                if draft_key in draft["draft_data"]:
                                                    default_val = draft["draft_data"][draft_key]["score"]
                                            
                                            score = st.slider(
                                                "Classificação",
                                                1,
                                                5,
                                                default_val,
                                                key=f"tech_{team}_{comp}",
                                            )
                                            
                                            emojis = ["😟", "😐", "🙂", "😊", "🤩"]
                                            st.markdown(
                                                f"<div style='text-align:center;font-size:2rem;'>{emojis[score-1]}</div>",
                                                unsafe_allow_html=True,
                                            )
                                        
                                        with cols[1]:
                                            default_comment = ""
                                            if load_draft and draft:
                                                draft_key = f"tech_{team}_{comp}"
                                                if draft_key in draft["draft_data"]:
                                                    default_comment = draft["draft_data"][draft_key].get("comment", "")
                                            
                                            comment = st.text_area(
                                                "Comentário (opcional)",
                                                value=default_comment,
                                                key=f"tech_comment_{team}_{comp}",
                                                height=100,
                                            )
                                        
                                        answers.append((f"Técnicas - {team}", comp, score, comment))
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                            tab_idx += 1
                    
                    with tabs[-1]:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        
                        for comp in OBJECTIVE_COMPETENCIES:
                            with st.expander(f"🎯 {comp}"):
                                cols = st.columns([2, 3])
                                with cols[0]:
                                    default_val = 3
                                    if load_draft and draft:
                                        draft_key = f"obj_{comp}"
                                        if draft_key in draft["draft_data"]:
                                            default_val = draft["draft_data"][draft_key]["score"]
                                    
                                    score = st.slider(
                                        "Classificação",
                                        1,
                                        5,
                                        default_val,
                                        key=f"obj_{comp}",
                                    )
                                    
                                    emojis = ["😟", "😐", "🙂", "😊", "🤩"]
                                    st.markdown(
                                        f"<div style='text-align:center;font-size:2rem;'>{emojis[score-1]}</div>",
                                        unsafe_allow_html=True,
                                    )
                                
                                with cols[1]:
                                    default_comment = ""
                                    if load_draft and draft:
                                        draft_key = f"obj_{comp}"
                                        if draft_key in draft["draft_data"]:
                                            default_comment = draft["draft_data"][draft_key].get("comment", "")
                                    
                                    comment = st.text_area(
                                        "Comentário (opcional)",
                                        value=default_comment,
                                        key=f"obj_comment_{comp}",
                                        height=100,
                                    )
                                
                                answers.append(("Objetivos", comp, score, comment))
                        
                        st.markdown('</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                submitted = st.form_submit_button(
                    "💾 Guardar Avaliação Final",
                    use_container_width=True,
                    type="primary",
                )
            
            with col2:
                save_draft_btn = st.form_submit_button(
                    "📝 Guardar Rascunho",
                    use_container_width=True,
                )
            
            with col3:
                cancel = st.form_submit_button(
                    "❌ Cancelar",
                    use_container_width=True,
                )

        if submitted:
            now_iso = datetime.utcnow().isoformat()
            evaluation_type = "SELF" if evaluatee["email"] == user["email"] else "OTHER"

            try:
                for category, competency, score, comment in answers:
                    supabase.table("evaluations").insert({
                        "evaluator": user["email"],
                        "evaluator_team": user.get("team"),
                        "evaluatee": evaluatee["email"],
                        "evaluatee_team": evaluatee.get("team"),
                        "category": category,
                        "competency": competency,
                        "score": score,
                        "comment": comment,
                        "evaluation_type": evaluation_type,
                        "created_at": now_iso,
                        "is_intern": is_intern,
                    }).execute()
                
                delete_draft(user["email"], evaluatee["email"])
                
                st.markdown('<div class="alert-success">', unsafe_allow_html=True)
                st.markdown("### ✅ Avaliação guardada com sucesso!")
                st.markdown(f"A avaliação de **{evaluatee['name']}** foi registada.")
                st.markdown('</div>', unsafe_allow_html=True)
                st.balloons()
            
            except Exception as e:
                st.error(f"❌ Erro ao guardar: {e}")
        
        elif save_draft_btn:
            draft_data = {}
            for category, competency, score, comment in answers:
                key = f"{category.replace(' ', '_')}_{competency}"
                draft_data[key] = {"score": score, "comment": comment}
            
            save_draft(user["email"], evaluatee["email"], draft_data)
            st.success("📝 Rascunho guardado!")
        
        elif cancel:
            st.info("Avaliação cancelada.")

    with tab2:
        show_my_evaluations(user)

    with tab3:
        show_drafts(user)


def show_my_evaluations(user: dict):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Histórico das minhas avaliações")

    my_evals = get_evaluations_by_evaluator(user["email"])

    if not my_evals:
        st.info("📭 Ainda não realizou nenhuma avaliação.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    df = pd.DataFrame(my_evals)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"<div class='metric-card'><h3>{len(df['evaluatee'].unique())}</h3>"
            f"<p>Pessoas avaliadas</p></div>",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"<div class='metric-card'><h3>{len(df)}</h3>"
            f"<p>Total avaliações</p></div>",
            unsafe_allow_html=True,
        )

    with col3:
        avg_score = df["score"].mean()
        st.markdown(
            f"<div class='metric-card'><h3>{avg_score:.2f}</h3>"
            f"<p>Média geral</p></div>",
            unsafe_allow_html=True,
        )

    with col4:
        self_evals = len(df[df["evaluation_type"] == "SELF"])
        st.markdown(
            f"<div class='metric-card'><h3>{self_evals}</h3>"
            f"<p>Autoavaliações</p></div>",
            unsafe_allow_html=True,
        )

    st.markdown("#### 👥 Pessoas que já avaliei")
    
    evaluated_people = df.groupby("evaluatee").agg({
        "score": "mean",
        "created_at": "max",
        "evaluatee_team": "first",
    }).reset_index()

    for _, row in evaluated_people.iterrows():
        user_info = get_user_by_email(row["evaluatee"])
        if user_info:
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"**{user_info['name']}** ({user_info['role']})")
            with col2:
                st.markdown(f"🏢 {row['evaluatee_team']}")
            with col3:
                st.markdown(f"⭐ Média: **{row['score']:.2f}**")
            st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)


def show_drafts(user: dict):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ⏳ Rascunhos guardados")

    try:
        res = supabase.table("evaluation_drafts").select("*").eq(
            "evaluator", user["email"]
        ).execute()
        drafts = res.data
    except:
        st.info("📭 Sem rascunhos guardados.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    if not drafts:
        st.info("📭 Sem rascunhos guardados.")
    else:
        for draft in drafts:
            evaluatee_user = get_user_by_email(draft["evaluatee"])
            if evaluatee_user:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{evaluatee_user['name']}** ({evaluatee_user['role']})")
                with col2:
                    updated = draft["updated_at"][:19].replace("T", " ")
                    st.caption(f"🕒 {updated}")
                with col3:
                    if st.button("🗑️", key=f"delete_{draft['id']}"):
                        delete_draft(user["email"], draft["evaluatee"])
                        st.success("Rascunho eliminado!")
                        st.rerun()
                st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- RESULTADOS (SEM COMENTÁRIOS) -----------------

def my_results(user: dict):
    render_header("Os seus resultados e feedback recebido (anónimo)")

    data = get_evaluations_by_evaluatee(user["email"])

    if not data:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.info("📭 Ainda não existem avaliações registadas para si.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    df = pd.DataFrame(data)
    df_self = df[df["evaluation_type"] == "SELF"] if "evaluation_type" in df.columns else pd.DataFrame()
    df_others = df[df["evaluation_type"] != "SELF"] if "evaluation_type" in df.columns else df

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Visão Geral")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"<div class='metric-card'><h3>{len(df)}</h3>"
            f"<p>Total Avaliações</p></div>",
            unsafe_allow_html=True,
        )

    with col2:
        avg_all = df["score"].mean()
        st.markdown(
            f"<div class='metric-card'><h3>{avg_all:.2f}</h3>"
            f"<p>Média Global</p></div>",
            unsafe_allow_html=True,
        )

    with col3:
        if not df_others.empty:
            avg_others = df_others["score"].mean()
            st.markdown(
                f"<div class='metric-card'><h3>{avg_others:.2f}</h3>"
                f"<p>Média Colegas</p></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='metric-card'><h3>-</h3>"
                "<p>Média Colegas</p></div>",
                unsafe_allow_html=True,
            )

    with col4:
        if not df_self.empty:
            avg_self = df_self["score"].mean()
            st.markdown(
                f"<div class='metric-card'><h3>{avg_self:.2f}</h3>"
                f"<p>Autoavaliação</p></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='metric-card'><h3>-</h3>"
                "<p>Autoavaliação</p></div>",
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)

    if not df_self.empty and not df_others.empty:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔄 Comparação: Autoavaliação vs Feedback")

        comparison = pd.DataFrame({
            "Categoria": df_self.groupby("category")["score"].mean().index,
            "Autoavaliação": df_self.groupby("category")["score"].mean().values,
            "Feedback Colegas": df_others.groupby("category")["score"].mean().values,
        })

        comparison["Diferença"] = comparison["Autoavaliação"] - comparison["Feedback Colegas"]

        st.dataframe(
            comparison.style.background_gradient(
                subset=["Diferença"], cmap="RdYlGn", vmin=-2, vmax=2
            ),
            use_container_width=True,
        )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📈 Médias por Dimensão")

    tab1, tab2 = st.tabs(["📊 Todas", "👥 Colegas"])

    with tab1:
        grouped_all = df.groupby("category")["score"].mean().reset_index()
        grouped_all = grouped_all.sort_values("score", ascending=False)

        for _, row in grouped_all.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{row['category']}**")
            with col2:
                score = row['score']
                color = "#10b981" if score >= 4 else "#f59e0b" if score >= 3 else "#ef4444"
                st.markdown(
                    f"<div style='background:{color};color:white;padding:0.5rem;border-radius:8px;"
                    f"text-align:center;font-weight:700;'>{score:.2f}</div>",
                    unsafe_allow_html=True,
                )

    with tab2:
        if not df_others.empty:
            grouped_others = df_others.groupby("category")["score"].mean().reset_index()
            grouped_others = grouped_others.sort_values("score", ascending=False)

            for _, row in grouped_others.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{row['category']}**")
                with col2:
                    score = row['score']
                    color = "#10b981" if score >= 4 else "#f59e0b" if score >= 3 else "#ef4444"
                    st.markdown(
                        f"<div style='background:{color};color:white;padding:0.5rem;border-radius:8px;"
                        f"text-align:center;font-weight:700;'>{score:.2f}</div>",
                        unsafe_allow_html=True,
                    )
        else:
            st.info("Ainda não tem feedback de colegas.")

    st.markdown('</div>', unsafe_allow_html=True)

    if not df_others.empty:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🌟 Análise de Competências")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### ✅ Top 3 Pontos Fortes")
            top_comp = (
                df_others.groupby("competency")["score"]
                .mean()
                .sort_values(ascending=False)
                .head(3)
            )
            for i, (comp, score) in enumerate(top_comp.items(), 1):
                st.markdown(
                    f"**{i}.** {comp} <span style='color:#10b981;font-weight:700;'>({score:.2f})</span>",
                    unsafe_allow_html=True,
                )

        with col2:
            st.markdown("#### 📈 Top 3 Áreas de Desenvolvimento")
            bottom_comp = (
                df_others.groupby("competency")["score"]
                .mean()
                .sort_values(ascending=True)
                .head(3)
            )
            for i, (comp, score) in enumerate(bottom_comp.items(), 1):
                st.markdown(
                    f"**{i}.** {comp} <span style='color:#f59e0b;font-weight:700;'>({score:.2f})</span>",
                    unsafe_allow_html=True,
                )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="alert-info">', unsafe_allow_html=True)
    st.markdown("ℹ️ **Nota:** Os comentários qualitativos são confidenciais e apenas acessíveis à liderança para desenvolvimento organizacional.")
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- PAINEL CEO -----------------

def ceo_dashboard():
    render_header("Dashboard executivo com análise completa da equipa")

    data = supabase.table("evaluations").select("*").execute().data

    if not data:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.info("📭 Ainda não existem dados de avaliação.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    df = pd.DataFrame(data)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Métricas Globais")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            f"<div class='metric-card'><h3>{len(df)}</h3>"
            f"<p>Total Avaliações</p></div>",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"<div class='metric-card'><h3>{df['evaluatee'].nunique()}</h3>"
            f"<p>Pessoas Avaliadas</p></div>",
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"<div class='metric-card'><h3>{df['evaluator'].nunique()}</h3>"
            f"<p>Avaliadores</p></div>",
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"<div class='metric-card'><h3>{df['score'].mean():.2f}</h3>"
            f"<p>Média Global</p></div>",
            unsafe_allow_html=True,
        )

    with col5:
        completion_rate = (df['evaluatee'].nunique() / len(get_all_users())) * 100
        st.markdown(
            f"<div class='metric-card'><h3>{completion_rate:.0f}%</h3>"
            f"<p>Taxa Conclusão</p></div>",
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Por Pessoa",
        "🏢 Por Equipa",
        "📈 Por Competência",
        "💬 Comentários",
        "👥 Estado",
        "📥 Exportar",
    ])

    with tab1:
        show_ceo_by_person(df)

    with tab2:
        show_ceo_by_team(df)

    with tab3:
        show_ceo_by_competency(df)

    with tab4:
        show_ceo_comments(df)

    with tab5:
        show_ceo_pending(df)

    with tab6:
        show_ceo_export(df)


def show_ceo_by_person(df: pd.DataFrame):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Ranking por Pessoa")

    df_all = df.groupby(["evaluatee", "evaluatee_team"]).agg({
        "score": "mean",
        "evaluator": "count",
    }).reset_index()
    df_all.columns = ["Pessoa", "Equipa", "Média Global", "Nº Avaliações"]
    df_all = df_all.sort_values("Média Global", ascending=False)

    df_others = df[df["evaluation_type"] != "SELF"]
    if not df_others.empty:
        df_others_agg = df_others.groupby(["evaluatee", "evaluatee_team"]).agg({
            "score": "mean",
        }).reset_index()
        df_others_agg.columns = ["Pessoa", "Equipa", "Média Colegas"]
        df_comparison = df_all.merge(df_others_agg, on=["Pessoa", "Equipa"], how="left")
    else:
        df_comparison = df_all

    top3 = df_comparison.head(3)["Pessoa"].tolist()
    bottom3 = df_comparison.tail(3)["Pessoa"].tolist()

    def highlight_rows(row):
        if row["Pessoa"] in top3:
            return ["background-color: #d1fae5"] * len(row)
        elif row["Pessoa"] in bottom3:
            return ["background-color: #fee2e2"] * len(row)
        else:
            return [""] * len(row)

    st.dataframe(
        df_comparison.style.apply(highlight_rows, axis=1).format({
            "Média Global": "{:.2f}",
            "Média Colegas": "{:.2f}",
        }),
        use_container_width=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)


def show_ceo_by_team(df: pd.DataFrame):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🏢 Análise por Equipa")

    team_stats = df.groupby("evaluatee_team").agg({
        "score": ["mean", "std", "count"],
        "evaluatee": "nunique",
    }).reset_index()
    
    team_stats.columns = ["Equipa", "Média", "Desvio Padrão", "Nº Avaliações", "Nº Pessoas"]
    team_stats = team_stats.sort_values("Média", ascending=False)

    st.dataframe(
        team_stats.style.format({
            "Média": "{:.2f}",
            "Desvio Padrão": "{:.2f}",
        }).background_gradient(subset=["Média"], cmap="RdYlGn", vmin=1, vmax=5),
        use_container_width=True,
    )

    st.bar_chart(team_stats.set_index("Equipa")["Média"])

    st.markdown('</div>', unsafe_allow_html=True)


def show_ceo_by_competency(df: pd.DataFrame):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📈 Análise por Competência")

    comp_stats = df.groupby(["category", "competency"]).agg({
        "score": "mean",
    }).reset_index()
    comp_stats.columns = ["Categoria", "Competência", "Média"]
    comp_stats = comp_stats.sort_values("Média", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ Top 10")
        top10 = comp_stats.head(10)
        for i, row in enumerate(top10.itertuples(), 1):
            st.markdown(
                f"**{i}.** {row.Competência} "
                f"<span style='color:#10b981;font-weight:700;'>({row.Média:.2f})</span>",
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("#### 📉 Bottom 10")
        bottom10 = comp_stats.tail(10)
        for i, row in enumerate(bottom10.itertuples(), 1):
            st.markdown(
                f"**{i}.** {row.Competência} "
                f"<span style='color:#ef4444;font-weight:700;'>({row.Média:.2f})</span>",
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)


def show_ceo_comments(df: pd.DataFrame):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💬 Todos os Comentários")
    
    st.markdown('<div class="alert-warning">', unsafe_allow_html=True)
    st.markdown("⚠️ **Confidencial:** Esta informação é exclusiva para liderança.")
    st.markdown('</div>', unsafe_allow_html=True)

    df_comments = df[df["comment"].notna() & (df["comment"] != "")].copy()

    if df_comments.empty:
        st.info("📭 Sem comentários.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    all_evaluatees = sorted(df_comments["evaluatee"].unique())
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_person = st.selectbox(
            "Filtrar por pessoa",
            ["Todas"] + all_evaluatees,
        )
    
    with col2:
        show_self = st.checkbox("Incluir autoavaliações", value=True)

    if selected_person != "Todas":
        df_comments = df_comments[df_comments["evaluatee"] == selected_person]
    
    if not show_self:
        df_comments = df_comments[df_comments["evaluation_type"] != "SELF"]

    st.markdown(f"**Total:** {len(df_comments)} comentários")
    st.markdown("---")

    for evaluatee in df_comments["evaluatee"].unique():
        df_person = df_comments[df_comments["evaluatee"] == evaluatee]
        
        user_info = get_user_by_email(evaluatee)
        person_name = user_info["name"] if user_info else evaluatee
        person_role = user_info["role"] if user_info else "N/A"
        
        with st.expander(f"👤 **{person_name}** ({person_role}) — {len(df_person)} comentários"):
            for idx, row in df_person.iterrows():
                evaluator_info = get_user_by_email(row["evaluator"])
                evaluator_name = evaluator_info["name"] if evaluator_info else row["evaluator"]
                
                is_self = row["evaluation_type"] == "SELF"
                badge_text = "🪞 Autoavaliação" if is_self else f"👤 {evaluator_name}"
                
                st.markdown(f"<div class='badge badge-info'>{badge_text}</div>", unsafe_allow_html=True)
                st.markdown(f"**{row['category']}** — {row['competency']} (⭐ **{row['score']}**/5)")
                st.markdown(f"> _{row['comment']}_")
                st.caption(f"📅 {row['created_at'][:19].replace('T', ' ')}")
                st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)


def show_ceo_pending(df: pd.DataFrame):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 👥 Estado das Avaliações")

    all_users = get_all_users()
    all_emails = {u["email"]: u["name"] for u in all_users}

    evaluated = set(df["evaluatee"].unique())
    not_evaluated = set(all_emails.keys()) - evaluated

    evaluators = set(df["evaluator"].unique())
    not_evaluating = set(all_emails.keys()) - evaluators

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📭 Sem Avaliações Recebidas")
        if not_evaluated:
            for email in not_evaluated:
                user_info = next((u for u in all_users if u["email"] == email), None)
                if user_info:
                    st.markdown(
                        f"<div class='badge badge-danger'>❌ {user_info['name']}</div>",
                        unsafe_allow_html=True,
                    )
        else:
            st.success("✅ Todos avaliados!")

    with col2:
        st.markdown("#### 📝 Não Avaliaram")
        if not_evaluating:
            for email in not_evaluating:
                user_info = next((u for u in all_users if u["email"] == email), None)
                if user_info:
                    st.markdown(
                        f"<div class='badge badge-warning'>⚠️ {user_info['name']}</div>",
                        unsafe_allow_html=True,
                    )
        else:
            st.success("✅ Todos avaliaram!")

    st.markdown('</div>', unsafe_allow_html=True)


def show_ceo_export(df: pd.DataFrame):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📥 Exportar Dados")

    col1, col2 = st.columns(2)

    with col1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📄 Descarregar CSV",
            data=csv,
            file_name=f"avaliacoes_360_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        try:
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Avaliações")
            excel_data = output.getvalue()
            
            st.download_button(
                label="📊 Descarregar Excel",
                data=excel_data,
                file_name=f"avaliacoes_360_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except:
            st.caption("Excel indisponível")

    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- MAIN -----------------

def main():
    seed_users()

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login_screen()
        return

    user = st.session_state.user

    with st.sidebar:
        st.markdown("### 👤 Utilizador")
        st.markdown(f"**{user['name']}**")
        st.markdown(f"`{user['role']}`")
        
        if user.get("team"):
            st.markdown(f"🏢 **{user['team']}**")
        
        st.markdown("---")

        my_evals = get_evaluations_by_evaluator(user["email"])
        received_evals = get_evaluations_by_evaluatee(user["email"])
        
        st.markdown("### 📊 Estatísticas")
        st.metric("Avaliações feitas", len(my_evals))
        st.metric("Avaliações recebidas", len(received_evals))
        
        if received_evals:
            avg = pd.DataFrame(received_evals)["score"].mean()
            st.metric("Média recebida", f"{avg:.2f}")
        
        st.markdown("---")

        menu_options = ["📝 Avaliar", "📊 Resultados", "🔑 Password"]
        if user["role"] == "CEO":
            menu_options.append("🎯 Painel CEO")
        
        choice = st.radio("**Menu**", menu_options)

        st.markdown("---")
        
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.user = None
            st.rerun()
        
        st.markdown("---")
        st.caption("© 2025 Startup Leiria")

    if choice == "📝 Avaliar":
        evaluation_form(user)
    elif choice == "📊 Resultados":
        my_results(user)
    elif choice == "🔑 Password":
        change_password_screen(user)
    elif choice == "🎯 Painel CEO":
        ceo_dashboard()


if __name__ == "__main__":
    main()
