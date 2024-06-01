import streamlit as st
import pandas as pd
import yfinance as yf
from PIL import Image
from datetime import date

# Configurando a largura da página
st.set_page_config(layout="wide")

# Função para formatar a data
def formatar_data(data):
    if data is not None:
        return pd.to_datetime(data, unit='s').strftime('%d-%m-%Y')
    return 'N/A'

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
        indicadores['P/L'] = ticker_data.info.get('forwardPE', 'N/A')
        indicadores['LPA'] = ticker_data.info.get('trailingEps', 'N/A')
        indicadores['P/VP'] = ticker_data.info.get('priceToBook', 'N/A')
        indicadores['VPA'] = ticker_data.info.get('bookValue', 'N/A')
        indicadores['P/EBIT'] = ticker_data.info.get('enterpriseToEbitda', 'N/A')
        indicadores['Margem Bruta'] = ticker_data.info.get('grossMargins', 'N/A')
        indicadores['Margem EBIT'] = ticker_data.info.get('ebitdaMargins', 'N/A')
        indicadores['Margem Líquida'] = ticker_data.info.get('profitMargins', 'N/A')
        indicadores['ROIC'] = ticker_data.info.get('returnOnAssets', 'N/A')
        indicadores['ROE'] = ticker_data.info.get('returnOnEquity', 'N/A')
    except Exception as e:
        st.error(f"Erro ao calcular os indicadores fundamentalistas: {e}")
    return indicadores

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

# Pegando os dados das ações
df = pegar_dados_acoes()
acao = df['snome']

nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:', acao)
df_acao = df[df['snome'] == nome_acao_escolhida]
sigla_acao_escolhida = df_acao.iloc[0]['sigla_acao']
sigla_acao_escolhida += '.SA'

# Coletando os dados fundamentais
ticker_data = yf.Ticker(sigla_acao_escolhida)

# Exibindo informações gerais sobre a empresa
st.subheader('Informações Gerais')
st.write(f"**Papel:** {sigla_acao_escolhida}")
st.write(f"**Cotação:** {ticker_data.info.get('currentPrice', 'N/A')}")
st.write(f"**Tipo:** {ticker_data.info.get('quoteType', 'N/A')}")
st.write(f"**Data da última cotação:** {formatar_data(ticker_data.info.get('regularMarketTime', None))}")
st.write(f"**Empresa:** {ticker_data.info.get('longName', 'N/A')}")
st.write(f"**Setor:** {ticker_data.info.get('sector', 'N/A')}")
st.write(f"**Subsetor:** {ticker_data.info.get('industry', 'N/A')}")
st.write(f"**Valor de mercado:** {ticker_data.info.get('marketCap', 'N/A')}")
st.write(f"**Valor da firma:** {ticker_data.info.get('enterpriseValue', 'N/A')}")
st.write(f"**Número de Ações:** {ticker_data.info.get('sharesOutstanding', 'N/A')}")

# Exibindo as oscilações
st.subheader('Oscilações')
st.write(f"**Oscilação 1 mês:** {ticker_data.info.get('52WeekChange', 'N/A')}")
st.write(f"**Oscilação 6 meses:** {ticker_data.info.get('beta', 'N/A')}")
st.write(f"**Oscilação 1 ano:** {ticker_data.info.get('52WeekHigh', 'N/A')}")

# Calculando e exibindo os indicadores fundamentalistas
st.subheader('Indicadores Fundamentalistas')
indicadores = calcular_indicadores(ticker_data)
for indicador, valor in indicadores.items():
    st.write(f"**{indicador}:** {valor}")

# Exibindo dados do Balanço Patrimonial
st.subheader('Dados do Balanço Patrimonial')
balance_sheet = ticker_data.balance_sheet
if not balance_sheet.empty:
    st.write(f"**Ativo:** {balance_sheet.iloc[0].sum()}")
    st.write(f"**Disponibilidades:** {balance_sheet.get('Cash And Cash Equivalents', 'N/A')}")
    st.write(f"**Ativo Circulante:** {balance_sheet.get('Total Current Assets', 'N/A')}")
    st.write(f"**Dívida Bruta:** {balance_sheet.get('Total Debt', 'N/A')}")
    st.write(f"**Dívida Líquida:** {balance_sheet.get('Net Debt', 'N/A')}")
    st.write(f"**Patrimônio Líquido:** {balance_sheet.get('Total Equity', 'N/A')}")
else:
    st.write('Dados do balanço patrimonial não disponíveis.')

# Exibindo dados dos Demonstrativos de Resultados
st.subheader('Dados dos Demonstrativos de Resultados')
financials = ticker_data.financials
if not financials.empty:
    st.write(f"**Receita Líquida:** {financials.get('Total Revenue', 'N/A')}")
    st.write(f"**EBIT:** {financials.get('Ebit', 'N/A')}")
    st.write(f"**Lucro Líquido:** {financials.get('Net Income', 'N/A')}")
else:
    st.write('Dados dos demonstrativos de resultados não disponíveis.')





