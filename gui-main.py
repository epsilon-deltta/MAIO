import streamlit as st
import pandas as pd
import numpy as np
from maio import keywordTrend as kt

import random as rd
st.title('MAIO : Marketing All In One ')
def keywd(kwd):
    trend = kt(kwd)
    kwd10 = trend.get_keywords()
    return kwd10

st.header('Keywords Master 😁')

# value = "palceholder"
label = "Search keyword"
sch_kw = st.text_input(
                        label=label,
                        # value=value
                        )
sch_btn = st.button("Search")
item_n = st.slider(
    'Select the number of keywords',
    0, 100, (0, 30)
)

if sch_btn:
    ktrend = kt(sch_kw)
    kwd30 = ktrend.get_keywords(item_n[1])
    kwd10 = ktrend.get_keywords()
    st.write(kwd30)

    coords = ktrend.get_df_coordis(start=0,end=5)
    st.line_chart(coords)
    
    coords = ktrend.get_df_coordis(start=5)
    st.line_chart(coords)
    

## get sample 3
# kwds_opts = st.button('')
# if kwds_opts :
#     rds = rd.sample(kwd10,3)
#     st.write(rds)

# layout
# Add a selectbox to the sidebar:

## sidebar
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )


## Column layout
# left_column, right_column = st.beta_columns(2)
# # You can use a column just like st.sidebar:
# left_column.button('Press me!')


# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")



##  Radio
# selected_item = st.radio("Radio Part", ("A", "B", "C"))

# if selected_item == "A":
#     st.write("A!!")
# elif selected_item == "B":
#     st.write("B!")
# elif selected_item == "C":
#     st.write("C!")