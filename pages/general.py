# general.py
# Healthflow Médica AI — Real API integration with Gemini
# Architecture: Uses actual Gemini API calls with proper error handling

import os, json, re, html
from typing import List, Optional
import streamlit as st
from pydantic import BaseModel, Field, ValidationError

# --- Gemini SDK ---
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

BRAND = "#0295a8"

st.set_page_config(
    page_title="Healthflow Médica AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- Global CSS (clean, pro) -----------------
st.markdown(f"""
<style>
:root {{
  --brand: {BRAND};
  --ink: #0f172a;
  --muted: #475569;
}}
html, body, [data-testid="stAppViewContainer"] {{
  background: #ffffff;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}
h1,h2,h3,h4,h5 {{ letter-spacing: .2px; }}
p, li {{ line-height: 1.6; color: #0f172a; }}
.small-muted {{ color: #475569; margin-top: -2px; }}
.header-wrap {{ text-align:center; margin: 6px 0 2px 0; }}
.brand-title {{
  font-size: 34px; font-weight: 800; color: var(--brand); margin: 10px 0 4px 0;
}}
.brand-sub {{ color: #64748b; font-size: 14px; }}
.card {{
  border: 1px solid #e6edf2; border-radius: 14px; background: #fff;
  box-shadow: 0 2px 10px rgba(2,6,23,0.04); padding: 16px 18px; margin-bottom: 14px;
}}
.card-head {{ display:flex; align-items:center; gap:10px; margin-bottom: 8px; }}
.icon {{
  width: 28px; height: 28px; border-radius: 999px; background: rgba(2,149,168,.12); color: var(--brand);
  display:flex; align-items:center; justify-content:center; font-weight:700;
}}
.card-title {{ font-weight: 700; color: #0f172a; font-size: 16px; }}
.kicker {{ text-align:center; color:#334155; margin: 6px 0 16px 0; }}
.section-title {{ text-align:center; color: var(--brand); font-size: 22px; font-weight: 800; margin: 6px 0 10px 0; }}
ul.clean {{ margin: 0.25rem 0 0; padding-left: 1.1rem; }}
ul.clean li {{ margin: 2px 0; }}
hr.divider {{
  border:none; height:1px; background:linear-gradient(90deg, rgba(2,6,23,0.08), rgba(2,6,23,0));
  margin: 12px 0;
}}
.input-row {{ max-width: 860px; margin: 8px auto 6px auto; display:flex; gap:10px; }}
[data-testid="stTextInput"] input {{
  height: 46px !important; border-radius: 10px !important; border: 1px solid #e5e7eb !important;
}}
.primary-btn button {{
  height: 46px !important; border-radius: 10px !important; background: var(--brand) !important; color: white !important; border: none !important;
}}
.note {{
  border-radius: 10px; border: 1px dashed #d7e3ea; background: #f7fafb; color: #334155; padding: 10px 14px; font-size: .92rem;
}}
.api-warning {{
  border-radius: 10px; border: 1px solid #fbbf24; background: #fef3c7; color: #92400e; padding: 12px 16px; margin: 10px 0;
}}
</style>
""", unsafe_allow_html=True)



# ----------------- Pydantic Models -----------------
class RecommendedTreatment(BaseModel):
    nome: str
    quando_por_que: str
    objetivos: List[str] = Field(min_items=3)
    consideracoes_chave: List[str] = Field(min_items=3)
    modalidades_tipicas: List[str] = Field(min_items=2)

class Terapeuticas(BaseModel):
    radioterapia: str = ""
    cirurgia: str = ""
    quimioterapia: str = ""

class MedicalCards(BaseModel):
    descricao_mecanismos: str
    sintomas_comuns: List[str] = Field(min_items=5)
    sintomas_incomuns: List[str] = Field(min_items=4)
    causas_risco: List[str] = Field(min_items=6)
    evolucao_natural: str
    complicacoes: List[str] = Field(min_items=5)
    recomendadas: List[RecommendedTreatment] = Field(min_items=3, max_items=3)
    terapeuticas: Terapeuticas = Field(default_factory=Terapeuticas)

# ----------------- Helpers -----------------
def _normalize_gemini_text(resp) -> str:
    """Extract text from various Gemini response formats."""
    text = getattr(resp, "text", None) or getattr(resp, "output_text", None)
    if not text and getattr(resp, "candidates", None):
        parts = getattr(resp.candidates[0].content, "parts", []) or []
        text = "".join(getattr(p, "text", "") for p in parts)
    if not text:
        return ""
    
    # Clean up markdown code blocks if present
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    # Extract JSON from response
    m = re.search(r"\{[\s\S]*\}", text)
    return m.group(0) if m else text

def _ensure_min_list(lst: List[str], min_len: int, fillers: List[str]) -> List[str]:
    """Ensure list has minimum number of items."""
    out = [s for s in lst if s and s.strip()]
    i = 0
    while len(out) < min_len and i < len(fillers):
        out.append(fillers[i]); i += 1
    return out

def _html_list(items: List[str]) -> str:
    """Convert list to HTML unordered list."""
    if not items:
        return "<em>—</em>"
    lis = "".join([f"<li>{html.escape(i)}</li>" for i in items])
    return f'<ul class="clean">{lis}</ul>'

def build_prompt(condition: str) -> str:
    """Build the prompt for Gemini API."""
    return f"""
You are a clinical assistant. Output ONLY valid JSON (no prose, no markdown, no backticks).
If the input isn't clearly a medical condition, return: {{"error":"non-medical"}}

GOALS
- Fill EVERY field with substantive, safe, evidence-based content.
- Portuguese (pt-PT). Patient-friendly but clinically accurate. No brand names, no URLs.
- Use general medical knowledge when specifics are uncertain.

MINIMA & LENGTH
- descricao_mecanismos: 110–180 palavras (parágrafo coerente de fisiopatologia/mecanismos).
- evolucao_natural: 70–120 palavras (trajetória temporal; estágios/agravantes/controlo).
- sintomas_comuns: ≥ 5; sintomas_incomuns: ≥ 4; causas_risco: ≥ 6; complicacoes: ≥ 5.
- recomendadas: exatamente 3 objetos, cada um com:
  - nome (específico para a condição)
  - quando_por_que (2–4 frases; elegibilidade e racional)
  - objetivos (≥ 3)
  - consideracoes_chave (≥ 3)
  - modalidades_tipicas (≥ 2, genéricas)

STRICT JSON SCHEMA:
{{
  "descricao_mecanismos": "string 110–180 palavras",
  "sintomas_comuns": ["...", "..."],
  "sintomas_incomuns": ["...", "..."],
  "causas_risco": ["...", "..."],
  "evolucao_natural": "string 70–120 palavras",
  "complicacoes": ["...", "..."],
  "recomendadas": [
    {{
      "nome": "string",
      "quando_por_que": "2–4 frases",
      "objetivos": ["...", "...", "..."],
      "consideracoes_chave": ["...", "...", "..."],
      "modalidades_tipicas": ["...", "..."]
    }},
    {{ "nome": "...", "quando_por_que": "...", "objetivos": ["..."], "consideracoes_chave": ["..."], "modalidades_tipicas": ["..."] }},
    {{ "nome": "...", "quando_por_que": "...", "objetivos": ["..."], "consideracoes_chave": ["..."], "modalidades_tipicas": ["..."] }}
  ],
  "terapeuticas": {{
    "radioterapia": "string",
    "cirurgia": "string",
    "quimioterapia": "string"
  }}
}}

User condition: "{condition}"
"""

# ----------------- ChatModel & ChatSession -----------------
class ChatModel:
    """Wrapper around google-genai Client."""
    def __init__(self, client: Optional[genai.Client], model_id: str):
        self.client = client
        self.model_id = model_id

    @classmethod
    def from_pretrained(cls, model_id: str):
        """Initialize model with API key."""
        if not GEMINI_API_KEY:
            return cls(client=None, model_id=model_id)
        
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            return cls(client=client, model_id=model_id)
        except Exception as e:
            st.error(f"Erro ao inicializar cliente Gemini: {e}")
            return cls(client=None, model_id=model_id)

class ChatSession:
    """Manages conversation with Gemini API."""
    def __init__(self, model: ChatModel):
        self.model = model
        self.last_raw_text: Optional[str] = None
        self.last_object: Optional[MedicalCards] = None

    def analyze(self, condition: str) -> MedicalCards:
        """Analyze medical condition using Gemini API."""
        
        # Check if API client is available
        if not self.model.client:
            raise Exception("API Key não configurada. Configure GEMINI_API_KEY no ficheiro .env")

        cfg = types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=2500,
            response_mime_type="application/json",
        )

        prompt = build_prompt(condition)
        attempts = 2
        last_text: Optional[str] = None

        for attempt in range(attempts):
            try:
                effective_prompt = prompt if attempt == 0 else (
                    "Converte o texto abaixo em JSON VÁLIDO que cumpra EXACTAMENTE o SCHEMA, "
                    "em pt-PT, sem markdown/backticks, garantindo mínimos de comprimento/contagem e sem campos vazios.\n\n"
                    f"TEXTO:\n{last_text or ''}"
                )
                
                # Make actual API call
                resp = self.model.client.models.generate_content(
                    model=self.model.model_id,
                    contents=effective_prompt,
                    config=cfg,
                )
                
                text = _normalize_gemini_text(resp).strip()
                self.last_raw_text = text
                
                if not text:
                    last_text = "(resposta vazia)"
                    continue

                # Try to parse JSON response
                try:
                    obj = MedicalCards.model_validate_json(text)
                except ValidationError:
                    try:
                        payload = json.loads(text)
                        # Check for error response
                        if isinstance(payload, dict) and payload.get("error") == "non-medical":
                            raise Exception(f"'{condition}' não parece ser uma condição médica válida.")
                        obj = MedicalCards.model_validate(payload)
                    except Exception as parse_error:
                        if attempt == attempts - 1:
                            raise Exception(f"Erro ao processar resposta da API: {str(parse_error)}")
                        last_text = text
                        continue

                # Post-guards for minima
                obj.sintomas_comuns = _ensure_min_list(
                    obj.sintomas_comuns, 5, 
                    ["Cansaço persistente", "Intolerância a esforços", "Mal-estar geral"]
                )
                obj.sintomas_incomuns = _ensure_min_list(
                    obj.sintomas_incomuns, 4, 
                    ["Sintomas atípicos inespecíficos", "Manifestações raras"]
                )
                obj.causas_risco = _ensure_min_list(
                    obj.causas_risco, 6, 
                    ["Exposição ocupacional", "Fatores hormonais", "Predisposição genética"]
                )
                obj.complicacoes = _ensure_min_list(
                    obj.complicacoes, 5, 
                    ["Comprometimento funcional prolongado", "Impacto na qualidade de vida"]
                )
                
                # Ensure exactly 3 recommended treatments
                while len(obj.recomendadas) < 3:
                    obj.recomendadas.append(
                        RecommendedTreatment(
                            nome="Intervenção multimodal de suporte",
                            quando_por_que="Indicada para melhorar controlo sintomático e adesão terapêutica.",
                            objetivos=["Reduzir sintomas", "Melhorar qualidade de vida", "Prevenir agudizações"],
                            consideracoes_chave=["Adequar à função orgânica", "Educação do doente", "Seguimento regular"],
                            modalidades_tipicas=["Plano de autocuidado estruturado", "Revisão farmacoterapêutica"],
                        )
                    )

                self.last_object = obj
                return obj
                
            except Exception as e:
                if attempt == attempts - 1:
                    raise Exception(f"Erro na chamada API (tentativa {attempt + 1}/{attempts}): {str(e)}")
                continue

        raise Exception("Falha ao obter resposta válida da API após múltiplas tentativas")

# ----------------- SESSION STATE -----------------
defaults = {
    "query_input": "asma",
    "current_topic": "asma",
    "data": None,
    "loading": False,
    "error": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Initialize model and session
if "session" not in st.session_state:
    st.session_state.chat_model = ChatModel.from_pretrained("gemini-2.0-flash-exp")
    st.session_state.session = ChatSession(model=st.session_state.chat_model)

# ----------------- Header -----------------
st.markdown('<div class="header-wrap">', unsafe_allow_html=True)
try:
    st.image("healthflow.png", width=72)
except:
    st.markdown("🩺")
st.markdown('<div class="brand-title">Healthflow Médica AI</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-sub">Insights detalhados sobre doenças (Português - pt-PT)</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Show API warning if no key
if not GEMINI_API_KEY:
    st.markdown("""
    <div class="api-warning">
        <strong>⚠️ API Key não configurada</strong><br>
        Para utilizar a análise em tempo real, configure GEMINI_API_KEY no ficheiro .env
    </div>
    """, unsafe_allow_html=True)

# ----------------- Input row -----------------
cA, cB, cC = st.columns([5,1.1,1.1])
with cA:
    st.session_state.query_input = st.text_input(
        "Pesquisar condição",
        value=st.session_state.query_input,
        label_visibility="collapsed",
        placeholder="ex.: asma, cancro da mama, DPOC, insuficiência cardíaca…"
    )
with cB:
    analyze = st.button("Analisar", type="primary", use_container_width=True)
with cC:
    clear = st.button("Limpar", use_container_width=True)

# --- Actions ---
if clear:
    st.session_state.update({
        "query_input": "asma", 
        "current_topic": "asma", 
        "data": None, 
        "error": None
    })
    st.rerun()

if analyze:
    topic = (st.session_state.query_input or "").strip() or "asma"
    st.session_state.update({
        "loading": True, 
        "error": None, 
        "current_topic": topic, 
        "data": None
    })
    
    try:
        with st.spinner(f"A analisar '{topic}' com Gemini AI..."):
            obj: MedicalCards = st.session_state.session.analyze(topic)
            st.session_state.data = obj.model_dump()
        st.toast(f"✅ Análise de '{topic}' concluída!", icon="✅")
        st.session_state.loading = False
        st.rerun()
    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.loading = False

# ----------------- Render -----------------
topic = st.session_state.current_topic
payload = st.session_state.data
error = st.session_state.error

st.markdown(f"<p class='kicker'>Análise: <strong style='color:{BRAND}'>{html.escape(topic.title())}</strong></p>", unsafe_allow_html=True)

if st.session_state.loading:
    st.info("⏳ Aguarde, a processar...")
    
if error:
    st.error(f"❌ {error}")

# Only show data if we have it
if payload:
    # ----------------- Render helpers -----------------
    def card(title: str, body_html: str, icon="·"):
        """Generic card that accepts HTML body."""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="card-head"><div class="icon">{icon}</div><div class="card-title">{html.escape(title)}</div></div>', unsafe_allow_html=True)
        st.markdown(body_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    def card_para(title: str, paragraph: str, icon="·"):
        card(title, f"<div>{html.escape(paragraph)}</div>", icon=icon)

    def card_list(title: str, items: List[str], icon="·"):
        card(title, _html_list(items), icon=icon)

    # ----------------- Cards Layout -----------------
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1: card_para("Descrição & Mecanismos", payload.get("descricao_mecanismos","—"), icon="ℹ️")
    with r1c2: card_list("Sintomas Comuns", payload.get("sintomas_comuns",[]), icon="💚")
    with r1c3: card_list("Sintomas Incomuns", payload.get("sintomas_incomuns",[]), icon="🧪")

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1: card_list("Causas & Fatores de Risco", payload.get("causas_risco",[]), icon="🧬")
    with r2c2: card_para("Evolução Natural", payload.get("evolucao_natural","—"), icon="📈")
    with r2c3: card_list("Complicações Possíveis", payload.get("complicacoes",[]), icon="⚠️")

    st.markdown("<div class='section-title'>Top 3 Tratamentos Recomendados</div>", unsafe_allow_html=True)
    rt1, rt2, rt3 = st.columns(3)
    recs = payload.get("recomendadas", [])[:3] if isinstance(payload.get("recomendadas"), list) else []
    for col, rec in zip([rt1, rt2, rt3], recs):
        with col:
            if rec:
                body = (
                    f"<p class='small-muted'><strong>Quando/porquê:</strong> {html.escape(rec.get('quando_por_que','—'))}</p>"
                    f"<p><strong>Objetivos</strong></p>{_html_list(rec.get('objetivos', []))}"
                    f"<p><strong>Considerações chave</strong></p>{_html_list(rec.get('consideracoes_chave', []))}"
                    f"<p><strong>Modalidades típicas</strong></p>{_html_list(rec.get('modalidades_tipicas', []))}"
                )
                card(rec.get('nome','Tratamento'), body, icon="💊")

    st.markdown("""
    <div class="note">
    <strong>Nota:</strong> Conteúdos para literacia em saúde; não substituem aconselhamento médico.
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("👆 Introduza uma condição médica e clique em 'Analisar' para começar.")