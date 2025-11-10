#streamlit run streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

st.set_page_config(layout="wide") 
st.markdown("""
        <style>
        .block-container {
            padding-top: 0rem; /* Adjust this value to your preference */
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        </style>
        """, unsafe_allow_html=True)


tab_page1, tab_page2 = st.tabs(["Sales DashBoard1", "Sales DashBoard2"])
def loadTab1():    
    st.text("Welcome to Page123 Function == store_sales_2022-2023.csv")    
def loadTab2():  
    st.text("Welcome to Page456 Function == RetailStores.xlsx")


def loadSalesData():    
    #Configs
    YEAR=2023
    CITIES = ["Tokyo", "Yokohama", "Osaka"]
    DATA_URL="store_sales_2022-2023.csv"

    # Page Setup
    # to pick windows Emoji icon - press windows and .
    st.set_page_config(page_title="Sales Dashboard", page_icon="📈")

    st.title("Sales Dashboard")

    # --- HIDE STREAMLIT BRANDING ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)



    #load Data
    #data=pd.read_csv(data_url)


    @st.cache_data  # This will load the data only once
    def load_data(data_url):
        return pd.read_csv(data_url).assign(  # Lambda Function Better way
            date_of_sale=lambda df: pd.to_datetime(df["date_of_sale"]),  # convert to Date time
            month=lambda df: df["date_of_sale"].dt.month,  # Extract month
            year=lambda df: df["date_of_sale"].dt.year,  # Extract year
        )


    #data = load_data(DATA_URL)



    data = load_data(DATA_URL)
    #st.dataframe(data)

    # Calculate total revenue for each city and year, and then calculate the percentage change
    city_revenues = (
        data.groupby(["city", "year"])["sales_amount"]
        .sum()
        .unstack()
        .assign(change=lambda x: x.pct_change(axis=1)[YEAR] * 100)
    )

    #st.dataframe(city_revenues)

    # Key Metric
    # display each city data in seprate column
    left_col, middle_col, right_col=st.columns(3)

    with left_col:
        st.metric(
            label=CITIES[0],
            value=f"$ {city_revenues.loc[CITIES[0], YEAR]:,.2f}",
            delta=f"{city_revenues.loc[CITIES[0], 'change']:.2f}% vs. Last Year",
        )

    # City 2 in the middle column
    with middle_col:
        st.metric(
            label=CITIES[1],
            value=f"$ {city_revenues.loc[CITIES[1], YEAR]:,.2f}",
            delta=f"{city_revenues.loc[CITIES[1], 'change']:.2f}% vs. Last Year",
        )

    # City 3 in the right column
    with right_col:
        st.metric(
            label=CITIES[2],
            value=f"$ {city_revenues.loc[CITIES[2], YEAR]:,.2f}",
            delta=f"{city_revenues.loc[CITIES[2], 'change']:.2f}% vs. Last Year",
        )


        # --- SELECTION FIELDS ---
    # City & Year selection
    selected_city = st.selectbox("Select a city:", CITIES)
    show_previous_year = st.toggle("Show Previous Year")
    if show_previous_year:
        visualization_year = YEAR - 1
    else:
        visualization_year = YEAR
    st.write(f"**Sales for {visualization_year}**")

    # Tabs for analysis type
    tab_month, tab_category = st.tabs(["Monthly Analysis", "Category Analysis"])

    # --- FILTER & VISUALIZE DATA ---
    with tab_month:
        filtered_data = (
            data.query("city == @selected_city & year == @visualization_year")
            .groupby("month", dropna=False, as_index=False)["sales_amount"]
            .sum()
        )
        st.bar_chart(
            data=filtered_data.set_index("month")["sales_amount"],
        )

    with tab_category:
        filtered_data = (
            data.query("city == @selected_city & year == @visualization_year")
            .groupby("product_category", dropna=False, as_index=False)["sales_amount"]
            .sum()
        )
        st.bar_chart(
            data=filtered_data.set_index("product_category")["sales_amount"],
        )

def loadSalesData1():    
    df = pd.read_excel('RetailStores.xlsx')
    df.head()
    store_df = df.pivot(
	index = 'StoreID',
	columns ='Product Category',
	values = 'Stock sold'
    )
    store_df.head()
    st.dataframe(store_df)

    from sklearn.cluster import KMeans
    k_means_model=KMeans(n_clusters=4)

    k_means_model.fit(store_df)

    store_df['cluster']=k_means_model.predict(store_df)

    store_df.head(100)
    filtered_df=store_df[store_df['cluster']!=0]
    filtered_df.head()
    grouped_data = store_df.groupby('cluster').sum()
    grouped_data.head()
    #plt.scatter(store_df['Frozen foods'],store_df['Groceries'],c=store_df['cluster'])


    st.scatter_chart(
    store_df,
    x='Frozen foods',
    y='Groceries',
    color='cluster'
)
    


    #grouped_data['Frozen foods'].hist()
    #plt.title('Frozen foods histogram')
    #plt.show()

# Create a matplotlib figure
    fig, ax = plt.subplots()
    grouped_data['Frozen foods'].hist(ax=ax)
    ax.set_title('Frozen foods histogram')

# Display the plot in Streamlit
    st.pyplot(fig)

with tab_page1:    
    data=loadTab1()
    data=loadSalesData()
with tab_page2:
    data=loadTab2()  
    data=loadSalesData1()
       