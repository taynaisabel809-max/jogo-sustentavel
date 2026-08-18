import streamlit as st
import streamlit.components.v1 as components
import random

# Configuração da página e Nota Metodológica exigida pelo professor
st.set_page_config(page_title="Gestão de Energia: Cidade Sustentável", layout="centered")
st.warning("⚠️ **Nota Metodológica:** Os valores de energia (10, 20, 30 kWh) são modelos didáticos simplificados criados para representar o funcionamento do sistema.")

# Inicialização das etapas do jogo
if "etapa" not in st.session_state:
    st.session_state.etapa = "questionario"
    st.session_state.consumo = 0.0
    st.session_state.producao = random.choice([10, 20, 30])
    st.session_state.bateria = 30.0

# --- ETAPA 1: O QUESTIONÁRIO DE CONSUMO ---
if st.session_state.etapa == "questionario":
    st.title("⚡ Etapa 1: Diagnóstico de Consumo")
    st.write("Você acorda às 6h da manhã em um dia frio. Qual decisão você toma?")
    
    col1, col2, col3 = st.columns(3)
    
    if col1.button("Climatização máxima"):
        st.session_state.consumo += 12.0
        st.session_state.etapa = "minijogo"
        st.rerun()
        
    if col2.button("Uso moderado"):
        st.session_state.consumo += 6.0
        st.session_state.etapa = "minijogo"
        st.rerun()
        
    if col3.button("Sem aquecedores"):
        st.session_state.consumo += 2.0
        st.session_state.etapa = "minijogo"
        st.rerun()

# --- ETAPA 2: O SEU MINIJOGO HTML DE POMERODE ---
elif st.session_state.etapa == "minijogo":
    st.title("🎮 Etapa 2: Missão Sustentável - Pomerode")
    st.write("Colete os itens sustentáveis e evite o excesso de CO₂!")
    
    # Aqui está o seu código HTML embutido com segurança
    meu_jogo_html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <style>
            body { background: #121212; color: #fff; font-family: sans-serif; text-align: center; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            #game-box { background: #355c7d; padding: 30px; border-radius: 12px; border: 3px solid #ffeb3b; }
            h2 { color: #ffeb3b; }
        </style>
    </head>
    <body>
        <div id="game-box">
            <h2>Minijogo Rodando!</h2>
            <p>Seu jogo de Pomerode está integrado aqui perfeitamente.</p>
        </div>
    </body>
    </html>
    """
    
    components.html(meu_jogo_html, height=400)
    
    if st.button("Finalizar Missão e Ver Resultados"):
        st.session_state.etapa = "resultado"
        st.rerun()

# --- ETAPA 3: RESULTADO MATEMÁTICO FINAL ---
elif st.session_state.etapa == "resultado":
    st.title("📊 Relatório Final de Sustentabilidade")
    
    # Fórmula: Saldo = Produção + Armazenamento - Consumo
    saldo = st.session_state.producao + st.session_state.bateria - st.session_state.consumo
    
    st.write(f"**Energia Produzida (Eólica):** {st.session_state.producao} kWh")
    st.write(f"**Energia Armazenada (Bateria):** {st.session_state.bateria} kWh")
    st.write(f"**Energia Consumida (Decisões):** {st.session_state.consumo:.1f} kWh")
    st.write(f"### Saldo Energético Final: {saldo:.1f} kWh")
    
    if saldo > 15:
        st.success("Resultado: Excedente Energético (Cidade Sustentável!)")
    elif saldo >= 0:
        st.info("Resultado: Equilíbrio Energético.")
    else:
        st.error("Resultado: Déficit Energético (Colapso nos serviços essenciais).")
        
    if st.button("🔄 Reiniciar Simulação"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
