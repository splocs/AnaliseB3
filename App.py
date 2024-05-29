import streamlit as st
import pandas as pd
import yfinance as yf
from PIL import Image
import plotly.graph_objects as go
from datetime import date
import openai
import matplotlib.pyplot as plt
import ta
from ta.utils import dropna
import numpy as np

# Configurando a API da OpenAI
openai.api_key = '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'

# Configurando a largura da página
st.set_page_config(layout="wide")

# Função para configurar o gráfico
def configurar_grafico(fig):
    fig.update_layout(dragmode='pan')
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['zoom2d'],
        'scrollZoom': True
    }
    return config

# Função para formatar a data
def formatar_data(data):
    return data.strftime('%d-%m-%Y')

# Dicionário de tradução de nomes das colunas
traducao = {
    'Date': 'Data',
    'Open': 'Abertura',
    'High': 'Alta',
    'Low': 'Baixa',
    'Close': 'Fechamento',
    'Adj Close': 'Fechamento Ajustado',
    'Volume': 'Volume'
}

# Função para pegar os dados das ações
@st.cache
def pegar_dados_acoes():
    path = 'https://raw.githubusercontent.com/splocs/meu-repositorio/main/acoes.csv'
    return pd.read_csv(path, delimiter=';')

# Função para pegar os valores online
@st.cache
def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, DATA_INICIO, DATA_FIM, progress=False)
    df.reset_index(inplace=True)
    return df

# Função para obter dados financeiros de uma ação ou FII
@st.cache
def get_data(ticker):
    data = yf.download(ticker, start="2000-01-01")
    return data

# Função para plotar gráficos de indicadores técnicos
def plot_technical_indicators(data, ticker):
    # Preparar os dados
    data = dropna(data)
    
    # Cálculo dos indicadores técnicos
    data['SMA'] = ta.trend.sma_indicator(data['Close'], window=50)
    data['EMA'] = ta.trend.ema_indicator(data['Close'], window=50)
    data['MACD'] = ta.trend.macd(data['Close'])
    data['MACD_signal'] = ta.trend.macd_signal(data['Close'])
    data['Bollinger_High'] = ta.volatility.bollinger_hband(data['Close'])
    data['Bollinger_Low'] = ta.volatility.bollinger_lband(data['Close'])
    data['RSI'] = ta.momentum.rsi(data['Close'])
    
    st.write(f"### Indicadores Técnicos para {ticker}")
    
    # Plot SMA and EMA
    st.write("#### SMA e EMA")
    fig, ax = plt.subplots()
    ax.plot(data.index, data['Close'], label='Close')
    ax.plot(data.index, data['SMA'], label='SMA')
    ax.plot(data.index, data['EMA'], label='EMA')
    ax.set_title(f"SMA e EMA - {ticker}")
    ax.legend()
    st.pyplot(fig)
    
    # Plot MACD
    st.write("#### MACD")
    fig, ax = plt.subplots()
    ax.plot(data.index, data['MACD'], label='MACD')
    ax.plot(data.index, data['MACD_signal'], label='Signal Line')
    ax.set_title(f"MACD - {ticker}")
    ax.legend()
    st.pyplot(fig)
    
    # Plot Bollinger Bands
    st.write("#### Bandas de Bollinger")
    fig, ax = plt.subplots()
    ax.plot(data.index, data['Close'], label='Close')
    ax.plot(data.index, data['Bollinger_High'], label='Bollinger High')
    ax.plot(data.index, data['Bollinger_Low'], label='Bollinger Low')
    ax.set_title(f"Bandas de Bollinger - {ticker}")
    ax.legend()
    st.pyplot(fig)
    
    # Plot RSI
    st.write("#### Índice de Força Relativa (RSI)")
    fig, ax = plt.subplots()
    ax.plot(data.index, data['RSI'], label='RSI')
    ax.axhline(y=70, color='r', linestyle='--')
    ax.axhline(y=30, color='g', linestyle='--')
    ax.set_title(f"RSI - {ticker}")
    ax.legend()
    st.pyplot(fig)

# Função para exibir informações fundamentalistas
def display_fundamentals(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    st.write(f"### Informações Fundamentalistas para {ticker}")
    st.write(f"**Nome:** {info.get('shortName', 'N/A')}")
    st.write(f"**Setor:** {info.get('sector', 'N/A')}")
    st.write(f"**Indústria:** {info.get('industry', 'N/A')}")
    st.write(f"**Resumo:** {info.get('longBusinessSummary', 'N/A')}")
    st.write(f"**Valor de Mercado:** {info.get('marketCap', 'N/A')}")
    st.write(f"**Beta:** {info.get('beta', 'N/A')}")
    st.write(f"**Dividendo Anual:** {info.get('dividendYield', 'N/A')}")

# Função para obter resposta do chatbot
def get_chatbot_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Definindo data de início e fim
DATA_INICIO = '2017-01-01'
DATA_FIM = date.today().strftime('%Y-%m-%d')

# Logo
logo_path = "logo.png"
logo = Image.open(logo_path)

# Exibir o logo no aplicativo Streamlit
st.image(logo, width=250)

# Exibir o logo na sidebar
st.sidebar.image(logo, width=150)

st.title('Análise de Ações e FIIs')

# Criando a sidebar
st.sidebar.markdown('Escolha a ação')
n_dias = st.sidebar.slider('Quantidade de dias de previsão', 30, 365)

# Pegando os dados das ações
df = pegar_dados_acoes()
acao = df['snome']

nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:', acao)
df_acao = df[df['snome'] == nome_acao_escolhida]
sigla_acao_escolhida = df_acao.iloc[0]['sigla_acao']
sigla_acao_escolhida += '.SA'

# Pegando os valores online
df_valores = pegar_valores_online(sigla_acao_escolhida)

st.subheader('Tabela de Valores - ' + nome_acao_escolhida)

# Renomeando as colunas usando o dicionário de tradução
df_valores = df_valores.rename(columns=traducao)

# Convertendo a coluna "Data" para o formato desejado
df_valores['Data'] = df_valores['Data'].dt.strftime('%d-%m-%Y')
st.write(df_valores.tail(40))

# Criando gráfico de preços
st.subheader('Gráfico de Preços')
fig = go.Figure()

fig.add_trace(go.Scatter(x=df_valores['Data'],
                         y=df_valores['Fechamento'],
                         name='Preço Fechamento',
                         line_color='yellow'))

fig.add_trace(go.Scatter(x=df_valores['Data'],
                         y=df_valores['Abertura'],
                         name='Preço Abertura',
                         line_color='blue'))

config = configurar_grafico(fig)
st.plotly_chart(fig, use_container_width=False, config=config)

# Calculando a média móvel simples (SMA) de 50 dias e 200 dias
df_valores['SMA_50'] = df_valores['Fechamento'].rolling(window=50).mean()
df_valores['SMA_200'] = df_valores['Fechamento'].rolling(window=200).mean()

# Calculando a média móvel exponencial (EMA) de 50 dias e 200 dias
df_valores['EMA_50'] = df_valores['Fechamento'].ewm(span=50, adjust=False).mean()
df_valores['EMA_200'] = df_valores['Fechamento'].ewm(span=200, adjust=False).mean()

# Criando o gráfico de preços com as médias móveis
fig = go.Figure()

# Adicionando os preços de fechamento
fig.add_trace(go.Scatter(x=df_valores['Data'],
                         y=df_valores['Fechamento'],
                         name='Preço Fechamento',
                         line_color='blue'))

# Adicionando as médias móveis simples
fig.add_trace(go.Scatter(x=df_valores['Data'],
                         y=df_valores['SMA_50'],
                         name='SMA 50 (Tendência de curto prazo)',
                         line_color='red'))

fig.add_trace(go.Scatter(x=df_valores['Data'],
                         y=df_valores['SMA_200'],
                         name='SMA 200 (Tendência de longo prazo)',
                         line_color='green'))

# Adicionando as médias móveis exponenciais
fig.add_trace(go.Scatter(x=df_valores['Data'],
                         y=df_valores['EMA_50'],
                         name='EMA 50',
                         line_color='orange',
                         visible='legendonly'))

fig.add_trace(go.Scatter(x=df_valores['Data'],
                         y=df_valores['EMA_200'],
                         name='EMA 200',
                         line_color='purple',
                         visible='legendonly'))

# Atualizando layout do gráfico
fig.update_layout(title='Análise de Tendência de Longo Prazo',
                   xaxis_title='Data',
                   yaxis_title='Preço',
                   xaxis_rangeslider_visible=False)

fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

config = configurar_grafico(fig)
st.plotly_chart(fig, use_container_width=False, config=config)

# Determinando a tendência com base nas médias móveis
tendencia = None
if df_valores['Fechamento'].iloc[-1] > df_valores['SMA_50'].iloc[-1] and df_valores['Fechamento'].iloc[-1] > df_valores['SMA_200'].iloc[-1]:
    tendencia = 'Tendência de <span style="color:green; font-size: larger;">alta</span>'
    explicacao_tendencia = "O preço de fechamento está acima das médias móveis de curto e longo prazo, sugerindo uma tendência de alta consistente."
elif df_valores['Fechamento'].iloc[-1] < df_valores['SMA_50'].iloc[-1] and df_valores['Fechamento'].iloc[-1] < df_valores['SMA_200'].iloc[-1]:
    tendencia = 'Tendência de <span style="color:red; font-size: larger;">baixa</span>'
    explicacao_tendencia = "O preço de fechamento está abaixo das médias móveis de curto e longo prazo, indicando uma tendência de baixa persistente."
elif df_valores['Fechamento'].iloc[-1] > df_valores['SMA_50'].iloc[-1] and df_valores['Fechamento'].iloc[-1] < df_valores['SMA_200'].iloc[-1]:
    tendencia = 'Tendência de <span style="color:orange; font-size: larger;">alta</span> em formação'
    explicacao_tendencia = "O preço de fechamento está acima da média móvel de curto prazo, mas abaixo da média móvel de longo prazo, sugerindo uma possível tendência de alta em desenvolvimento."
elif df_valores['Fechamento'].iloc[-1] < df_valores['SMA_50'].iloc[-1] and df_valores['Fechamento'].iloc[-1] > df_valores['SMA_200'].iloc[-1]:
    tendencia = 'Tendência de <span style="color:blue; font-size: larger;">baixa</span> em formação'
    explicacao_tendencia = "O preço de fechamento está abaixo da média móvel de curto prazo, mas acima da média móvel de longo prazo, indicando uma possível tendência de baixa em desenvolvimento."
else:
    tendencia = '<span style="color:gray; font-size: larger;">Estabilização ou acumulação</span>'
    explicacao_tendencia = "O preço de fechamento está entre as médias móveis de curto e longo prazo, sugerindo um período de estabilização ou acumulação no mercado."

# Mensagem com a tendência e explicação
mensagem_tendencia = f"A ação está atualmente em {tendencia}. {explicacao_tendencia}"

# Exibindo mensagem com a tendência e explicação
st.markdown(mensagem_tendencia, unsafe_allow_html=True)

# Criando o objeto Ticker
try:
    acao_escolhida = yf.Ticker(sigla_acao_escolhida)
except Exception as e:
    st.error(f"Erro ao criar o objeto Ticker para {sigla_acao_escolhida}: {e}")

# Função para exibir dados com tratamento de exceção
def exibir_dados(label, func):
    try:
        dados = func()
        if dados is not None and not dados.empty:
            st.write(f"**{label}:**")
            st.write(dados)
    except Exception as e:
        st.warning(f"{label} não disponível: {e}")

# Coletando e exibindo dados fundamentalistas
exibir_dados("Histórico de preços", lambda: acao_escolhida.history(period="max"))
exibir_dados("Dividendos", lambda: acao_escolhida.dividends)
exibir_dados("Splits de ações", lambda: acao_escolhida.splits)
exibir_dados("Balanço patrimonial", lambda: acao_escolhida.balance_sheet)
exibir_dados("Demonstração de resultados", lambda: acao_escolhida.financials)
exibir_dados("Fluxo de caixa", lambda: acao_escolhida.cashflow)
exibir_dados("Recomendações de analistas", lambda: acao_escolhida.recommendations)
exibir_dados("Infromações Basicas", lambda: acao_escolhida.news)

# Exibindo opções de ações
try:
    options = acao_escolhida.options
    if options:
        option_date = options[0]
        calls = acao_escolhida.option_chain(option_date).calls
        puts = acao_escolhida.option_chain(option_date).puts
        st.write(f"**Calls para {option_date}:**")
        st.write(calls)
        st.write(f"**Puts para {option_date}:**")
        st.write(puts)
except Exception as e:
    st.warning(f"Opções de ações não disponíveis: {e}")

# Adicionando a seção de Chatbot
st.sidebar.title("Chatbot")
chat_input = st.sidebar.text_input("Faça uma pergunta ao Chatbot:")
if st.sidebar.button("Enviar"):
    if chat_input:
        response = get_chatbot_response(chat_input)
        st.sidebar.write("Resposta do Chatbot:")
        st.sidebar.write(response)

# Exibindo dados financeiros e gráficos técnicos adicionais
if sigla_acao_escolhida:
    df_financial = get_data(sigla_acao_escolhida)
    plot_technical_indicators(df_financial, sigla_acao_escolhida)
    display_fundamentals(sigla_acao_escolhida)

