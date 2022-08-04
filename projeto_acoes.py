import investpy as ip
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objs as go

paises = ['Brazil', 'United States', 'Spain', 'Canada']
intervalos = ['Daily', 'Weekly', 'Monthly']

data_inicio = datetime.today() - timedelta(days=30)
data_final = datetime.today()

@st.cache
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(stock=stock, country=country, from_date=from_date,to_date=to_date, interval=interval)
    return df
def formatar_data(dt, format='%d/%m/%Y'):
    return dt.strftime(format)

def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }

    data = [trace1]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig

############################### Criando as opções em uma barra lateral esquerda
barra_lateral = st.sidebar.empty()
country_select = st.sidebar.selectbox("Selecione o país:", paises)
acoes = ip.get_stocks_list(country=country_select)
stock_select = st.sidebar.selectbox("Selecione o ativo:", acoes)
from_date = st.sidebar.date_input('De:', data_inicio)
to_date = st.sidebar.date_input('Para:', data_final)
interval_select = st.sidebar.selectbox("Selecione o interval:", intervalos)
carregar_dados = st.sidebar.checkbox('Carregar dataframe na página')

grafico_line = st.empty()
grafico_candle = st.empty()

st.title('Monitor de Ações')

st.subheader('Visualização gráfica')


#### Elementos da página
if from_date > to_date:
    st.sidebar.error('Data de ínicio maior do que data final')
else:
    df = consultar_acao(stock_select, country_select, formatar_data(from_date), formatar_data(to_date), interval_select)
    try:
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_linha = st.line_chart(df.Close)
        if carregar_dados:
            st.subheader('Dados')
            dados = st.dataframe(df)
            stock_select = st.sidebar.selectbox
    except Exception as e:
        st.error(e)