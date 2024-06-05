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
    indicadores = {
        'P/L': ticker_data.info.get('forwardPE', 'N/A'),
        'LPA': ticker_data.info.get('trailingEps', 'N/A'),
        'P/VP': ticker_data.info.get('priceToBook', 'N/A'),
        'VPA': ticker_data.info.get('bookValue', 'N/A'),
        'P/EBIT': ticker_data.info.get('enterpriseToEbitda', 'N/A'),
        'Margem Bruta': ticker_data.info.get('grossMargins', 'N/A'),
        'Margem EBIT': ticker_data.info.get('ebitdaMargins', 'N/A'),
        'Margem Líquida': ticker_data.info.get('profitMargins', 'N/A'),
        'ROIC': ticker_data.info.get('returnOnAssets', 'N/A'),
        'ROE': ticker_data.info.get('returnOnEquity', 'N/A')
    }
    return indicadores

# Função para classificar os indicadores
def classificar_indicador(valor, tipo):
    if valor == 'N/A':
        return 'N/A', 'gray'
    try:
        valor = float(valor)
        if tipo == 'P/L':
            if valor < 15:
                return 'bom', 'green'
            elif valor < 25:
                return 'regular', 'yellow'
            else:
                return 'ruim', 'red'
        elif tipo == 'LPA':
            if valor > 0:
                return 'bom', 'green'
            else:
                return 'ruim', 'red'
        elif tipo == 'P/VP':
            if valor < 1:
                return 'bom', 'green'
            elif valor < 2:
                return 'regular', 'yellow'
            else:
                return 'ruim', 'red'
        elif tipo == 'P/EBIT':
            if valor < 10:
                return 'bom', 'green'
            elif valor < 15:
                return 'regular', 'yellow'
            else:
                return 'ruim', 'red'
        elif tipo in ['Margem Bruta', 'Margem EBIT', 'Margem Líquida']:
            if valor > 0.2:
                return 'bom', 'green'
            elif valor > 0.1:
                return 'regular', 'yellow'
            else:
                return 'ruim', 'red'
        elif tipo == 'ROIC':
            if valor > 0.1:
                return 'bom', 'green'
            elif valor > 0.05:
                return 'regular', 'yellow'
            else:
                return 'ruim', 'red'
        elif tipo == 'ROE':
            if valor > 0.15:
                return 'bom', 'green'
            elif valor > 0.1:
                return 'regular', 'yellow'
            else:
                return 'ruim', 'red'
    except ValueError:
        return 'N/A', 'gray'
    return 'N/A', 'gray'

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
informacoes_gerais = {
    'Papel': sigla_acao_escolhida,
    'Cotação': ticker_data.info.get('currentPrice', 'N/A'),
    'Tipo': ticker_data.info.get('quoteType', 'N/A'),
    'Data da última cotação': formatar_data(ticker_data.info.get('regularMarketTime', None)),
    'Empresa': ticker_data.info.get('longName', 'N/A'),
    'Setor': ticker_data.info.get('sector', 'N/A'),
    'Subsetor': ticker_data.info.get('industry', 'N/A'),
    'Valor de mercado': ticker_data.info.get('marketCap', 'N/A'),
    'Valor da firma': ticker_data.info.get('enterpriseValue', 'N/A'),
    'Número de Ações': ticker_data.info.get('sharesOutstanding', 'N/A'),
    'Endereço': f"{ticker_data.info.get('address1', 'N/A')}, {ticker_data.info.get('address2', '')} - {ticker_data.info.get('city', 'N/A')} - {ticker_data.info.get('state', 'N/A')} - {ticker_data.info.get('country', 'N/A')}",
    'Site': ticker_data.info.get('website', 'N/A'),
    'Resumo': ticker_data.info.get('longBusinessSummary', 'N/A'),
    'Dividendo': ticker_data.info.get('dividendRate', 'N/A'),
    'Rendimento de Dividendos': ticker_data.info.get('dividendYield', 'N/A')
}

for chave, valor in informacoes_gerais.items():
    st.write(f"**{chave}:** {valor}")

# Exibindo as oscilações
st.subheader('Oscilações')
oscilações = {
    'Oscilação 1 mês': ticker_data.info.get('52WeekChange', 'N/A'),
    'Oscilação 6 meses': ticker_data.info.get('beta', 'N/A'),
    'Oscilação 1 ano': ticker_data.info.get('52WeekHigh', 'N/A')
}

for chave, valor in oscilações.items():
    st.write(f"**{chave}:** {valor}")

# Calculando e exibindo os indicadores fundamentalistas
st.subheader('Indicadores Fundamentalistas')

explicacoes = {
    'P/L': 'Preço/Lucro: Relação entre o preço da ação e o lucro por ação. Um P/L baixo pode indicar que a ação está subvalorizada.',
    'LPA': 'Lucro por Ação: Lucro líquido da empresa dividido pelo número total de ações.',
    'P/VP': 'Preço/Valor Patrimonial: Relação entre o preço da ação e o valor patrimonial por ação. Um P/VP abaixo de 1 pode indicar que a ação está subvalorizada.',
    'VPA': 'Valor Patrimonial por Ação: Patrimônio líquido da empresa dividido pelo número total de ações.',
    'P/EBIT': 'Preço/Lucro antes dos Juros e Impostos: Relação entre o preço da ação e o lucro antes dos juros e impostos.',
    'Margem Bruta': 'Margem Bruta: Percentual do lucro bruto em relação à receita total. Margens mais altas indicam maior eficiência.',
    'Margem EBIT': 'Margem EBIT: Percentual do lucro antes dos juros e impostos em relação à receita total.',
    'Margem Líquida': 'Margem Líquida: Percentual do lucro líquido em relação à receita total.',
    'ROIC': 'Retorno sobre o Capital Investido: Eficiência da empresa em gerar retorno sobre o capital investido.',
    'ROE': 'Retorno sobre o Patrimônio Líquido: Eficiência da empresa em gerar retorno sobre o patrimônio líquido.'
}

indicadores = calcular_indicadores(ticker_data)
for indicador, valor in indicadores.items():
    classificacao, cor = classificar_indicador(valor, indicador)
    st.write(f"**{indicador}:** {valor} ({classificacao})", unsafe_allow_html=True)
    st.markdown(f"<span style='color:{cor}'>{explicacoes[indicador]}</span>", unsafe_allow_html=True)

# Exibindo dados do Balanço Patrimonial
st.subheader('Dados do Balanço Patrimonial')
balanco = {
    'Ativo Total': ticker_data.balance_sheet.get('Total Assets', 'N/A'),
    'Passivo Total': ticker_data.balance_sheet.get('Total Liabilities Net Minority Interest', 'N/A'),
    'Patrimônio Líquido': ticker_data.balance_sheet.get('Stockholders Equity', 'N/A')
}

for chave, valor in balanco.items():
    st.write(f"**{chave}:** {valor}")





