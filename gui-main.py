import streamlit as st
import pandas as pd
import numpy as np
from maio import keywordTrend as kt

st.title('MAIO : Marketing All In One ')
def keywd(kwd):
    trend = kt(kwd)
    kwd10 = trend.get_keywords()
    return kwd10

st.header('Keywords Master 😁')

# value = "Search Keyword"
label = "Search keyword"
sch_kw = st.text_input(
                        label=label,
                        # value=value
                        )

if st.button("Search"):
    ktrend = kt(sch_kw)
    kwd10 = ktrend.get_keywords()
    st.write(kwd10)

    coords = ktrend.get_df_coordis(start=0,end=5)
    st.line_chart(coords)
    
    coords = ktrend.get_df_coordis(start=5)
    st.line_chart(coords)
    # 데이터 로딩 함수는 여기에!

