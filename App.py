import streamlit as st
import pandas as pd
import yfinance as yf
from PIL import Image
from datetime import date
import plotly.express as px
import plotly.graph_objects as go

# Configurando a largura da página
st.set_page_config(
    page_title="Plotos.com.br",
    page_icon="FAV.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Função para formatar a data
def formatar_data(data):
    if data is not None:
        return pd.to_datetime(data).strftime('%d-%m-%Y')
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
    dividendos = ticker.dividends.reset_index()
    dividendos['Date'] = dividendos['Date'].apply(formatar_data)
    return info, dividendos

# Função para exibir informações da empresa
def exibir_info_empresa(info, dividendos):
    st.write(f"{info.get('shortName', 'N/A')}")
    st.write(f"**Nome completo:** {info.get('longName', 'N/A')}")
    st.write(f"**Endereço:** {info.get('address1', 'N/A')}")
    st.write(f"**Cidade:** {info.get('city', 'N/A')}")
    st.write(f"**Estado:** {info.get('state', 'N/A')}")
    st.write(f"**País:** {info.get('country', 'N/A')}")
    st.write(f"**CEP:** {info.get('zip', 'N/A')}")
    st.write(f"**Telefone:** {info.get('phone', 'N/A')}")
    st.write(f"**Site:** {info.get('website', 'N/A')}")
    st.write(f"**Setor:** {info.get('sector', 'N/A')}")
    st.write(f"**Indústria:** {info.get('industry', 'N/A')}")
    st.write(f"Moeda financeira: {info.get('financialCurrency', 'N/A')}")
    st.write(f"**Descrição:** {info.get('longBusinessSummary', 'N/A')}")
    
    with st.expander("Diretores da Empresa", expanded=False):
        directors = info.get('companyOfficers', [])
        if directors:
            for director in directors:
                st.write(f"- **Nome:** {director.get('name', 'N/A')}")
                st.write(f"  **Cargo:** {director.get('title', 'N/A')}")
                st.write(f"  **Idade:** {director.get('age', 'N/A')}")
                st.write(f"  **Ano de Nascimento:** {director.get('yearBorn', 'N/A')}")
        else:
            st.write("Nenhum diretor encontrado.")

    st.markdown("#### Preço")
    st.write(f"**Preço Fechamento Anterior:** {info.get('previousClose', 'N/A')}")
    st.write(f"**Preço Fechamento Anterior Mercado Regular:** {info.get('regularMarketPreviousClose', 'N/A')}")
    st.write(f"**Preço de Compra Atual(Bid):** {info.get('bid', 'N/A')}")
    st.write(f"**Preço de Venda Atual (Ask):** {info.get('ask', 'N/A')}")
    st.write(f"**Preço Médio dos últimos 50 dias:** {info.get('fiftyDayAverage', 'N/A')}")
    st.write(f"**Preço Médio dos últimos 200 dias:** {info.get('twoHundredDayAverage', 'N/A')}")
    st.write(f"**Máxima das últimas 52 semanas:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
    st.write(f"**Preço atual:** {info.get('currentPrice', 'N/A')}")
    st.write(f"**Preço/Vendas nos últimos 12 meses:** {info.get('priceToSalesTrailing12Months', 'N/A')}")

    st.markdown("#### Recomendações Analistas")
    st.write(f"**Média das recomendações:** {info.get('recommendationMean', 'N/A')}")
    st.write(f"**Preço alvo máximo:** {info.get('targetHighPrice', 'N/A')}")
    st.write(f"**Preço alvo mínimo:** {info.get('targetLowPrice', 'N/A')}")
    st.write(f"**Preço médio alvo:** {info.get('targetMeanPrice', 'N/A')}")
    st.write(f"**Preço mediano alvo:** {info.get('targetMedianPrice', 'N/A')}")
    st.write(f"Número de opiniões de analistas: {info.get('numberOfAnalystOpinions', 'N/A')}")
    st.write(f"Recomendação: {info.get('recommendationKey', 'N/A')}")

    st.markdown("#### Volume")
    st.write(f"**Volume médio:** {info.get('averageVolume', 'N/A')}")
    st.write(f"**Volume médio últimos 10 dias:** {info.get('averageVolume10days', 'N/A')}")

    st.markdown("#### Float")
    st.write(f"**Ações em circulação:** {info.get('sharesOutstanding', 'N/A')}")
    st.write(f"**Free Float:** {info.get('floatShares', 'N/A')}")
    st.write(f"**Percentual mantido por insiders:** {info.get('heldPercentInsiders', 'N/A')}")
    st.write(f"**Percentual mantido por instituições:** {info.get('heldPercentInstitutions', 'N/A')}")
    st.write(f"**Número de Ações mantidas por insiders:** {info.get('impliedSharesOutstanding', 'N/A')}")

    st.markdown("#### Dividendos")
    st.write(f"**Taxa de dividendos:** {info.get('dividendRate', 'N/A')}")
    st.write(f"**Dividend Yield:** {info.get('dividendYield', 'N/A')}")
    st.write(f"**Data do ex dividendos:** {info.get('exDividendDate', 'N/A')}")
    st.write(f"**Índice de pagamento:** {info.get('payoutRatio', 'N/A')}")
    st.write(f"**Rendimento médio de dividendos últimos cinco anos:** {info.get('fiveYearAvgDividendYield', 'N/A')}")
    st.write(f"**Histórico de dividendos:**")
    st.dataframe(dividendos)

    # Gráfico de barras
    st.markdown("#### Gráfico de Barras - Histórico de Dividendos")
    fig_bar = px.bar(dividendos, x='Date', y='Dividends', labels={'Date': 'Data', 'Dividends': 'Dividendos'},
                     title='Histórico de Dividendos', color_discrete_sequence=['blue'], template='plotly_dark')
    fig_bar.update_xaxes(type='category')
    st.plotly_chart(fig_bar)

    # Gráfico de linha
    st.markdown("#### Gráfico de Linha - Histórico de Dividendos")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=dividendos['Date'], y=dividendos['Dividends'],
                                  mode='lines+markers', name='Dividendos', line=dict(color='blue')))
    fig_line.update_layout(title='Histórico de Dividendos',
                           xaxis_title='Data', yaxis_title='Dividendos',
                           template='plotly_dark')
    st.plotly_chart(fig_line)

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
info_acao, dividendos_acao = pegar_info_empresa(sigla_acao_escolhida)
st.header(f"Informações da ação: {nome_acao_escolhida}")
exibir_info_empresa(info_acao, dividendos_acao)

