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

    # Função para traduzir texto
def traduzir_texto(texto, destino='pt'):
    translator = Translator()
    traducao = translator.translate(texto, dest=destino)
    return traducao.text

   

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
    
    st.write(f"**Nome:** {info.get('longName', 'N/A')}")
    st.write(f"**Nome curto:** {info.get('shortName', 'N/A')}")
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
    
  # Exibição dos diretores dentro de um expander sem borda
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

    st.markdown("## Analise de Risco")  
    st.write(f"**Numedo de casas do preço da ação:** {info.get('priceHint', 'N/A')}")
    st.write(f"**Preço Fechamento Anterior:** {info.get('previousClose', 'N/A')}")
    st.write(f"**Preço Fechamento Anterior Mercado Regular:** {info.get('regularMarketPreviousClose', 'N/A')}")
    st.write(f"**Taxa de dividendos:** {info.get('dividendRate', 'N/A')}")
    st.write(f"**Dividend Yield:** {info.get('dividendYield', 'N/A')}")
    st.write(f"**Data do ex dividendos:** {info.get('exDividendDate', 'N/A')}")
    st.write(f"**Índice de pagamento:** {info.get('payoutRatio', 'N/A')}")
    st.write(f"**Rendimento médio de dividendos nos últimos cinco anos:** {info.get('fiveYearAvgDividendYield', 'N/A')}")
    st.write(f"**Beta:** {info.get('beta', 'N/A')}")
    st.write(f"**P/L (Preço/Lucro) em retrospecto:** {info.get('trailingPE', 'N/A')}")
    st.write(f"**P/L (Preço/Lucro) projetado:** {info.get('forwardPE', 'N/A')}")
    st.write(f"**Volume médio:** {info.get('averageVolume', 'N/A')}")
    st.write(f"**Volume médio nos últimos 10 dias:** {info.get('averageVolume10days', 'N/A')}")
    st.write(f"**Volume médio diário nos últimos 10 dias:** {info.get('averageDailyVolume10Day', 'N/A')}")
    st.write(f"**Oferta:** {info.get('bid', 'N/A')}")
    st.write(f"**Pedido:** {info.get('ask', 'N/A')}")
    st.write(f"**Capitalização de mercado:** {info.get('marketCap', 'N/A')}")
    st.write(f"**Máxima das últimas 52 semanas:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
    st.write(f"**Preço/Vendas nos últimos 12 meses:** {info.get('priceToSalesTrailing12Months', 'N/A')}")
    st.write(f"**Média dos últimos 50 dias:** {info.get('fiftyDayAverage', 'N/A')}")
    st.write(f"**Média dos últimos 200 dias:** {info.get('twoHundredDayAverage', 'N/A')}")
    st.write(f"**Moeda:** {info.get('currency', 'N/A')}")
    st.write(f"**Valor da empresa:** {info.get('enterpriseValue', 'N/A')}")
    st.write(f"**Margens de lucro:** {info.get('profitMargins', 'N/A')}")
    st.write(f"**Ações flutuantes:** {info.get('floatShares', 'N/A')}")
    st.write(f"**Ações emitidas:** {info.get('sharesOutstanding', 'N/A')}")
    st.write(f"**Percentual mantido por insiders:** {info.get('heldPercentInsiders', 'N/A')}")
    st.write(f"**Percentual mantido por instituições:** {info.get('heldPercentInstitutions', 'N/A')}")
    st.write(f"**Ações emitidas implícitas:** {info.get('impliedSharesOutstanding', 'N/A')}")
    st.write(f"**Valor contábil:** {info.get('bookValue', 'N/A')}")
    st.write(f"**Preço/Valor contábil:** {info.get('priceToBook', 'N/A')}")
    st.write(f"**Fim do último ano fiscal:** {info.get('lastFiscalYearEnd', 'N/A')}")
    st.write(f"**Fim do próximo ano fiscal:** {info.get('nextFiscalYearEnd', 'N/A')}")
    st.write(f"**Trimestre mais recente:** {info.get('mostRecentQuarter', 'N/A')}")
    st.write(f"**Crescimento trimestral dos lucros:** {info.get('earningsQuarterlyGrowth', 'N/A')}")
    st.write(f"**Lucro líquido comum:** {info.get('netIncomeToCommon', 'N/A')}")
    st.write(f"**EPS (Lucro por ação) em retrospecto:** {info.get('trailingEps', 'N/A')}")
    st.write(f"**EPS (Lucro por ação) projetado:** {info.get('forwardEps', 'N/A')}")
    st.write(f"**Último fator de divisão:** {info.get('lastSplitFactor', 'N/A')}")
    st.write(f"**Data da última divisão:** {info.get('lastSplitDate', 'N/A')}")
    st.write(f"**Empresa/Receita:** {info.get('enterpriseToRevenue', 'N/A')}")
    st.write(f"**Empresa/EBITDA:** {info.get('enterpriseToEbitda', 'N/A')}")
    st.write(f"**Mudança em 52 semanas:** {info.get('52WeekChange', 'N/A')}")
    st.write(f"**Mudança em 52 semanas (S&P):** {info.get('SandP52WeekChange', 'N/A')}")
    st.write(f"**Valor do último dividendo:** {info.get('lastDividendValue', 'N/A')}")
    st.write(f"**Data do último dividendo:** {info.get('lastDividendDate', 'N/A')}")
    st.write(f"**Bolsa:** {info.get('exchange', 'N/A')}")
    st.write(f"**Tipo de cotação:** {info.get('quoteType', 'N/A')}")
    st.write(f"**Data da primeira negociação (UTC):** {info.get('firstTradeDateEpochUtc', 'N/A')}")
    st.write(f"**Nome completo do fuso horário:** {info.get('timeZoneFullName', 'N/A')}")
    st.write(f"**Nome curto do fuso horário:** {info.get('timeZoneShortName', 'N/A')}")
    st.write(f"**UUID:** {info.get('uuid', 'N/A')}")
    st.write(f"**ID do quadro de mensagens:** {info.get('messageBoardId', 'N/A')}")
    st.write(f"**Desvio de GMT em milissegundos:** {info.get('gmtOffSetMilliseconds', 'N/A')}")
    st.write(f"**Preço atual:** {info.get('currentPrice', 'N/A')}")
    st.write(f"**Preço alvo máximo:** {info.get('targetHighPrice', 'N/A')}")
    st.write(f"**Preço alvo mínimo:** {info.get('targetLowPrice', 'N/A')}")
    st.write(f"**Preço médio alvo:** {info.get('targetMeanPrice', 'N/A')}")
    st.write(f"**Preço mediano alvo:** {info.get('targetMedianPrice', 'N/A')}")
    st.write(f"**Média das recomendações:** {info.get('recommendationMean', 'N/A')}")
    st.write(f"Número de opiniões de analistas: {info.get('numberOfAnalystOpinions', 'N/A')}")
    st.write(f"Total de dinheiro: {info.get('totalCash', 'N/A')}")
    st.write(f"Total de dinheiro por ação: {info.get('totalCashPerShare', 'N/A')}")
    st.write(f"EBITDA: {info.get('ebitda', 'N/A')}")
    st.write(f"Dívida total: {info.get('totalDebt', 'N/A')}")
    st.write(f"Índice rápido: {info.get('quickRatio', 'N/A')}")
    st.write(f"Índice de liquidez corrente: {info.get('currentRatio', 'N/A')}")
    st.write(f"Receita total: {info.get('totalRevenue', 'N/A')}")
    st.write(f"Dívida/Patrimônio líquido: {info.get('debtToEquity', 'N/A')}")
    st.write(f"Receita por ação: {info.get('revenuePerShare', 'N/A')}")
    st.write(f"Retorno sobre ativos: {info.get('returnOnAssets', 'N/A')}")
    st.write(f"Retorno sobre patrimônio líquido: {info.get('returnOnEquity', 'N/A')}")
    st.write(f"Fluxo de caixa livre: {info.get('freeCashflow', 'N/A')}")
    st.write(f"Fluxo de caixa operacional: {info.get('operatingCashflow', 'N/A')}")
    st.write(f"Crescimento dos lucros: {info.get('earningsGrowth', 'N/A')}")
    st.write(f"Crescimento da receita: {info.get('revenueGrowth', 'N/A')}")
    st.write(f"Margens brutas: {info.get('grossMargins', 'N/A')}")
    st.write(f"Margens EBITDA: {info.get('ebitdaMargins', 'N/A')}")
    st.write(f"Margens operacionais: {info.get('operatingMargins', 'N/A')}")
    
 

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
