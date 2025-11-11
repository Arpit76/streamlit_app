#streamlit run streamlit_app.py
import streamlit as st
import tab1,tab2,tab3

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


with tab_page1:    
    #data=tab1.loadTab1()
    data=tab1.loadSalesData()
with tab_page2:
    #data=tab2.loadTab2()  
    data=tab2.loadSalesData1()
with tab_page3:    
    #data=tab3.loadTab3()
    data=tab3.loadSalesData2()

       