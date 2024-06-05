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

# Exemplo de dicionário estruturado para várias empresas
empresas_info = {
    'Helbor': {
        'companyInfo': {
            'address1': 'Av. Cândido de Abreu, 428',
            'city': 'Curitiba',
            'state': 'PR',
            'zip': '80530-000',
            'country': 'Brazil',
            'phone': '41 3029 8300',
            'website': 'https://www.helbor.com.br',
        },
        'industryInfo': {
            'industry': 'Real Estate',
            'industryKey': 'real-estate',
            'industryDisp': 'Real Estate',
            'sector': 'Finance',
            'sectorKey': 'finance',
            'sectorDisp': 'Finance',
        },
        'summary': {
            'longBusinessSummary': "Helbor Empreendimentos S.A. operates in the real estate sector in Brazil. The company engages in the development, construction, and sale of residential and commercial properties. It was founded in 1977 and is headquartered in Mogi das Cruzes, Brazil."
        },
        'employees': {
            'fullTimeEmployees': 1200,
            'companyOfficers': [
                {'maxAge': 1, 'name': 'Mr. Henrique Borenstein', 'age': 69, 'title': 'CEO & Chairman', 'yearBorn': 1955, 'fiscalYear': 2023, 'totalPay': 500000, 'exercisedValue': 0, 'unexercisedValue': 0},
                {'maxAge': 1, 'name': 'Ms. Maria Silva', 'age': 45, 'title': 'CFO', 'yearBorn': 1978, 'fiscalYear': 2023, 'totalPay': 250000, 'exercisedValue': 0, 'unexercisedValue': 0},
            ]
        },
        'risk': {
            'auditRisk': 4,
            'boardRisk': 7,
            'compensationRisk': 6,
            'shareHolderRightsRisk': 5,
            'overallRisk': 7,
            'governanceEpochDate': 1717200000,
            'compensationAsOfEpochDate': 1703980800
        },
        'investorRelations': {
            'irWebsite': 'https://ri.helbor.com.br',
            'maxAge': 86400
        },
        'stockInfo': {
            'priceHint': 2,
            'previousClose': 1.5,
            'open': 1.45,
            'dayLow': 1.4,
            'dayHigh': 1.6,
            'regularMarketPreviousClose': 1.5,
            'regularMarketOpen': 1.45,
            'regularMarketDayLow': 1.4,
            'regularMarketDayHigh': 1.6,
            'beta': 1.2,
            'trailingPE': 10.5,
            'forwardPE': 9.8,
            'volume': 200000,
            'regularMarketVolume': 200000,
            'averageVolume': 250000,
            'averageVolume10days': 220000,
            'averageDailyVolume10Day': 220000,
            'bid': 1.49,
            'ask': 1.51,
            'bidSize': 100,
            'askSize': 100,
            'marketCap': 500000000,
            'fiftyTwoWeekLow': 1.0,
            'fiftyTwoWeekHigh': 2.0,
            'priceToSalesTrailing12Months': 1.5,
            'fiftyDayAverage': 1.45,
            'twoHundredDayAverage': 1.35,
            'currency': 'BRL',
            'enterpriseValue': 600000000,
            'profitMargins': 0.12,
            'floatShares': 100000000,
            'sharesOutstanding': 150000000,
            'sharesShort': 1000000,
            'sharesShortPriorMonth': 900000,
            'sharesShortPreviousMonthDate': 1713139200,
            'dateShortInterest': 1715731200,
            'sharesPercentSharesOut': 0.01,
            'heldPercentInsiders': 0.3,
            'heldPercentInstitutions': 0.5,
            'shortRatio': 1.2,
            'shortPercentOfFloat': 0.01,
            'impliedSharesOutstanding': 150000000,
            'bookValue': 2.0,
            'priceToBook': 0.75,
            'lastFiscalYearEnd': 1703980800,
            'nextFiscalYearEnd': 1735603200,
            'mostRecentQuarter': 1711843200,
            'earningsQuarterlyGrowth': 0.2,
            'netIncomeToCommon': 60000000,
            'trailingEps': 0.15,
            'forwardEps': 0.16,
            'pegRatio': 1.5,
            'lastSplitFactor': '1:1',
            'lastSplitDate': 1654473600,
            'enterpriseToRevenue': 2.0,
            'enterpriseToEbitda': 8.0,
            '52WeekChange': 0.3,
            'SandP52WeekChange': 0.2,
            'exchange': 'BVMF',
            'quoteType': 'EQUITY',
            'symbol': 'HBOR3.SA',
            'underlyingSymbol': 'HBOR3.SA',
            'shortName': 'Helbor',
            'longName': 'Helbor Empreendimentos S.A.',
            'firstTradeDateEpochUtc': 863703000,
            'timeZoneFullName': 'America/Sao_Paulo',
            'timeZoneShortName': 'BRT',
            'uuid': '261fd26b-0151-3813-b0d0-97e4ed4c6505',
            'messageBoardId': 'finmb_18749',
            'gmtOffSetMilliseconds': -10800000,
            'currentPrice': 1.5,
            'targetHighPrice': 2.0,
            'targetLowPrice': 1.3,
            'targetMeanPrice': 1.6,
            'targetMedianPrice': 1.55,
            'recommendationMean': 2.5,
            'recommendationKey': 'hold',
            'numberOfAnalystOpinions': 5,
        },
        'financials': {
            'totalCash': 100000000,
            'totalCashPerShare': 0.67,
            'ebitda': 50000000,
            'totalDebt': 200000000,
            'quickRatio': 1.2,
            'currentRatio': 1.5,
            'totalRevenue': 300000000,
            'debtToEquity': 1.3,
            'revenuePerShare': 2.0,
            'returnOnAssets': 0.06,
            'returnOnEquity': 0.12,
            'freeCashflow': 30000000,
            'operatingCashflow': 40000000,
            'earningsGrowth': 0.1,
            'revenueGrowth': 0.15,
            'grossMargins': 0.4,
            'ebitdaMargins': 0.17,
            'operatingMargins': 0.12,
            'financialCurrency': 'BRL',
            'trailingPegRatio': 1.5
        }
    },
    'OutraEmpresa': {
        # Adicione informações da próxima empresa aqui...
    }
}

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

# Pegar os dados estruturados da empresa selecionada
info_empresa = empresas_info.get(nome_acao_escolhida, {})

# Exibir informações estruturadas da empresa selecionada
if info_empresa:
    st.write(f"### Informações da Empresa: {nome_acao_escolhida}")
    st.json(info_empresa)
else:
    st.write(f"### Informações da Empresa: {nome_acao_escolhida} não estão disponíveis.")

# Pegar os dados online da ação escolhida
st.write(f"### Dados de {nome_acao_escolhida} ({sigla_acao_escolhida})")
dados_acao = pegar_valores_online(sigla_acao_escolhida)
st.write(dados_acao)








