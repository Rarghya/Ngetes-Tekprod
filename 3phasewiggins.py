import streamlit as st
import plotly.express as px
import pandas as pd  
st.header('Three Phase Inflow Performance Relationship')
st.subheader('Wiggins Method')
st.warning('#TEKPRODCEPE')

well = st.text_input('Well Name: ')
q = st.number_input('Flowrate (STBD)')
pwf = st.number_input('Pwf (Psia)')
pres = st.number_input('Reservoir Pressure (Psia)')
wc = st.number_input('Water Cut (%)')

qwpwf = q*(wc/100)
qopwf = q*(1-(wc/100))
qomax = qopwf/(1-(0.52*(pwf/pres))-(0.48*((pwf/pres)**2)))
qwmax = qwpwf/(1-(0.72*(pwf/pres))-(0.28*((pwf/pres)**2)))

pwflist=[pres]
qolist=[0]
qwlist=[0]
qlist=[0]
qdict={'Pwf':pwflist,'Qo':qolist,'Qw':qwlist,'Q':qlist}
pwfb=pres-100

while pwfb > 100:
    pwflist.append(pwfb)
    qo = qomax*(1-(0.52*(pwfb/pres))-(0.48*((pwfb/pres)**2)))
    qolist.append(qo)
    qw = qwmax*(1-(0.72*(pwfb/pres))-(0.28*((pwfb/pres)**2)))
    qwlist.append(qw)
    qt = qo+qw
    qlist.append(qt)
    pwfb=pwfb-100
else:
    pwf0=0
    pwflist.append(pwf0)
    qtmax=qomax+qwmax
    qolist.append(qomax)
    qwlist.append(qwmax)
    qlist.append(qtmax)

qdf = pd.DataFrame(qdict)
plot = px.line(qdf,x='Pwf',y=['Q','Qw','Qo'],labels={'Pwf':'Psia','value':'Stbd'})

ops=st.radio('Show',['Data','IPR Chart'])
if ops == 'Data':
    st.write('Data of {} Well'.format(well))
    st.dataframe(qdf)
elif ops == 'IPR Chart':
    st.write('IPR chart of {} Well'.format(well))
    st.write(plot)