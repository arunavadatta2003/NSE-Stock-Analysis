# Import the libraries
import streamlit as st
import pandas as pd

# Add a title and an image
st.write("""
# Area Converter Web Application
created by **Arunava Datta**
""")

# Set the Background and sidebar
st.markdown("""
<style>
body {
    background-color: #46484a;
    color: white;
}
.sidebar .sidebar-content {
    background-image: linear-gradient(#315168,#315168);
    color: white;
}
</style>
    """, unsafe_allow_html=True)

# Create a function to get user inputs
st.header('User Input')
st.subheader('Input Area in Sq.M.')
x = st.number_input("",0.0)

sq_ft = round(x * 10.764,2)
st.write('Area in Sq.ft. -',sq_ft,' Sq.ft.')

acres = round(x * 0.000247105,4)
st.write('Area in Acres -', acres, 'acres')

bigha = int(sq_ft//(20*720))

r1 = sq_ft-(bigha*20*720)
kh = int(r1//720)

r2 = sq_ft - ((bigha*20*720)+(kh*720))
ch = int(r2//45)

r3 = round(sq_ft - ((bigha*20*720)+(kh*720)+(ch*45)),2)

d = {'Bigha':[bigha], 'Katha':[kh], 'Chattak':[ch], 'Sq.ft.':[r3]}
df = pd.DataFrame(data=d)
df['Sq.ft.'] = df['Sq.ft.'].map('{0:g}'.format)
st.subheader('Area in Bigha - Katha - Chattak')
st.write(df)

if x <=200:
    y = 65
elif x >= 500:
    y = 50
elif 200 < x < 500:
    y = round(50 + (0.05*(500 - x)),2)
st.write('Permissible Ground Coverage -',y,"%")
coverage = (x*y)/100
st.write('Permissible Ground Coverage -',coverage,"Sq.M.")
