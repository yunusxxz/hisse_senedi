import streamlit as st
from datetime import datetime
import yfinance as yf


ticker = st.sidebar.text_input('Hisse Senedi Sembolü', value='ASELS')
st.title(ticker + " Hisse Senedi Grafiği")


start_date = st.sidebar.date_input("Başlangıç Tarihi", value=datetime(2022, 1, 1))
end_date = st.sidebar.date_input("Bitiş Tarihi", value=datetime.now())


df = yf.download(ticker + '.IS', start=start_date, end=end_date)


options = st.sidebar.multiselect(
    'Gösterilecek Veriler',
    ['Close', 'Open', 'Volume'],
    default=['Close']
)


st.subheader("Seçilen Verilerin Trend Grafiği")
if not df.empty:
    st.line_chart(df[options])


    sma_window = st.sidebar.slider('Hareketli Ortalama Penceresi (Gün)', 5, 100, 20)
    df['SMA'] = df['Close'].rolling(sma_window).mean()
    st.line_chart(df[['Close', 'SMA']])

    st.subheader("Fiyat Tablosu")
    st.write(df)

    st.download_button(
        label="Verileri CSV olarak indir",
        data=df.to_csv(),
        file_name=f'{ticker}_data.csv',
        mime='text/csv'
    )
else:
    st.write("Veri bulunamadı.")

second_ticker = st.sidebar.text_input('İkinci Hisse Senedi Sembolü', value='KOZAL')

second_df = yf.download(second_ticker + '.IS', start=start_date, end=end_date)

if not second_df.empty:
    st.subheader(f"{ticker} ve {second_ticker} Karşılaştırma Grafiği")
    combined_df = df[['Close']].rename(columns={'Close': ticker}).join(
        second_df[['Close']].rename(columns={'Close': second_ticker}), how='inner'
    )
    st.line_chart(combined_df)




