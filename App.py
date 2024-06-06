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
    
    st.write(f"**Nome:** {info.get('longName', 'N/A')}")
    st.write(f"**Endereço:** {info.get('address1', 'N/A')}")
    st.write(f"**Cidade:** {info.get('city', 'N/A')}")
    st.write(f"**Estado:** {info.get('state', 'N/A')}")
    st.write(f"**País:** {info.get('country', 'N/A')}")
    st.write(f"**CEP:** {info.get('zip', 'N/A')}")
    st.write(f"**Telefone:** {info.get('phone', 'N/A')}")
    st.write(f"**Site:** {info.get('website', 'N/A')}")      
    st.write(f"**Setor:** {info.get('sector', 'N/A')}")
    st.write(f"**Indústria:** {info.get('industry', 'N/A')}")
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

"exDividendDate":1714608000, "dataExDividendos":1714608000,
"payoutRatio":0.2365, "índiceDistribuição":0.2365,
"fiveYearAvgDividendYield":9.02, "rendimentoMédioDividendosCincoAnos":9.02,
"beta":1.408, "beta":1.408,
"trailingPE":5.769231, "P/LProjetado":5.769231,
"forwardPE":3.4615386, "P/LPotencial":3.4615386,
"averageVolume":522604, "volumeMédio":522604,
"averageVolume10days":564944, "volumeMédio10dias":564944,
"averageDailyVolume10Day":564944, "volumeMédioDiário10dias":564944,
"bid":2.25, "oferta":2.25,
"ask":2.25, "pedido":2.25,
"marketCap":298561504, "capitalizaçãoMercado":298561504,
"fiftyTwoWeekHigh":4.45, "máxima52semanas":4.45,
"priceToSalesTrailing12Months":0.22934654, "preço/vendasÚltimos12Meses":0.22934654,
"fiftyDayAverage":2.6942, "média50dias":2.6942,
"twoHundredDayAverage":2.78175, "média200dias":2.78175,
"currency":"BRL", "moeda":"BRL",
"enterpriseValue":2951044352, "valorEmpresa":2951044352,
"profitMargins":0.03938, "margensLucro":0.03938,
"floatShares":71183488, "açõesFlutuantes":71183488,
"sharesOutstanding":132694000, "açõesEmitidas":132694000,
"heldPercentInsiders":0.50129, "percentualMantidoInsiders":0.50129,
"heldPercentInstitutions":0.12604, "percentualMantidoInstituições":0.12604,
"impliedSharesOutstanding":132694000, "açõesEmitidasImplícitas":132694000,
"bookValue":10.655, "valorContábil":10.655,
"priceToBook":0.21116847, "preço/valorContábil":0.21116847,
"lastFiscalYearEnd":1703980800, "fimÚltimoAnoFiscal":1703980800,
"nextFiscalYearEnd":1735603200, "fimPróximoAnoFiscal":1735603200,
"mostRecentQuarter":1711843200, "trimestreMaisRecente":1711843200,
"earningsQuarterlyGrowth":0.063, "crescimentoTrimestralLucros":0.063,
"netIncomeToCommon":51262000, "lucroLíquidoComum":51262000,
"trailingEps":0.39, "EPSProjetado":0.39,
"forwardEps":0.65, "EPSPotencial":0.65,
"lastSplitFactor":"1:5", "últimoFatorDivisão":"1:5",
"lastSplitDate":1597276800, "dataÚltimaDivisão":1597276800,
"enterpriseToRevenue":2.267, "empresa/receita":2.267,
"enterpriseToEbitda":16.379, "empresa/ebitda":16.379,
"52WeekChange":-0.35833335, "mudança52semanas":-0.35833335,
"SandP52WeekChange":0.24688339, "mudançaSandP52semanas":0.24688339,
"lastDividendValue":0.091013, "valorÚltimoDividendo":0.091013,
"lastDividendDate":1714608000, "dataÚltimoDividendo":1714608000,
"exchange":"SAO", "bolsa":"SAO",
"quoteType":"EQUITY", "tipoCotação":"AÇÕES",
"symbol":"HBOR3.SA", "símbolo":"HBOR3.SA",
"underlyingSymbol":"HBOR3.SA", "símboloSubjacente":"HBOR3.SA",
"shortName":"HELBORONNM", "nomeCurto":"HELBORONNM",
"longName":"Helbor Empreendimentos S.A.", "nomeCompleto":"Helbor Empreendimentos S.A.",
"firstTradeDateEpochUtc":1193659200, "dataPrimeiraNegociaçãoEpochUtc":1193659200,
"timeZoneFullName":"America/Sao_Paulo", "nomeCompletoFusoHorário":"America/Sao_Paulo",
"timeZoneShortName":"BRT", "nomeCurtoFusoHorário":"BRT",
"uuid":"a57656f4-6084-3c66-b33f-ca8fd9d37c05", "uuid":"a57656f4-6084-3c66-b33f-ca8fd9d37c05",
"messageBoardId":"finmb_38648356", "idQuadroMensagens":"finmb_38648356",
"gmtOffSetMilliseconds":-10800000, "gmtDesvioMilissegundos":-10800000,
"currentPrice":2.25, "preçoAtual":2.25,
"targetHighPrice":4.7, "preçoAlvoMáximo":4.7,
"targetLowPrice":3.4, "preçoAlvoMínimo":3.4,
"targetMeanPrice":4.05, "preçoMédioAlvo":4.05,
"targetMedianPrice":4.05, "preçoMedianoAlvo":4.05,
"recommendationMean":3.0, "médiaRecomendações":3.0,
"recommendationKey":"hold", "chaveRecomendação":"manter",
"numberOfAnalystOpinions":2, "númeroOpiniõesAnalistas":2,
"totalCash":443475008, "totalDinheiro":443475008,
"totalCashPerShare":3.342, "totalDinheiroPorAção":3.342,
"ebitda":180172992, "ebitda":180172992,
"totalDebt":2102781056, "dívidaTotal":2102781056,
"quickRatio":0.771, "índiceRápido":0.771,
"currentRatio":2.353, "índiceLiquidezCorrente":2.353,
"totalRevenue":1301792000, "receitaTotal":1301792000,
"debtToEquity":87.652, "dívida/PatrimônioLíquido":87.652,
"revenuePerShare":9.81, "receitaPorAção":9.81,
"returnOnAssets":0.01698, "retornoSobreAtivos":0.01698,
"returnOnEquity":0.07789, "retornoSobrePatrimônioLíquido":0.07789,
"freeCashflow":32589376, "fluxoCaixaLivre":32589376,
"operatingCashflow":129286000, "fluxoCaixaOperacional":129286000,
"earningsGrowth":0.063, "crescimentoLucros":0.063,
"revenueGrowth":0.095, "crescimentoReceita":0.095,
"grossMargins":0.29997, "margensBrutas":0.29997,
"ebitdaMargins":0.1384, "margensEbitda":0.1384,
"operatingMargins":0.14161, "margensOperacionais":0.14161,
"financialCurrency":"BRL", "moedaFinanceira":"BRL",

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







