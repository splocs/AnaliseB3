import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import ta
from ta.utils import dropna
import numpy as np

# Configuração inicial do Streamlit
st.set_page_config(page_title="Análise de Ações e FIIs", layout="wide")

# Função para obter dados financeiros de uma ação ou FII
@st.cache
def get_data(ticker):
    data = yf.download(ticker, start="2000-01-01")
    return data

# Função para plotar gráficos de indicadores técnicos
def plot_technical_indicators(data, ticker):
    # Preparar os dados
    data = dropna(data)
    
    # Cálculo dos indicadores técnicos
    data['SMA'] = ta.trend.sma_indicator(data['Close'], window=50)
    data['EMA'] = ta.trend.ema_indicator(data['Close'], window=50)
    data['MACD'] = ta.trend.macd(data['Close'])
    data['MACD_signal'] = ta.trend.macd_signal(data['Close'])
    data['Bollinger_High'] = ta.volatility.bollinger_hband(data['Close'])
    data['Bollinger_Low'] = ta.volatility.bollinger_lband(data['Close'])
    data['RSI'] = ta.momentum.rsi(data['Close'])
    
    st.write(f"### Indicadores Técnicos para {ticker}")
    
    # Plot SMA and EMA
    st.write("#### SMA e EMA")
    fig, ax = plt.subplots()
    ax.plot(data.index, data['Close'], label='Close')
    ax.plot(data.index, data['SMA'], label='SMA')
    ax.plot(data.index, data['EMA'], label='EMA')
    ax.set_title(f"SMA e EMA - {ticker}")
    ax.legend()
    st.pyplot(fig)
    
    # Plot MACD
    st.write("#### MACD")
    fig, ax = plt.subplots()
    ax.plot(data.index, data['MACD'], label='MACD')
    ax.plot(data.index, data['MACD_signal'], label='Signal Line')
    ax.set_title(f"MACD - {ticker}")
    ax.legend()
    st.pyplot(fig)
    
    # Plot Bollinger Bands
    st.write("#### Bandas de Bollinger")
    fig, ax = plt.subplots()
    ax.plot(data.index, data['Close'], label='Close')
    ax.plot(data.index, data['Bollinger_High'], label='Bollinger High')
    ax.plot(data.index, data['Bollinger_Low'], label='Bollinger Low')
    ax.set_title(f"Bandas de Bollinger - {ticker}")
    ax.legend()
    st.pyplot(fig)
    
    # Plot RSI
    st.write("#### Índice de Força Relativa (RSI)")
    fig, ax = plt.subplots()
    ax.plot(data.index, data['RSI'], label='RSI')
    ax.axhline(y=70, color='r', linestyle='--')
    ax.axhline(y=30, color='g', linestyle='--')
    ax.set_title(f"RSI - {ticker}")
    ax.legend()
    st.pyplot(fig)

# Função para exibir informações fundamentalistas
def display_fundamentals(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    st.write(f"### Informações Fundamentalistas para {ticker}")
    st.write(f"**Nome:** {info.get('shortName', 'N/A')}")
    st.write(f"**Setor:** {info.get('sector', 'N/A')}")
    st.write(f"**Indústria:** {info.get('industry', 'N/A')}")
    st.write(f"**Resumo:** {info.get('longBusinessSummary', 'N/A')}")
    st.write(f"**Valor de Mercado:** {info.get('marketCap', 'N/A')}")
    st.write(f"**Beta:** {info.get('beta', 'N/A')}")
    st.write(f"**Dividendo Anual:** {info.get('dividendYield', 'N/A')}")

# Função principal para executar o Streamlit
def main():
    st.title("Análise de Ações e FIIs")
    
    # Entrada do usuário para o ticker
    ticker = st.text_input("Digite o Ticker da Ação ou FII:", value='AAPL')
    
    if ticker:
        data = get_data(ticker)
        
        # Exibir gráficos de indicadores técnicos
        plot_technical_indicators(data, ticker)
        
        # Exibir informações fundamentalistas
        display_fundamentals(ticker)

# Executar o aplicativo Streamlit
if __name__ == "__main__":
    main()
