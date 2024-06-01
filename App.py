import streamlit as st
import pandas as pd
import yfinance as yf
from PIL import Image
from datetime import date

# Configurando a largura da página
st.set_page_config(layout="wide")

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
def pegar_dados_acoes():
    path = 'https://raw.githubusercontent.com/splocs/meu-repositorio/main/acoes.csv'
    return pd.read_csv(path, delimiter=';')

# Função para pegar os valores online
def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, DATA_INICIO, DATA_FIM, progress=False)
    df.reset_index(inplace=True)
    return df

# Função para calcular os indicadores fundamentalistas
def calcular_indicadores(ticker_data):
    indicadores = {}
    try:
        indicadores['P/L'] = ticker_data.info['forwardPE']
        indicadores['LPA'] = ticker_data.info['trailingEps']
        indicadores['P/VP'] = ticker_data.info['priceToBook']
        indicadores['VPA'] = ticker_data.info['bookValue']
        indicadores['P/EBIT'] = ticker_data.info['enterpriseToEbitda']
        indicadores['Margem Bruta'] = ticker_data.info['grossMargins']
        indicadores['Margem EBIT'] = ticker_data.info['ebitdaMargins']
        indicadores['Margem Líquida'] = ticker_data.info['profitMargins']
        indicadores['ROIC'] = ticker_data.info['returnOnAssets']
        indicadores['ROE'] = ticker_data.info['returnOnEquity']
    except Exception as e:
        st.error(f"Erro ao calcular os indicadores fundamentalistas: {e}")
    return indicadores

# Função para exibir dados com tratamento de exceção
def exibir_dados(label, func):
    try:
        dados = func()
        if dados is not None and not dados.empty:
            st.write(f"**{label}:**")
            st.write(dados)
    except Exception as e:
        st.warning(f"{label} não disponível: {e}")

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

st.title('Análise de ações')

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

# Coletando os dados fundamentais
ticker_data = yf.Ticker(sigla_acao_escolhida)

# Exibindo informações gerais sobre a empresa
st.subheader('Informações Gerais')
st.write(f"**Papel:** {sigla_acao_escolhida}")
st.write(f"**Cotação:** {ticker_data.info['currentPrice']}")
st.write(f"**Tipo:** {ticker_data.info['quoteType']}")
st.write(f"**Data da última cotação:** {formatar_data(ticker_data.info['regularMarketTime'])}")
st.write(f"**Empresa:** {ticker_data.info['longName']}")
st.write(f"**Setor:** {ticker_data.info['sector']}")
st.write(f"**Subsetor:** {ticker_data.info['industry']}")
st.write(f"**Valor de mercado:** {ticker_data.info['marketCap']}")
st.write(f"**Valor da firma:** {ticker_data.info['enterpriseValue']}")
st.write(f"**Número de Ações:** {ticker_data.info['sharesOutstanding']}")

# Exibindo as oscilações
st.subheader('Oscilações')
st.write(f"**Oscilação 1 mês:** {ticker_data.info['52WeekChange']}")
st.write(f"**Oscilação 6 meses:** {ticker_data.info['beta']}")
st.write(f"**Oscilação 1 ano:** {ticker_data.info['52WeekHigh']}")

# Calculando e exibindo os indicadores fundamentalistas
st.subheader('Indicadores Fundamentalistas')
indicadores = calcular_indicadores(ticker_data)
for indicador, valor in indicadores.items():
    st.write(f"**{indicador}:** {valor}")

# Exibindo dados do Balanço Patrimonial
st.subheader('Dados do Balanço Patrimonial')
st.write(f"**Ativo:** {ticker_data.balance_sheet.iloc[0].sum()}")
st.write(f"**Disponibilidades:** {ticker_data.balance_sheet.iloc[0]['Cash And Cash Equivalents']}")
st.write(f"**Ativo Circulante:** {ticker_data.balance_sheet.iloc[0]['Total Current Assets']}")
st.write(f"**Dívida Bruta:** {ticker_data.balance_sheet.iloc[0]['Total Debt']}")
st.write(f"**Dívida Líquida:** {ticker_data.balance_sheet.iloc[0]['Net Debt']}")
st.write(f"**Patrimônio Líquido:** {ticker_data.balance_sheet.iloc[0]['Total Equity']}")

# Exibindo dados dos Demonstrativos de Resultados
st.subheader('Dados dos Demonstrativos de Resultados')
st.write(f"**Receita Líquida:** {ticker_data.financials.iloc[0]['Total Revenue']}")
st.write(f"**EBIT:** {ticker_data.financials.iloc[0]['Ebit']}")
st.write(f"**Lucro Líquido:** {ticker_data.financials.iloc[0]['Net Income']}")



