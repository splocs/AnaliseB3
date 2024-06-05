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

# Dicionário estruturado da Helbor (exemplo com dados da Amazon)
helbor_info = {
    'companyInfo': {
        'address1': '410 Terry Avenue North',
        'city': 'Seattle',
        'state': 'WA',
        'zip': '98109-5210',
        'country': 'United States',
        'phone': '206 266 1000',
        'website': 'https://www.aboutamazon.com',
    },
    'industryInfo': {
        'industry': 'Internet Retail',
        'industryKey': 'internet-retail',
        'industryDisp': 'Internet Retail',
        'sector': 'Consumer Cyclical',
        'sectorKey': 'consumer-cyclical',
        'sectorDisp': 'Consumer Cyclical',
    },
    'summary': {
        'longBusinessSummary': "Amazon.com, Inc. engages in the retail sale of consumer products, advertising, and subscriptions service through online and physical stores in North America and internationally. The company operates through three segments: North America, International, and Amazon Web Services (AWS). It also manufactures and sells electronic devices, including Kindle, Fire tablets, Fire TVs, Echo, Ring, Blink, and eero; and develops and produces media content. In addition, the company offers programs that enable sellers to sell their products in its stores; and programs that allow authors, independent publishers, musicians, filmmakers, Twitch streamers, skill and app developers, and others to publish and sell content. Further, it provides compute, storage, database, analytics, machine learning, and other services, as well as advertising services through programs, such as sponsored ads, display, and video advertising. Additionally, the company offers Amazon Prime, a membership program. The company's products offered through its stores include merchandise and content purchased for resale and products offered by third-party sellers. It serves consumers, sellers, developers, enterprises, content creators, advertisers, and employees. Amazon.com, Inc. was incorporated in 1994 and is headquartered in Seattle, Washington."
    },
    'employees': {
        'fullTimeEmployees': 1525000,
        'companyOfficers': [
            {'maxAge': 1, 'name': 'Mr. Jeffrey P. Bezos', 'age': 59, 'title': 'Founder & Executive Chairman', 'yearBorn': 1964, 'fiscalYear': 2023, 'totalPay': 1681840, 'exercisedValue': 0, 'unexercisedValue': 0},
            {'maxAge': 1, 'name': 'Mr. Andrew R. Jassy', 'age': 55, 'title': 'President, CEO & Director', 'yearBorn': 1968, 'fiscalYear': 2023, 'totalPay': 1722764, 'exercisedValue': 0, 'unexercisedValue': 0},
            {'maxAge': 1, 'name': 'Mr. Brian T. Olsavsky', 'age': 59, 'title': 'Senior VP & CFO', 'yearBorn': 1964, 'fiscalYear': 2023, 'totalPay': 371600, 'exercisedValue': 0, 'unexercisedValue': 0},
            {'maxAge': 1, 'name': 'Mr. David A. Zapolsky', 'age': 59, 'title': 'Senior VP of Global Public Policy & General Counsel', 'yearBorn': 1964, 'fiscalYear': 2023, 'totalPay': 371600, 'exercisedValue': 0, 'unexercisedValue': 0},
            {'maxAge': 1, 'name': 'Mr. Douglas J. Herrington', 'age': 56, 'title': 'Chief Executive Officer of Worldwide Amazon Stores', 'yearBorn': 1967, 'fiscalYear': 2023, 'totalPay': 394231, 'exercisedValue': 0, 'unexercisedValue': 0},
            {'maxAge': 1, 'name': 'Mr. Albert  Cheng', 'title': 'Vice President of Prime Video U.S.', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0},
            {'maxAge': 1, 'name': 'Dr. Matt  Wood', 'title': 'Vice President of Artificial Intelligence - AWS', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0},
            {'maxAge': 1, 'name': 'Ms. Kara  Hurst', 'title': 'Vice President of Worldwide Sustainability', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0},
            {'maxAge': 1, 'name': 'Mr. Peter  Larsen', 'title': 'Vice President of Multi-Channel Fulfillment & buy with Prime', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0},
            {'maxAge': 1, 'name': 'Jon  Jenkins', 'title': 'Vice President of Just Walk Out', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}
        ]
    },
    'risk': {
        'auditRisk': 5,
        'boardRisk': 10,
        'compensationRisk': 10,
        'shareHolderRightsRisk': 3,
        'overallRisk': 9,
        'governanceEpochDate': 1717200000,
        'compensationAsOfEpochDate': 1703980800
    },
    'investorRelations': {
        'irWebsite': 'http://phx.corporate-ir.net/phoenix.zhtml?c=97664&p=irol-irhome',
        'maxAge': 86400
    },
    'stockInfo': {
        'priceHint': 2,
        'previousClose': 178.34,
        'open': 177.69,
        'dayLow': 176.44,
        'dayHigh': 179.82,
        'regularMarketPreviousClose': 178.34,
        'regularMarketOpen': 177.69,
        'regularMarketDayLow': 176.44,
        'regularMarketDayHigh': 179.82,
        'beta': 1.155,
        'trailingPE': 50.235294,
        'forwardPE': 31.135414,
        'volume': 26430843,
        'regularMarketVolume': 26430843,
        'averageVolume': 39073798,
        'averageVolume10days': 34714520,
        'averageDailyVolume10Day': 34714520,
        'bid': 179.22,
        'ask': 179.32,
        'bidSize': 100,
        'askSize': 100,
        'marketCap': 1866319527936,
        'fiftyTwoWeekLow': 118.35,
        'fiftyTwoWeekHigh': 191.7,
        'priceToSalesTrailing12Months': 3.159291,
        'fiftyDayAverage': 182.2718,
        'twoHundredDayAverage': 157.30865,
        'currency': 'USD',
        'enterpriseValue': 1941810577408,
        'profitMargins': 0.06379,
        'floatShares': 9262106532,
        'sharesOutstanding': 10406599680,
        'sharesShort': 70812929,
        'sharesShortPriorMonth': 75734073,
        'sharesShortPreviousMonthDate': 1713139200,
        'dateShortInterest': 1715731200,
        'sharesPercentSharesOut': 0.0068,
        'heldPercentInsiders': 0.09155,
        'heldPercentInstitutions': 0.63642,
        'shortRatio': 1.55,
        'shortPercentOfFloat': 0.0076,
        'impliedSharesOutstanding': 10406599680,
        'bookValue': 20.827,
        'priceToBook': 8.610938,
        'lastFiscalYearEnd': 1703980800,
        'nextFiscalYearEnd': 1735603200,
        'mostRecentQuarter': 1711843200,
        'earningsQuarterlyGrowth': 2.288,
        'netIncomeToCommon': 37683998720,
        'trailingEps': 3.57,
        'forwardEps': 5.76,
        'pegRatio': 1.29,
        'lastSplitFactor': '20:1',
        'lastSplitDate': 1654473600,
        'enterpriseToRevenue': 3.287,
        'enterpriseToEbitda': 20.1,
        '52WeekChange': 0.47933674,
        'SandP52WeekChange': 0.23990989,
        'exchange': 'NMS',
        'quoteType': 'EQUITY',
        'symbol': 'AMZN',
        'underlyingSymbol': 'AMZN',
        'shortName': 'Amazon.com, Inc.',
        'longName': 'Amazon.com, Inc.',
        'firstTradeDateEpochUtc': 863703000,
        'timeZoneFullName': 'America/New_York',
        'timeZoneShortName': 'EDT',
        'uuid': '261fd26b-0151-3813-b0d0-97e4ed4c6505',
        'messageBoardId': 'finmb_18749',
        'gmtOffSetMilliseconds': -14400000,
        'currentPrice': 179.34,
        'targetHighPrice': 500.0,
        'targetLowPrice': 180.0,
        'targetMeanPrice': 227.1,
        'targetMedianPrice': 220.0,
        'recommendationMean': 1.7,
        'recommendationKey': 'buy',
        'numberOfAnalystOpinions': 53,
    },
    'financials': {
        'totalCash': 85074001920,
        'totalCashPerShare': 8.175,
        'ebitda': 96609001472,
        'totalDebt': 160560005120,
        'quickRatio': 0.829,
        'currentRatio': 1.072,
        'totalRevenue': 590739996672,
        'debtToEquity': 74.107,
        'revenuePerShare': 57.133,
        'returnOnAssets': 0.059510004,
        'returnOnEquity': 0.20305,
        'freeCashflow': 57269751808,
        'operatingCashflow': 99146997760,
        'earningsGrowth': 2.167,
        'revenueGrowth': 0.125,
        'grossMargins': 0.47594002,
        'ebitdaMargins': 0.16354,
        'operatingMargins': 0.106809996,
        'financialCurrency': 'USD',
        'trailingPegRatio': 1.914
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

# Exibir dados estruturados da Helbor (substitua 'helbor_info' pelos dados reais da Helbor)
if nome_acao_escolhida == 'Helbor':
    st.write('### Informações da Empresa:')
    st.json(helbor_info)

    # Pegar os dados online da ação escolhida
    st.write(f"### Dados de {nome_acao_escolhida} ({sigla_acao_escolhida})")
    dados_acao = pegar_valores_online(sigla_acao_escolhida)
    st.write(dados_acao)
else:
    # Pegar os dados online da ação escolhida
    st.write(f"### Dados de {nome_acao_escolhida} ({sigla_acao_escolhida})")
    dados_acao = pegar_valores_online(sigla_acao_escolhida)
    st.write(dados_acao)








