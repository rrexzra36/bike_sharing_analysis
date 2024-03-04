import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
data_url = "dashboard/day_clean.csv"
day_df = pd.read_csv(data_url)

# Create streamlit app
st.title('Visualisasi Data Pengguna Sepeda')

# Add tabs
tabs = ["Question 1", "Question 2", "RFM Analysis"]
selected_tab = st.sidebar.selectbox("Select Question", tabs)

if selected_tab == "Question 1":
    st.write(
    """
    # Question 1
    Bagaimana perbedaan penggunaan sepeda pada hari kerja (_working day_), hari libur (_holiday_), dan hari biasa (weekday) dalam hal jumlah perjalanan, rata-rata waktu perjalanan, dan pola penggunaan lainnya?
    """
    )
    
    # Berdasarkan weekday
    st.subheader('Jumlah Pengguna Sepeda berdasarkan Hari dalam Seminggu (Weekday)')
    fig_weekday, ax_weekday = plt.subplots(figsize=(10, 6))
    ax_weekday.bar(day_df['weekday'], day_df['count'])
    ax_weekday.set_xlabel('Hari dalam Seminggu')
    ax_weekday.set_ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig_weekday)

    # Berdasarkan workingday
    st.subheader('Jumlah Pengguna Sepeda berdasarkan Hari Kerja (Working Day)')
    fig_workingday, ax_workingday = plt.subplots(figsize=(10, 6))
    ax_workingday.bar(day_df['workingday'], day_df['count'])
    ax_workingday.set_xlabel('Hari Kerja')
    ax_workingday.set_ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig_workingday)

    # Berdasarkan holiday
    st.subheader('Jumlah Pengguna Sepeda berdasarkan Hari Libur (Holiday)')
    fig_holiday, ax_holiday = plt.subplots(figsize=(10, 6))
    ax_holiday.bar(day_df['holiday'], day_df['count'])
    ax_holiday.set_xlabel('Hari Libur')
    ax_holiday.set_ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig_holiday)

elif selected_tab == "Question 2":
    st.write(
    """
    # Question 2
    Dalam jangka waktu satu tahun, bagaimana tren penggunaan sepeda berubah antara tahun 2011 dan 2012? Apakah terdapat perbedaan signifikan dalam jumlah perjalanan, pola penggunaan, atau faktor lain yang dapat mempengaruhi keputusan bisnis terkait promosi atau alokasi sumber daya?
    """
    )

    # Menginisialisasi palet warna
    palette_colors = ['red', 'blue']

    # Menyiapkan data
    monthly_counts = day_df.groupby(by=["month","year"]).agg({
        "count": "sum"
    }).reset_index()
    monthly_counts_2011 = monthly_counts[monthly_counts['year'] == 0]
    monthly_counts_2012 = monthly_counts[monthly_counts['year'] == 1]

    # Plot menggunakan pyplot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_counts_2011['month'], monthly_counts_2011['count'], marker='o', color=palette_colors[0], label='2011')
    ax.plot(monthly_counts_2012['month'], monthly_counts_2012['count'], marker='o', color=palette_colors[1], label='2012')

    # Menambahkan judul dan label sumbu
    ax.set_title('Jumlah total sepeda yang disewakan berdasarkan Bulan dan Tahun')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Total Sepeda Disewakan')

    # Menambahkan legenda
    ax.legend(title='Tahun', loc='upper right')

    # Menampilkan plot
    st.pyplot(fig)

elif selected_tab == "RFM Analysis":
    st.write(
    """
    # RFM Analysis
    Dalam jangka waktu satu tahun, bagaimana tren penggunaan sepeda berubah antara tahun 2011 dan 2012? Apakah terdapat perbedaan signifikan dalam jumlah perjalanan, pola penggunaan, atau faktor lain yang dapat mempengaruhi keputusan bisnis terkait promosi atau alokasi sumber daya?
    """
    )
    st.write("- Recency: parameter yang digunakan untuk melihat kapan terakhir seorang pelanggan melakukan transaksi.")
    st.write("- Frequency: parameter ini digunakan untuk mengidentifikasi seberapa sering seorang pelanggan melakukan transaksi.")
    st.write("- Monetary: parameter terakhir ini digunakan untuk mengidentifikasi seberapa besar revenue yang berasal dari pelanggan tersebut.")

    # Membuat Dataframe RFM Analysis
    rfm_df = day_df.groupby(by="weekday", as_index=False).agg({
        "dateday": "max", # retrieve the date of the last order
        "instant": "nunique", # calculate the order quantity
        "count": "sum" # calculate the amount of revenue generated
    })

    rfm_df.columns = ["weekday", "max_order_timestamp", "frequency", "monetary"]

    # Kalkulasi transaksi terkahir
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].astype('datetime64[ns]').dt.date
    recent_date = day_df["dateday"].astype('datetime64[ns]').dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    st.write(rfm_df)

    # Data
    recency_data = rfm_df.sort_values(by="recency", ascending=True).head(5)
    frequency_data = rfm_df.sort_values(by="frequency", ascending=False).head(5)
    monetary_data = rfm_df.sort_values(by="monetary", ascending=False).head(5)

    # Create streamlit app
    st.subheader('RFM Analysis Visualization')
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_recency = round(rfm_df.recency.mean(), 1)
        st.metric("Average Recency (days)", value=avg_recency)

    with col2:
        avg_frequency = round(rfm_df.frequency.mean(), 2)
        st.metric("Average Frequency", value=avg_frequency)

    with col3:
        st.metric("Average Monetary", value=rfm_df.monetary.mean())

    # Plotting dengan pyplot
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

    # Plot by Recency
    ax[0].bar(recency_data['weekday'], recency_data['recency'], color='#72BCD4')
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title('By Recency (days)', loc='center', fontsize=18)
    ax[0].tick_params(axis ='x', labelsize=15)

    # Plot by Frequency
    ax[1].bar(frequency_data['weekday'], frequency_data['frequency'], color='#72BCD4')
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title('By Frequency', loc='center', fontsize=18)
    ax[1].tick_params(axis='x', labelsize=15)

    # Plot by Monetary
    ax[2].bar(monetary_data['weekday'], monetary_data['monetary'], color='#72BCD4')
    ax[2].set_ylabel(None)
    ax[2].set_xlabel(None)
    ax[2].set_title('By Monetary', loc='center', fontsize=18)
    ax[2].tick_params(axis='x', labelsize=15)

    # Title
    plt.suptitle('Best Customer Based on RFM Parameters (day)', fontsize=20)

    # Display plot
    st.pyplot(fig)


