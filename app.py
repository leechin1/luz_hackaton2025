# app.py
# Healthflow Landing Page - Beautiful entry point with mission statement

import streamlit as st
from datetime import datetime

BRAND = "#0295a8"
ACCENT = "#10b981"

st.set_page_config(
    page_title="Healthflow | Informação Médica Clara",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful landing page
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

:root {{
  --brand: {BRAND};
  --accent: {ACCENT};
  --ink: #0f172a;
  --muted: #64748b;
  --bg-soft: #f8fafc;
}}

* {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

html, body, [data-testid="stAppViewContainer"] {{
  background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
}}

.hero-section {{
  text-align: center;
  padding: 60px 20px 40px;
  max-width: 900px;
  margin: 0 auto;
}}

.logo-wrapper {{
  margin-bottom: 24px;
}}

.hero-title {{
  font-size: 52px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--brand) 0%, var(--accent) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 16px 0;
  letter-spacing: -1px;
}}

.hero-subtitle {{
  font-size: 22px;
  color: var(--muted);
  font-weight: 400;
  line-height: 1.6;
  margin: 0 auto 20px;
  max-width: 700px;
}}

.mission-card {{
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(2,149,168,0.08);
  margin: 40px auto;
  max-width: 800px;
  border: 1px solid rgba(2,149,168,0.1);
}}

.mission-title {{
  font-size: 28px;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 20px 0;
  text-align: center;
}}

.mission-text {{
  font-size: 16px;
  line-height: 1.8;
  color: var(--ink);
  margin-bottom: 16px;
}}

.highlight {{
  color: var(--brand);
  font-weight: 600;
}}

.pillars-section {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin: 40px auto;
  max-width: 1100px;
  padding: 0 20px;
}}

.pillar-card {{
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  transition: transform 0.2s, box-shadow 0.2s;
}}

.pillar-card:hover {{
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(2,149,168,0.12);
}}

.pillar-icon {{
  font-size: 48px;
  margin-bottom: 16px;
}}

.pillar-title {{
  font-size: 18px;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 12px 0;
}}

.pillar-text {{
  font-size: 14px;
  color: var(--muted);
  line-height: 1.6;
}}

.cta-section {{
  text-align: center;
  margin: 60px auto 40px;
  max-width: 900px;
  padding: 0 20px;
}}

.cta-title {{
  font-size: 32px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 32px;
}}

.cta-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin-top: 32px;
}}

.cta-card {{
  background: white;
  border-radius: 20px;
  padding: 40px 32px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}}

.cta-card::before {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--brand), var(--accent));
  transform: scaleX(0);
  transition: transform 0.3s;
}}

.cta-card:hover {{
  border-color: var(--brand);
  box-shadow: 0 12px 32px rgba(2,149,168,0.15);
  transform: translateY(-2px);
}}

.cta-card:hover::before {{
  transform: scaleX(1);
}}

.cta-icon {{
  font-size: 56px;
  margin-bottom: 20px;
}}

.cta-card-title {{
  font-size: 24px;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 12px 0;
}}

.cta-card-desc {{
  font-size: 15px;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 24px;
}}

.footer {{
  text-align: center;
  padding: 40px 20px;
  color: var(--muted);
  font-size: 14px;
  border-top: 1px solid #e5e7eb;
  margin-top: 60px;
}}

.stats-bar {{
  display: flex;
  justify-content: center;
  gap: 48px;
  margin: 40px auto;
  padding: 32px;
  background: linear-gradient(135deg, rgba(2,149,168,0.05) 0%, rgba(16,185,129,0.05) 100%);
  border-radius: 16px;
  max-width: 800px;
}}

.stat-item {{
  text-align: center;
}}

.stat-number {{
  font-size: 36px;
  font-weight: 800;
  color: var(--brand);
  display: block;
  margin-bottom: 4px;
}}

.stat-label {{
  font-size: 13px;
  color: var(--muted);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}

/* Hide Streamlit branding */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="hero-section">', unsafe_allow_html=True)

# Try to show logo, fallback to emoji
try:
    st.image("healthflow.png", width=120)
except:
    st.markdown('<div class="logo-wrapper">🩺</div>', unsafe_allow_html=True)

st.markdown('''
<h1 class="hero-title">Healthflow</h1>
<p class="hero-subtitle">
Transformando informação médica complexa em conhecimento claro e acessível para pacientes e profissionais
</p>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Stats Bar
st.markdown('''
<div class="stats-bar">
  <div class="stat-item">
    <span class="stat-number">100%</span>
    <span class="stat-label">Transparente</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">24/7</span>
    <span class="stat-label">Disponível</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">AI+</span>
    <span class="stat-label">Inteligência</span>
  </div>
</div>
''', unsafe_allow_html=True)

# Mission Card
st.markdown('''
<div class="mission-card">
  <h2 class="mission-title">💡 A Nossa Missão</h2>
  <p class="mission-text">
    A <span class="highlight">transparência médica</span> não é apenas um direito — é a base para decisões informadas 
    que podem salvar vidas. Quando os pacientes compreendem verdadeiramente a sua condição, tratamentos e opções, 
    tornam-se parceiros ativos no seu processo de cura.
  </p>
  <p class="mission-text">
    O Healthflow nasceu da convicção de que <span class="highlight">informação médica de qualidade</span> não deve ser 
    um privilégio, mas sim acessível a todos. Utilizamos inteligência artificial avançada para traduzir conceitos 
    médicos complexos em linguagem clara, mantendo sempre o rigor científico.
  </p>
  <p class="mission-text">
    Cada paciente merece entender o que está a acontecer com o seu corpo, conhecer as suas opções de tratamento, 
    e sentir-se <span class="highlight">confiante e capacitado</span> para fazer perguntas e tomar decisões ao lado 
    dos seus profissionais de saúde.
  </p>
</div>
''', unsafe_allow_html=True)

# Pillars Section
st.markdown('''
<div class="pillars-section">
  <div class="pillar-card">
    <div class="pillar-icon">🔍</div>
    <h3 class="pillar-title">Informação Clara</h3>
    <p class="pillar-text">
      Convertemos terminologia médica complexa em explicações compreensíveis, 
      sem perder precisão científica.
    </p>
  </div>
  
  <div class="pillar-card">
    <div class="pillar-icon">🤝</div>
    <h3 class="pillar-title">Decisões Partilhadas</h3>
    <p class="pillar-text">
      Capacitamos pacientes e familiares com conhecimento para participarem 
      ativamente nas decisões de saúde.
    </p>
  </div>
  
  <div class="pillar-card">
    <div class="pillar-icon">🎯</div>
    <h3 class="pillar-title">Personalização</h3>
    <p class="pillar-text">
      Cada condição é única. Fornecemos informação contextualizada ao perfil 
      individual de cada paciente.
    </p>
  </div>
  
  <div class="pillar-card">
    <div class="pillar-icon">🛡️</div>
    <h3 class="pillar-title">Segurança</h3>
    <p class="pillar-text">
      Toda a informação é baseada em evidências científicas atualizadas e 
      guidelines internacionais.
    </p>
  </div>
</div>
''', unsafe_allow_html=True)

# CTA Section
st.markdown('''
<div class="cta-section">
  <h2 class="cta-title">Explore as Nossas Ferramentas</h2>
</div>
''', unsafe_allow_html=True)

# Navigation Cards
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('''
    <div class="cta-card">
      <div class="cta-icon">🩺</div>
      <h3 class="cta-card-title">Healthflow Médica AI</h3>
      <p class="cta-card-desc">
        Pesquise qualquer condição médica e obtenha explicações detalhadas sobre mecanismos, 
        sintomas, tratamentos e evolução clínica em português.
      </p>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("Aceder à Médica AI", use_container_width=True, type="primary", key="btn1"):
        st.switch_page("pages/general.py")

with col2:
    st.markdown('''
    <div class="cta-card">
      <div class="cta-icon">🧬</div>
      <h3 class="cta-card-title">Painel Oncologia</h3>
      <p class="cta-card-desc">
        Dashboard interativo com informações personalizadas do paciente oncológico, 
        timeline de tratamentos e acompanhamento detalhado.
      </p>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("Aceder ao Painel", use_container_width=True, type="primary", key="btn2"):
        st.switch_page("pages/dashboard.py")

# Why it Matters Section
st.markdown('<div style="margin-top: 60px;">', unsafe_allow_html=True)

st.markdown('''
<div class="mission-card" style="background: linear-gradient(135deg, rgba(2,149,168,0.03) 0%, rgba(16,185,129,0.03) 100%);">
  <h2 class="mission-title">🌟 Porquê é que isto Importa</h2>
  <p class="mission-text">
    <strong>Estudos demonstram que pacientes informados:</strong>
  </p>
  <p class="mission-text">
    ✓ Apresentam <span class="highlight">maior adesão aos tratamentos</span> (até 40% de melhoria)<br>
    ✓ Reportam <span class="highlight">melhor qualidade de vida</span> durante e após o tratamento<br>
    ✓ Experimentam <span class="highlight">menos ansiedade e stress</span> relacionados com o diagnóstico<br>
    ✓ Fazem <span class="highlight">perguntas mais relevantes</span> aos seus médicos<br>
    ✓ Sentem-se mais <span class="highlight">confiantes e no controlo</span> da sua jornada de saúde
  </p>
  <p class="mission-text">
    A literacia em saúde não substitui o aconselhamento médico — <span class="highlight">complementa-o</span>. 
    Um paciente informado é um parceiro mais eficaz no processo terapêutico.
  </p>
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
current_year = datetime.now().year
st.markdown(f'''
<div class="footer">
  <p><strong>Healthflow</strong> — Informação médica clara e acessível</p>
  <p style="margin-top: 8px;">
    © {current_year} Healthflow (under myLuz) • Demonstração educacional<br>
    A informação fornecida não substitui consulta médica profissional
  </p>
  <p style="margin-top: 16px; font-size: 13px;">
    Para mais informações: <strong>217 104 400</strong>
  </p>
</div>
''', unsafe_allow_html=True)