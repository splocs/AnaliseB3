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

# Função para pegar as informações da empresa
def pegar_info_empresa(sigla_acao):
    ticker = yf.Ticker(sigla_acao)
    info = ticker.info
    return info

# Função para exibir informações da empresa
def exibir_info_empresa(info):
    st.markdown("## Informações da Companhia")
    st.write(f"**Nome:** {info.get('longName', 'N/A')}")
    st.write(f"**Endereço:** {info.get('address1', 'N/A')}")
    st.write(f"**Cidade:** {info.get('city', 'N/A')}")
    st.write(f"**Estado:** {info.get('state', 'N/A')}")
    st.write(f"**País:** {info.get('country', 'N/A')}")
    st.write(f"**CEP:** {info.get('zip', 'N/A')}")
    st.write(f"**Telefone:** {info.get('phone', 'N/A')}")
    st.write(f"**Website:** {info.get('website', 'N/A')}")
    
    st.write(f"**Setor:** {info.get('sector', 'N/A')}")
    st.write(f"**Indústria:** {info.get('industry', 'N/A')}")
    st.write(f"**Descrição:** {info.get('longBusinessSummary', 'N/A')}")
    
    st.write(f"**Número de funcionários:** {info.get('fullTimeEmployees', 'N/A')}")
    st.write(f"**Capitalização de mercado:** {info.get('marketCap', 'N/A')}")
    st.write(f"**Preço atual:** {info.get('currentPrice', 'N/A')}")
    st.write(f"**Alta/baixa de 52 semanas:** {info.get('fiftyTwoWeekHigh', 'N/A')} / {info.get('fiftyTwoWeekLow', 'N/A')}")
    st.write(f"**Volume médio:** {info.get('averageVolume', 'N/A')}")
    st.write(f"**P/L (trailing):** {info.get('trailingPE', 'N/A')}")
    st.write(f"**P/L (forward):** {info.get('forwardPE', 'N/A')}")
    st.write(f"**Peg Ratio:** {info.get('pegRatio', 'N/A')}")
    st.write(f"**Beta:** {info.get('beta', 'N/A')}")
    st.write(f"**Margem Bruta:** {info.get('grossMargins', 'N/A')}")
    st.write(f"**Margem Operacional:** {info.get('operatingMargins', 'N/A')}")
    st.write(f"**Margem EBITDA:** {info.get('ebitdaMargins', 'N/A')}")
    st.write(f"**Retorno sobre Ativos:** {info.get('returnOnAssets', 'N/A')}")
    st.write(f"**Retorno sobre Patrimônio:** {info.get('returnOnEquity', 'N/A')}")
    st.write(f"**Dívida Total:** {info.get('totalDebt', 'N/A')}")
    st.write(f"**Receita Total:** {info.get('totalRevenue', 'N/A')}")
    st.write(f"**Lucro Líquido:** {info.get('netIncomeToCommon', 'N/A')}")
    st.write(f"**Fluxo de Caixa Livre:** {info.get('freeCashflow', 'N/A')}")
    st.write(f"**Data do último balanço:** {formatar_data(info.get('mostRecentQuarter', None))}")
    st.write(f"**Moeda:** {info.get('financialCurrency', 'N/A')}")

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

# Criando a sidebar
st.sidebar.markdown('Escolha a ação')

# Pegando os dados das ações
df = pegar_dados_acoes()
acao = df['snome']

nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:', acao)
df_acao = df[df['snome'] == nome_acao_escolhida]
sigla_acao_escolhida = df_acao.iloc[0]['sigla_acao']
sigla_acao_escolhida += '.SA'

# Pegar e exibir as informações da empresa
info_acao = pegar_info_empresa(sigla_acao_escolhida)
st.header(f"Informações da ação: {nome_acao_escolhida}")
exibir_info_empresa(info_acao)







