import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def loadTab2():  
    st.text("Welcome to Page456 Function == RetailStores.xlsx")

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
