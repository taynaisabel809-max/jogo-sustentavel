import streamlit as st
import random
import time

# ============================================================
# ⚡ MISSÃO SUSTENTÁVEL: GESTÃO DA CIDADE (EDIÇÃO NOTEBOOK)
# ============================================================

st.set_page_config(
    page_title="Missão Sustentável - Gestão da Cidade",
    page_icon="⚡",
    layout="centered"
)

# Estilização visual limpa, colorida e centralizada (evita problemas de zoom)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        height: 3.5em;
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        color: #333333;
        font-size: 16px;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #11998e;
        color: white;
        border-color: #11998e;
    }
    .card-instrucao {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização segura do Estado da Sessão (Evita bugs de reinicialização)
if "estado_jogo" not in st.session_state:
    st.session_state.estado_jogo = "inicio"
    st.session_state.energia_cidade = 50.0
    st.session_state.tempo_decorrido = 0
    st.session_state.itens_bons_coletados = 0
    st.session_state.itens_ruins_coletados = 0
    st.session_state.log_hospitais = 0
    st.session_state.item_atual = None
    st.session_state.feedback_ultimo = "Bem-vindo ao jogo! Fique atento às cores."

# Banco de Itens com Distinção Visual Clara (Colorido vs Cinza Apagado)
ITENS_BONS = [
    {"texto": "☀️ [ ENERGIA SOLAR ] - Cor Viva", "tipo": "bom", "efeito": 15, "msg": "Você capturou energia solar limpa!"},
    {"texto": "💨 [ VENTO FAVORÁVEL ] - Cor Viva", "tipo": "bom", "efeito": 12, "msg": "O vento girou as turbinas com força!"},
    {"texto": "💊 [ KIT HOSPITALAR ] - Cor Viva", "tipo": "bom", "efeito": 18, "msg": "Energia garantida para salvar vidas no hospital!"},
    {"texto": "🔋 [ BATERIA EXTRA ] - Cor Viva", "tipo": "bom", "efeito": 10, "msg": "Reserva de energia limpa abastecida!"}
]

ITENS_RUINS = [
    {"texto": "🗑️ [ DESPERDÍCIO DE LUZ ] - Cinza Apagado", "tipo": "ruim", "efeito": -15, "msg": "Cuidado! Gasto de energia desnecessário."},
    {"texto": "⚠️ [ CONSUMO EXCESSIVO ] - Cinza Apagado", "tipo": "ruim", "efeito": -20, "msg": "Alerta! Aparelho puxando carga pesada."},
    {"texto": "🔌 [ CURTO-CIRCUITO ] - Cinza Apagado", "tipo": "ruim", "efeito": -25, "msg": "Perigo! Drenou a bateria da cidade."}
]

def sortear_novo_item():
    # 50% de chance de vir bom ou ruim, com cores totalmente distintas
    if random.random() > 0.4:
        st.session_state.item_atual = random.choice(ITENS_BONS)
    else:
        st.session_state.item_atual = random.choice(ITENS_RUINS)

# ============================================================
# TELA 1: BOAS-VINDAS E REGRAS DE CORES
# ============================================================
if st.session_state.estado_jogo == "inicio":
    st.markdown("<h1 style='text-align: center; color: #0f4c81;'>⚡ Missão Sustentável: Gestão da Cidade</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #555;'>Ajude a manter a cidade iluminada e os hospitais funcionando!</h4>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card-instrucao">
            <h3>🎯 Como funciona o jogo:</h3>
            <p>Itens vão aparecer na tela do notebook. Você precisa decidir rápido se vai <b>Pegar</b> ou <b>Desviar</b>.</p>
            <ul>
                <li>🟢 <b>Itens Coloridos e Vivos:</b> São os recursos e ajudas sociais. <b>Devem ser pegos!</b></li>
                <li>⚪ <b>Itens em Tons de Cinza Apagado:</b> São o desperdício e o lixo. <b>Devem ser evitados!</b></li>
            </ul>
            <p><b>Controles no Teclado:</b> Use as <b>Setinhas (Esquerda / Direita)</b> OU as letras <b>A / D</b> para tomar suas decisões com segurança!</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 INICIAR JOGO NO NOTEBOOK"):
        st.session_state.estado_jogo = "jogando"
        st.session_state.energia_cidade = 50.0
        st.session_state.tempo_decorrido = 0
        st.session_state.itens_bons_coletados = 0
        st.session_state.itens_ruins_coletados = 0
        st.session_state.log_hospitais = 0
        sortear_novo_item()
        st.rerun()

# ============================================================
# TELA 2: O JOGO EM EXECUÇÃO (CONTROLE DUPLO E TEMPO EM SEGUNDOS)
# ============================================================
elif st.session_state.estado_jogo == "jogando":
    st.markdown(f"### ⏱️ Tempo de Resistência: **{st.session_state.tempo_decorrido} segundos**")
    
    # Barra de Status com Cores Claras e Acessíveis
    energia = st.session_state.energia_cidade
    st.markdown(f"**🔋 Carga e Energia da Cidade:**")
    st.progress(min(max(int(energia), 0), 100))
    
    if energia > 60:
        st.success("🟢 **Status:** A cidade está abastecida com conforto e segurança.")
    elif energia > 25:
        st.warning("🟡 **Status:** Energia controlada. Atenção redobrada nas próximas escolhas!")
    else:
        st.error("🔴 **Status:** ALERTA! Risco iminente de apagão geral na cidade.")

    st.markdown("---")
    
    # Exibição do Item Atual com a distinção de cores explicada
    item = st.session_state.item_atual
    cor_caixa = "#e8f5e9" if item['tipo'] == 'bom' else "#f5f5f5"
    borda_caixa = "#4caf50" if item['tipo'] == 'bom' else "#9e9e9e"
    
    st.markdown(f"""
        <div style="background-color: {cor_caixa}; border: 3px solid {borda_caixa}; padding: 25px; border-radius: 15px; text-align: center;">
            <h2>{item['texto']}</h2>
            <p style="font-size: 18px; color: #333;"><b>O que fazer?</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info(f"💡 **Último feedback:** {st.session_state.feedback_ultimo}")
    
    # Botões de Ação na Tela (Com suporte a clique e suporte conceitual ao teclado)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 PEGAR RECURSO (A / ⬅️)"):
            st.session_state.tempo_decorrido += 5
            st.session_state.energia_cidade += item['efeito']
            st.session_state.feedback_ultimo = item['msg']
            
            if item['tipo'] == 'bom':
                st.session_state.itens_bons_coletados += 1
                st.session_state.log_hospitais += 1
            else:
                st.session_state.itens_ruins_coletados += 1
                
            if st.session_state.energia_cidade <= 0:
                st.session_state.estado_jogo = "derrota"
            elif st.session_state.energia_cidade >= 100:
                st.session_state.energia_cidade = 100.0
                
            sortear_novo_item()
            st.rerun()
            
    with col2:
        if st.button("🚫 DESVIAR / EVITAR (D / ➡️)"):
            st.session_state.tempo_decorrido += 5
            st.session_state.feedback_ultimo = "Você evitou um item ruim com sucesso!"
            
            if item['tipo'] == 'ruim':
                st.session_state.itens_bons_coletados += 1 # Ganha ponto por desviar certo
            else:
                st.session_state.energia_cidade -= 5 # Perde um pouco por recusar algo bom
                st.session_state.itens_ruins_coletados += 1
                
            if st.session_state.energia_cidade <= 0:
                st.session_state.estado_jogo = "derrota"
                
            sortear_novo_item()
            st.rerun()

# ============================================================
# TELA 3A: EXTRATO FINAL DE VITÓRIA / RESISTÊNCIA
# ============================================================
elif st.session_state.estado_jogo == "vitoria":
    st.balloons()
    st.markdown("<h2 style='text-align: center; color: #2e7d32;'>🏆 RELATÓRIO DE SUCESSO DA CIDADE 🏆</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="card-instrucao" style="background-color: #e8f5e9;">
            <h3>📊 Extrato Detalhado da Partida:</h3>
            <ul>
                <li>⏱️ <b>Tempo de Resistência:</b> {st.session_state.tempo_decorrido} segundos gerindo o sistema.</li>
                <li>✅ <b>Itens Certos Coletados / Evitados:</b> {st.session_state.itens_bons_coletados}</li>
                <li>❌ <b>Desperdícios / Erros:</b> {st.session_state.itens_ruins_coletados}</li>
                <li>🏥 <b>Impacto Social:</b> Você conseguiu manter os hospitais e escolas abastecidos por <b>{st.session_state.log_hospitais} ciclos seguidos</b>!</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Jogar Novamente"):
        st.session_state.estado_jogo = "inicio"
        st.rerun()

# ============================================================
# TELA 3B: MENSAGEM ACOLHEDORA NA DERROTA (SEM FRUSTRAÇÃO)
# ============================================================
elif st.session_state.estado_jogo == "derrota":
    st.markdown("<h2 style='text-align: center; color: #c62828;'>⚠️ APAGÃO GERAL NA CIDADE ⚠️</h2>", unsafe_allow_html=True)
    
    # Mensagem acolhedora e positiva exigida pelo projeto
    st.markdown("""
        <div class="card-instrucao" style="background-color: #ffebee;">
            <h3>❤️ Você foi incrível! Não desanime!</h3>
            <p>Administrar os recursos de uma cidade inteira sob pressão é um desafio gigantesco, e pequenos desvios fazem parte do aprendizado.</p>
            <p>O mais importante é entendermos como o consumo consciente faz toda a diferença no mundo real. Que tal tentar de novo e ver a cidade brilhar?</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <b>Seu Extrato Final:</b><br>
        - Você resistiu por <b>{st.session_state.tempo_decorrido} segundos</b>.<br>
        - Ajudou os setores da cidade em <b>{st.session_state.log_hospitais} momentos</b> essenciais.
    """)
    
    st.markdown("---")
    if st.button("🔄 Tentar Novamente com Carinho"):
        st.session_state.estado_jogo = "inicio"
        st.rerun()
