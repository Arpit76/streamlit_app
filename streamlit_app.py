#streamlit run streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import duckdb
import plotly.express as px
import plotly.graph_objects as go

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


tab_page3, tab_page2, tab_page1 = st.tabs(["Sales DashBoard3", "Sales DashBoard2", "Sales DashBoard1"])



def loadTab1():    
    st.text("Welcome to Page123 Function == store_sales_2022-2023.csv")    
def loadTab2():  
    st.text("Welcome to Page456 Function == RetailStores.xlsx")
def loadTab3():  
    st.text("Welcome to Page789 Function == Financial Data Clean.xlsx")


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

def loadSalesData2():
    st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

    

    st.title("Sales Streamlit Dashboard")
    st.markdown("_Prototype v0.4.1_")

    with st.sidebar:
        st.header("Config")
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])


    if uploaded_file is None:
        st.info(" Upload a file through config", icon="ℹ️")
        st.stop()

    #######################################
    # DATA LOADING
    #######################################


    @st.cache_data
    def load_data(path: str):
        df = pd.read_excel(path)
        return df


    df = load_data(uploaded_file)
    duckdb.register("df", df)
    all_months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    with st.expander("Data Preview"):
        st.dataframe(
            df,
            column_config={"Year": st.column_config.NumberColumn(format="%d")},
        )

    #######################################
    # VISUALIZATION METHODS
    #######################################


    def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                value=value,
                gauge={"axis": {"visible": False}},
                number={
                    "prefix": prefix,
                    "suffix": suffix,
                    "font.size": 28,
                },
                title={
                    "text": label,
                    "font": {"size": 24},
                },
            )
        )

        if show_graph:
            fig.add_trace(
                go.Scatter(
                    y=random.sample(range(0, 101), 30),
                    hoverinfo="skip",
                    fill="tozeroy",
                    fillcolor=color_graph,
                    line={
                        "color": color_graph,
                    },
                )
            )

        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=False, fixedrange=True)
        fig.update_layout(
            # paper_bgcolor="lightgrey",
            margin=dict(t=30, b=0),
            showlegend=False,
            plot_bgcolor="white",
            height=100,
        )

        st.plotly_chart(fig, use_container_width=True)


    def plot_gauge(
        indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
    ):
        fig = go.Figure(
            go.Indicator(
                value=indicator_number,
                mode="gauge+number",
                domain={"x": [0, 1], "y": [0, 1]},
                number={
                    "suffix": indicator_suffix,
                    "font.size": 26,
                },
                gauge={
                    "axis": {"range": [0, max_bound], "tickwidth": 1},
                    "bar": {"color": indicator_color},
                },
                title={
                    "text": indicator_title,
                    "font": {"size": 28},
                },
            )
        )
        fig.update_layout(
            # paper_bgcolor="lightgrey",
            height=200,
            margin=dict(l=10, r=10, t=50, b=10, pad=8),
        )
        st.plotly_chart(fig, use_container_width=True)


    def plot_top_right():
        sales_data = duckdb.sql(
            f"""
            WITH sales_data AS (
                UNPIVOT ( 
                    SELECT 
                        Scenario,
                        business_unit,
                        {','.join(all_months)} 
                        FROM df 
                        WHERE Year='2023' 
                        AND Account='Sales' 
                    ) 
                ON {','.join(all_months)}
                INTO
                    NAME month
                    VALUE sales
            ),

            aggregated_sales AS (
                SELECT
                    Scenario,
                    business_unit,
                    SUM(sales) AS sales
                FROM sales_data
                GROUP BY Scenario, business_unit
            )
            
            SELECT * FROM aggregated_sales
            """
        ).df()

        fig = px.bar(
            sales_data,
            x="business_unit",
            y="sales",
            color="Scenario",
            barmode="group",
            text_auto=".2s",
            title="Sales for Year 2023",
            height=400,
        )
        fig.update_traces(
            textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
        )
        st.plotly_chart(fig, use_container_width=True)


    def plot_bottom_left():
        sales_data = duckdb.sql(
            f"""
            WITH sales_data AS (
                SELECT 
                Scenario,{','.join(all_months)} 
                FROM df 
                WHERE Year='2023' 
                AND Account='Sales'
                AND business_unit='Software'
            )

            UNPIVOT sales_data 
            ON {','.join(all_months)}
            INTO
                NAME month
                VALUE sales
        """
        ).df()

        fig = px.line(
            sales_data,
            x="month",
            y="sales",
            color="Scenario",
            markers=True,
            text="sales",
            title="Monthly Budget vs Forecast 2023",
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)


    def plot_bottom_right():
        sales_data = duckdb.sql(
            f"""
            WITH sales_data AS (
                UNPIVOT ( 
                    SELECT 
                        Account,Year,{','.join([f'ABS({month}) AS {month}' for month in all_months])}
                        FROM df 
                        WHERE Scenario='Actuals'
                        AND Account!='Sales'
                    ) 
                ON {','.join(all_months)}
                INTO
                    NAME year
                    VALUE sales
            ),

            aggregated_sales AS (
                SELECT
                    Account,
                    Year,
                    SUM(sales) AS sales
                FROM sales_data
                GROUP BY Account, Year
            )
            
            SELECT * FROM aggregated_sales
        """
        ).df()

        fig = px.bar(
            sales_data,
            x="Year",
            y="sales",
            color="Account",
            title="Actual Yearly Sales Per Account",
        )
        st.plotly_chart(fig, use_container_width=True)


    #######################################
    # STREAMLIT LAYOUT
    #######################################

    top_left_column, top_right_column = st.columns((2, 1))
    bottom_left_column, bottom_right_column = st.columns(2)

    with top_left_column:
        column_1, column_2, column_3, column_4 = st.columns(4)

        with column_1:
            plot_metric(
                "Total Accounts Receivable",
                6621280,
                prefix="$",
                suffix="",
                show_graph=True,
                color_graph="rgba(0, 104, 201, 0.2)",
            )
            plot_gauge(1.86, "#0068C9", "%", "Current Ratio", 3)

        with column_2:
            plot_metric(
                "Total Accounts Payable",
                1630270,
                prefix="$",
                suffix="",
                show_graph=True,
                color_graph="rgba(255, 43, 43, 0.2)",
            )
            plot_gauge(10, "#FF8700", " days", "In Stock", 31)

        with column_3:
            plot_metric("Equity Ratio", 75.38, prefix="", suffix=" %", show_graph=False)
            plot_gauge(7, "#FF2B2B", " days", "Out Stock", 31)
            
        with column_4:
            plot_metric("Debt Equity", 1.10, prefix="", suffix=" %", show_graph=False)
            plot_gauge(28, "#29B09D", " days", "Delay", 31)

    with top_right_column:
        plot_top_right()

    with bottom_left_column:
        plot_bottom_left()

    with bottom_right_column:
        plot_bottom_right()


with tab_page1:    
    data=loadTab1()
    data=loadSalesData()
with tab_page2:
    data=loadTab2()  
    data=loadSalesData1()
with tab_page3:    
    data=loadTab3()
    loadSalesData2()

       