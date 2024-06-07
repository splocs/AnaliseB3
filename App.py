import streamlit as st
import pandas as pd
import yfinance as yf
from PIL import Image
from datetime import date
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

def criar_grafico_dividendos(dividendos):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dividendos.index,
        y=dividendos.values,
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(color='blue', size=6)
    ))
    
    fig.update_layout(
        title="Evolução dos Dividendos",
        xaxis_title='',
        yaxis_title='',
        showlegend=False,
        plot_bgcolor='white'
    )
    
    fig.update_xaxes(
        rangeslider_visible=True,
        fixedrange=False,
        showgrid=True,
        zeroline=True
    )
    
    fig.update_yaxes(
        fixedrange=True,
        showgrid=True,
        zeroline=True
    )
    
    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
        dragmode='pan',
        modebar_remove=['zoom', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
    )

    return fig

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
    return info, ticker

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

    with st.expander("Histórico de Dividendos", expanded=False):
        if not dividendos.empty:
            st.dataframe(dividendos)
            grafico = criar_grafico_dividendos(dividendos)
            st.plotly_chart(grafico)
        else:
            st.write("Nenhum dividendo encontrado.")

    st.write(f"**Beta:** {info.get('beta', 'N/A')}")
    st.write(f"**P/L (Preço/Lucro) em retrospecto:** {info.get('trailingPE', 'N/A')}")
    st.write(f"**P/L (Preço/Lucro) projetado:** {info.get('forwardPE', 'N/A')}")
    st.write(f"**Capitalização de mercado:** {info.get('marketCap', 'N/A')}")
    st.write(f"**Valor da empresa:** {info.get('enterpriseValue', 'N/A')}")
    st.write(f"**Margens de lucro:** {info.get('profitMargins', 'N/A')}")
    st.write(f"**Valor contábil:** {info.get('bookValue', 'N/A')}")
    st.write(f"**Preço/Valor contábil:** {info.get('priceToBook', 'N/A')}")
    st.write(f"**Fim do último ano fiscal:** {info.get('lastFiscalYearEnd', 'N/A')}")
    st.write(f"**Data do último trimestre:** {info.get('mostRecentQuarter', 'N/A')}")
    st.write(f"**Total de empregados:** {info.get('fullTimeEmployees', 'N/A')}")
    st.write(f"**Auditoria de risco:** {info.get('auditRisk', 'N/A')}")
    st.write(f"**Trabalho no último ano:** {info.get('compensationAsOfLastFiscalYear', 'N/A')}")
    st.write(f"**Número de empregados:** {info.get('fullTimeEmployees', 'N/A')}")
    st.write(f"**Ranking no ESG:** {info.get('esgPop', 'N/A')}")

DATA_INICIO = '2010-01-01'
DATA_FIM = date.today().strftime('%Y-%m-%d')

acoes = pegar_dados_acoes()

st.title('Plotos.com.br')

st.sidebar.title('Escolha a ação:')
sigla_acao = st.sidebar.selectbox('Ticker', acoes['sigla'])

if sigla_acao:
    df = pegar_valores_online(sigla_acao)
    info, ticker = pegar_info_empresa(sigla_acao)

    st.header(f'Informações sobre a ação {sigla_acao}')
    exibir_info_empresa(info, ticker.dividends)
else:
    st.write("Selecione uma ação para ver as informações.")
