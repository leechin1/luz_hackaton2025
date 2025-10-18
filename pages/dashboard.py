# dashboard.py
# Oncology Patient Dashboard — Static, zero-input, information-rich
# All content is placeholders for demonstration (no uploads, no inputs)

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta


st.sidebar.image("healthflow.png", width=160)


# -----------------------#
#   CONFIG & THEME       #
# -----------------------#

logo = open("healthflow.png", "rb").read()
st.set_page_config(
    page_title="Healthlow | Under myLuz",
    page_icon= logo,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Subtle CSS polish (cards, chips, typography)
st.markdown("""
<style>
:root { --ink: #0f172a; --muted:#475569; }
.card {
  border:1px solid rgba(2,6,23,0.08);
  border-radius:16px;
  padding:16px 18px;
  background:#fff;
  box-shadow:0 2px 10px rgba(2,6,23,0.06);
}
.card + .card { margin-top:14px; }
.card-title { display:flex; align-items:center; gap:8px; margin:0 0 6px 0; font-size:1.05rem; font-weight:700; color:var(--ink); }
.accent { width:8px; height:20px; border-radius:999px; display:inline-block; }
.chip {
  display:inline-block; padding:6px 10px; border-radius:999px;
  background:rgba(14,165,233,0.08); color:#0ea5e9; font-weight:600;
  border:1px solid rgba(14,165,233,0.2); font-size:0.85rem; margin:2px 6px 2px 0;
}
.kpi {
  border-radius:16px; padding:14px; background:linear-gradient(180deg,#f8fafc, #ffffff);
  border:1px solid rgba(2,6,23,0.06);
}
hr.div { border:none; height:1px; background:linear-gradient(90deg, rgba(2,6,23,0.08), rgba(2,6,23,0)); margin:8px 0 16px; }
.small { color: var(--muted); font-size:0.92rem; }
</style>
""", unsafe_allow_html=True)

def chip(text, color="#0ea5e9"):
    st.markdown(
        f"""<span class="chip" style="color:{color};
        border-color:{color}33; background:{color}14;">{text}</span>""",
        unsafe_allow_html=True
    )

def card(title, body_md, accent="#0ea5e9"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="card-title"><span class="accent" style="background:{accent};"></span>{title}</div>',
        unsafe_allow_html=True
    )
    st.markdown(body_md)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------#
#   PLACEHOLDER DATA     #
# -----------------------#
patient = {
    "id": "P-001",
    "name": "Ana Martins",
    "dob": "1977-05-04",
    "diagnosis": "Carcinoma da mama (RH+, HER2-), Estádio II (T2N1M0)",
    "comorbidities": ["Hipertensão arterial", "Dislipidemia"],
    "allergies": ["Penicilina"],
    "genomics": {"BRCA1": "Negativo", "BRCA2": "Negativo", "PIK3CA": "Mutação"},
    "baseline": {"PS": "ECOG 1", "weight_kg": 64.0, "height_cm": 168},
}

# Fixed therapy schedule (no inputs)
start_date = (datetime.today() - timedelta(days=28)).date()

# --- FASE ATUAL: TIMELINE (mais completa com exemplos de quimioterapia) ---
timeline_rows = []

# Linha ATUAL (exemplo): ddAC q14d → Paclitaxel semanal
# ddAC (Doxorrubicina + Ciclofosfamida) q14d, 4 ciclos
for c in range(1, 5):
    ini = start_date + timedelta(days=14 * (c - 1))
    fim = ini + timedelta(days=14)
    timeline_rows.append({
        "Fase": "Linha atual: ddAC (q14d)",
        "Ciclo": c,
        "Início": ini,
        "Fim": fim
    })

# Paclitaxel semanal, 12 semanas
pac_start = start_date + timedelta(days=14 * 4)  # após 4 ciclos ddAC (8 semanas)
for c in range(1, 13):
    ini = pac_start + timedelta(days=7 * (c - 1))
    fim = ini + timedelta(days=7)
    timeline_rows.append({
        "Fase": "Linha atual: Paclitaxel (semanal)",
        "Ciclo": c,
        "Início": ini,
        "Fim": fim
    })

# EXEMPLOS ALTERNATIVOS (não aplicados) — mostrados para literacia do doente
# Alternativa 1: TC (Docetaxel + Ciclofosfamida) q21d x4
for c in range(1, 5):
    ini = start_date + timedelta(days=21 * (c - 1))
    fim = ini + timedelta(days=21)
    timeline_rows.append({
        "Fase": "Exemplo: TC (q21d)",
        "Ciclo": c,
        "Início": ini,
        "Fim": fim
    })

# Alternativa 2: EC → D (Epirrubicina + Ciclofosfamida q21d x4 → Docetaxel q21d x4)
for c in range(1, 5):
    ini = start_date + timedelta(days=21 * (c - 1))
    fim = ini + timedelta(days=21)
    timeline_rows.append({
        "Fase": "EC (q21d)",
        "Ciclo": c,
        "Início": ini,
        "Fim": fim
    })
ec_end = start_date + timedelta(days=21 * 4)
for c in range(1, 5):
    ini = ec_end + timedelta(days=21 * (c - 1))
    fim = ini + timedelta(days=21)
    timeline_rows.append({
        "Fase": " Docetaxel (q21d)",
        "Ciclo": c,
        "Início": ini,
        "Fim": fim
    })

# Alternativa 3: AC-T clássico (AC q21d x4 → Paclitaxel semanal x12)
for c in range(1, 5):
    ini = start_date + timedelta(days=21 * (c - 1))
    fim = ini + timedelta(days=21)
    timeline_rows.append({
        "Fase": "AC (q21d)",
        "Ciclo": c,
        "Início": ini,
        "Fim": fim
    })
ac_end = start_date + timedelta(days=21 * 4)
for c in range(1, 13):
    ini = ac_end + timedelta(days=7 * (c - 1))
    fim = ini + timedelta(days=7)
    timeline_rows.append({
        "Fase": "Paclitaxel (semanal)",
        "Ciclo": c,
        "Início": ini,
        "Fim": fim
    })

tl_df = pd.DataFrame(timeline_rows)
tl_df["Início"] = pd.to_datetime(tl_df["Início"])
tl_df["Fim"] = pd.to_datetime(tl_df["Fim"])

side_effects = pd.DataFrame([
    {"Efeito secundário": "Náuseas e vómitos", "Grau (CTCAE)": "1–2", "Prevenção/gestão": "Antieméticos programados; hidratação; dividir refeições."},
    {"Efeito secundário": "Alopecia", "Grau (CTCAE)": "2", "Prevenção/gestão": "Touca de arrefecimento (se disponível); aconselhamento; próteses capilares."},
    {"Efeito secundário": "Neutropenia", "Grau (CTCAE)": "1", "Prevenção/gestão": "Profilaxia com G-CSF; vigilância de febre; medidas de higiene."},
    {"Efeito secundário": "Neuropatia periférica", "Grau (CTCAE)": "0–1", "Prevenção/gestão": "Monitorização semanal; ajuste de dose se sintomas progredirem."},
])

consults_df = pd.DataFrame([
    {
        "Data": "2025-08-02",
        "Tipo": "Oncologia Médica",
        "Sumário detalhado": (
            "Consulta de confirmação diagnóstica com revisão de biópsia (RH+, HER2-), estadiamento clínico T2N1. "
            "Discussão de objetivos: redução tumoral pré-cirúrgica e preservação de qualidade de vida. "
            "Apresentado esquema neoadjuvante AC seguido de taxano; consentimento informado obtido."
        ),
        "Documento": "Acesso interno: Consulta_Oncologia_2025-08-02",
    },
    {
        "Data": "2025-08-20",
        "Tipo": "Enfermagem",
        "Sumário detalhado": (
            "Sessão de educação terapêutica: preparação para quimioterapia, profilaxia de náuseas, cuidados com cateter, "
            "lista de sinais de alarme (febre ≥ 38°C; hemorragia; dispneia; dor não controlada) e plano SOS."
        ),
        "Documento": "Acesso interno: Consulta_Enfermagem_2025-08-20",
    },
    {
        "Data": "2025-09-10",
        "Tipo": "Oncologia Médica",
        "Sumário detalhado": (
            "Reavaliação após 2 ciclos AC: tolerância globalmente boa (náuseas G1, neutropenia G1). "
            "Manter antiemese programada; considerar touca de arrefecimento; planear transição para paclitaxel semanal "
            "após ciclo 4, com vigilância de neuropatia periférica."
        ),
        "Documento": "Acesso interno: Consulta_Oncologia_2025-09-10",
    },
]).sort_values("Data", ascending=False)

doctor_notes = [
    "Manter hidratação ≥ 2L/dia nos 3 dias pós-infusão; utilizar esquema antiemético conforme instruções impressas.",
    "Em caso de febre ≥ 38°C, NÃO aguardar: contactar linha direta do serviço e dirigir-se ao SU indicado.",
    "Evitar aglomerações e contacto com doentes infecciosos durante períodos de neutropenia prevista (Dias +7 a +14).",
    "Para punhos/solas dormentes (sinais de neuropatia), registar início/gravidade; comunicar se interferir com ADLs.",
    "Verificar tensão arterial 2–3x/semana devido a hipertensão prévia; levar registo à próxima consulta.",
]

# -----------------------#
#        SIDEBAR         #
# -----------------------#
st.sidebar.title("Painel do Paciente")
st.sidebar.markdown(f"**{patient['name']}**  \nID: {patient['id']}")
st.sidebar.caption(f"Nasc.: {patient['dob']}  \nDiagnóstico: {patient['diagnosis']}")
st.sidebar.markdown("---")
st.sidebar.caption("Apoio a uma terapêutica segura e informada personalizada a cada doente, porque cada caso é um caso.")

# -----------------------#
#        HEADER          #
# -----------------------#
left, mid, right = st.columns([1.6, 1, 1])
with left:
    st.markdown(f"## {patient['name']}")
    st.caption(f"Estádio atual: II • ECOG: {patient['baseline']['PS']}")
    chip("Oncologia - Apoio ao Tratamento", "#6366f1")
with mid:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Esquema", "ddAC → Paclitaxel")
    st.metric("Ciclos previstos", "4 ddAC + 12 T")
    st.markdown('</div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Próxima janela terapêutica", (datetime.today() + timedelta(days=6)).date().isoformat())
    st.metric("Alergias", ", ".join(patient["allergies"]))
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="div" />', unsafe_allow_html=True)

# -----------------------#
#           TABS         #
# -----------------------#
tab_overview, tab_phase, tab_history, tab_notes = st.tabs(
    ["Visão Geral", "Fase Atual", "Histórico Clínico", "Notas do Médico"]
)

# ---------- VISÃO GERAL ----------
with tab_overview:
    col1, col2 = st.columns([1.15, 1])
    with col1:
        card(
            "Explicação da doença",
            """
**Carcinoma da mama (RH+, HER2-)** caracteriza-se por células tumorais com recetores hormonais positivos e ausência de sobre-expressão HER2.  
Este subtipo tende a responder a **terapêutica hormonal** e a beneficiar de **quimioterapia** em contextos de maior risco (p.ex., N1).  
O objetivo clínico engloba **redução tumoral pré-cirúrgica**, **controlo locorregional** e **diminuição do risco de recorrência sistémica**, 
preservando **qualidade de vida** e função em atividades diárias.
            """,
        )
        card(
            "Mecanismos de ação da doença",
            """
A proliferação neoplásica resulta de **desregulação de vias hormonais (ER/PR)** e alterações de sinalização (p.ex., **PI3K/AKT**).  
A presença de mutação **PIK3CA** pode influenciar sensibilidade a determinadas terapias e requer **monitorização metabólica/neurológica**.  
A disseminação linfática (N1) justifica uma abordagem **sistémica** precoce para reduzir carga tumoral antes da cirurgia.
            """,
        )
    with col2:
        card(
            "Objetivos do tratamento",
            """
- **Resposta tumoral objetiva** por critérios **RECIST** até à 1.ª reavaliação  
- **Toxicidade controlada (≤ Grau 2 CTCAE)** com medidas de suporte adequadas  
- **Qualidade de vida estável/melhorada** (p.ex., EORTC QLQ-C30)  
- **Preparação cirúrgica** com potencial para cirurgia conservadora consoante resposta
            """,
            accent="#22c55e",
        )
        st.markdown("##### Comorbilidades relevantes")
        for c in patient["comorbidities"]: chip(c, "#f59e0b")
        st.markdown("##### Perfil molecular")
        for k, v in patient["genomics"].items(): chip(f"{k}: {v}", "#14b8a6")

# ---------- FASE ATUAL ----------
with tab_phase:
    st.caption("Medicação + SOS destacados, explicação e racional no contexto do perfil clínico, efeitos secundários e timeline da quimioterapia.")

    # Medicação + SOS (highlight)
    card(
        "Medicação prescrita + SOS (Destaque)",
        """
**Esquema atual:** **ddAC → Paclitaxel semanal**  
**Prescrições ativas (exemplo):**  
- **Doxorrubicina** — 60 mg/m² IV — q14d (ciclos 1–4, dose-dense)  
- **Ciclofosfamida** — 600 mg/m² IV — q14d (ciclos 1–4, dose-dense)  
- **Paclitaxel** — 80 mg/m² IV — semanal (12 semanas)  

**SOS (utilização conforme sintomas):**  
- **Ondansetrona 8 mg (oral)** — náuseas/vómitos  
- **Loperamida 2 mg (oral)** — diarreia  

> **Atenção:** Em **febre ≥ 38°C**, **hemorragia ativa** ou **dor não controlada**, contactar imediatamente a equipa.
        """,
        accent="#dc2626",
    )

    # Explicação da terapêutica
    card(
        "Explicação da terapêutica",
        """
O regime **dose-dense AC** seguido de **paclitaxel semanal** combina **antraciclinas** e **alquilantes** numa fase inicial,
maximizando **citotoxicidade** e redução tumoral rápida, e transita para **taxano** para consolidar resposta antes da cirurgia.  
A estratégia sequencial pretende **aumentar probabilidade de resposta patológica** e facilitar **cirurgia conservadora**.
        """,
    )

    # Porquê no contexto do perfil do doente + comorbilidades
    card(
        "Porquê esta terapêutica no contexto do perfil clínico e comorbilidades",
        """
O perfil **RH+/HER2-** com **N1** beneficia de abordagem **neoadjuvante**.  
A mutação **PIK3CA** reforça vigilância de **toxicidade metabólica/neurológica**;  
com **hipertensão** e **dislipidemia**, reforça-se:  
- Monitorização de **tensão arterial** e **risco cardiovascular** (especial atenção às antraciclinas)  
- Otimização de **antiemese** e educação para **sinais de alarme**  
- Apoio nutricional e **atividade física leve** para manter o estado geral
        """,
        accent="#f59e0b",
    )

    # Efeitos secundários
    card(
        "Efeitos secundários da terapêutica (exemplos e medidas)",
        "Abaixo apresenta-se um quadro de toxicidades frequentes e medidas recomendadas.",
    )
    st.dataframe(side_effects, use_container_width=True, hide_index=True)

    # --- Timeline da terapêutica (atual + exemplos) ---
    fig = px.timeline(
        tl_df,
        x_start="Início",
        x_end="Fim",
        y="Fase",
        color="Fase",
        hover_data=["Ciclo"],
        title="Timeline da terapêutica — linha atual e exemplos (quimioterapia)"
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(margin=dict(l=0, r=0, t=60, b=0), height=420)
    st.plotly_chart(fig, use_container_width=True)

# ---------- HISTÓRICO CLÍNICO ----------
with tab_history:
    st.caption("Consultas passadas com **sumários extensos** e referência a documentos clínicos (placeholders).")
    card(
        "Resumo do histórico clínico",
        f"""
**Paciente:** {patient['name']} (ID {patient['id']}), {patient['dob']}.  
**Diagnóstico:** Carcinoma da mama **RH+ / HER2-**, Estádio **II (T2N1M0)**.  
**Comorbilidades:** {', '.join(patient['comorbidities'])}. **Alergias:** {', '.join(patient['allergies'])}.  
**Perfil molecular:** BRCA1/2 negativos; **PIK3CA mutado**.

**Linha terapêutica atual (neoadjuvante):** esquema **dose-dense AC** (q14d, 4 ciclos) seguido de **Paclitaxel semanal** (12 semanas).  
Até à última reavaliação, a doente completou **3 ciclos ddAC** com **tolerância globalmente boa**: náuseas G1 controladas, **neutropenia G1** sem febre, alopecia esperada; sem neuropatia relevante.  
**Educação de enfermagem** realizada (cuidados com cateter, plano antiemético, sinais de alarme). **Plano SOS** fornecido.

**Objetivos em curso:** reduzir volume tumoral para otimizar cirurgia conservadora; **limitar toxicidade ≤ G2 (CTCAE)**; manter **qualidade de vida**.  
**Próximos passos previstos:** completar ddAC, transitar para **Paclitaxel semanal**, re-estadiar por imagem (RECIST) e discutir estratégia cirúrgica; radioterapia e **terapêutica hormonal adjuvante** serão consideradas conforme resposta patológica e risco residual.

**Sinais de segurança reforçados ao doente:** febre **≥ 38°C**, hemorragia, dispneia, dor torácica ou **dor não controlada** → contacto imediato com a equipa.  
Este resumo agrega decisões clínicas, educação e tolerância terapêutica até à data, servindo de guia para o percurso terapêutico e literacia do doente/família.
        """,
    )
    st.markdown("#### Consultas passadas (sumários + documentos)")
    st.dataframe(
        consults_df[["Data", "Tipo", "Sumário detalhado", "Documento"]],
        use_container_width=True, hide_index=True
    )

# ---------- NOTAS DO Medico ----------
with tab_notes:
    st.caption("Mensagens personalizadas do médico para orientação prática do dia-a-dia.")
    card(
        "Notas do Médico",
        """
- **Hidratação e nutrição:** manter **≥ 2L/dia** nos 3 dias pós-quimioterapia; escolher refeições pequenas e frequentes.  
- **Antieméticos:** tomar conforme **plano programado** mesmo que as náuseas sejam leves; isto previne agravamento.  
- **Sinais de alarme:** febre **≥ 38°C**, arrepios, hemorragia, falta de ar, dor torácica ou **dor não controlada** → **contactar de imediato**.  
- **Atividade física leve:** caminhar 15–20 minutos/dia pode reduzir **fadiga** e melhorar humor/sono.  
- **Higiene oral:** escova macia, colutório sem álcool; reportar **úlceras** ou dor oral.  
- **Neuropatia:** se notar formigueiro/dormência que interfira em tarefas (abotoar camisa, segurar objetos), **informar** a equipa.  
- **Medicação habitual:** trazer lista atualizada e medições de **tensão arterial**; registar valores 2–3x/semana.  
- **Rede de apoio:** é normal precisar de ajuda; combine tarefas (compras, transportes) com familiares/amigos nos dias pós-infusão.
        """,
        accent="#6366f1",
    )

st.markdown('<hr class="div" />', unsafe_allow_html=True)
st.caption("© 2025 HealthFlow (under myLuz)— Dashboard ilustrativo para apoio à literacia do doente. Este material não substitui aconselhamento médico.")
st.caption("Para mais informações ligue 217 104 400")
