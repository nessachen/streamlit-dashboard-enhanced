import streamlit as st
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

title, button = st.columns([3, 1])

with title:
    st.header("2024 AHI 507 Streamlit Example") 

with button: 
    st.link_button("Go to My GitHub", "https://github.com/nessachen/streamlit-dashboard-enhanced.git")
st.subheader("We are going through a couple different examples of loading and visualizing information into this dashboard")

st.text("""In this streamlit dashboard, we are going to focus on some recently released data on school learning modalities from the NCES, for the years of 2020-2021""")

df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000")

## data cleaning 
df['weeks'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

st.write("")

## box to show how many rows and columns of data we have: 
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1]) 
col2.metric("Rows", len(df))
col3.metric("Number of unique districts:", df['district_name'].nunique())

st.write("")


## exposing first 1k of NCES 20-21 data
st.dataframe(df)

# descriptive statistics on student count
st.write("**The following table displays the different descriptive statistics conducted on the student count data:**")

student_stats = df['student_count'].describe()

st.subheader("Summary Statistics Table")
st.table(student_stats)

## line chart by week 
table = pd.pivot_table(df, values='student_count', index=['week'],
                       columns=['learning_modality'], aggfunc="sum")

table = table.reset_index()

st.write("")

st.write("**The following three bar chart is categorized by learning modalities and displays the student count for each learning modality by week:**")

st.bar_chart(
    table,
    x="week",
    y="Hybrid",
)

st.bar_chart(
    table,
    x="week",
    y="In Person",
)

st.bar_chart(
    table,
    x="week",
    y="Remote",
)

# pie chart for learning modalities 
st.write("")

st.write("**The following pie chart represents the percentage count for each learning modality in the dataset:**")
df = df.dropna(subset=['learning_modality'])
pieces = df['learning_modality'].value_counts()
labels = pieces.index

fig, ax = plt.subplots()
fig.patch.set_alpha(0) 
ax.pie(pieces, labels=labels, autopct='%1.1f%%', startangle=140, radius=0.1)
ax.axis('equal') 

st.pyplot(fig)

st.write("")

rating, thanks = st.columns([3, 1])

# feedback button
feedback = st.text_area("Please give me feedback on the dashboard:")

if st.button('Submit') and feedback:
    st.write("Thank you!")

st.write("")

# feedback widget for rating 
with rating:
    st.write("Please rate your experience with the dashboard!")
    feedback = st.feedback(options="faces")

st.write("")

# thank you button
with thanks:
    if st.button('Click me for a message 🙂'):
        st.write('Thank you for viewing my Streamlit dashboard!')
