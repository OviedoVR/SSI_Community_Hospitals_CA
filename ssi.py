# --- Python Modules:
import numpy as np
import pandas as pd
import plotly.express as px
from custom_white import *
import streamlit as st

# --- Data Collection:
ssi_ca = pd.read_csv('./data/ssi_data.csv')

facilities_count = len(ssi_ca.Facility_ID.unique())

# --- Header:
st.title('Surgical Site Infections (SSI) in CA')
st.write(f'Data from {facilities_count} community hospitalar facilites in 2017')
st.markdown('---')
st.markdown("""**SSI** are those infections that occurs after a surgical procedure and 
            can result in:<br> **1.** Additional costs to the hospital,<br> **2.** Longer patient staying time,<br>
            **3.** Unexpected readimissions,<br> **4.** Deaths.<br> Thus, preventing or reducing SSI plays 
            a great role in healthcare facilities. Considering a **benchmark of 3\%** for **SSI**,
            could you quickly get those facilities performing bad (SSI > benchmark)? 
            With this *Streamlit app* you could do that by procedure category and procedure type.
            """, unsafe_allow_html=True)
st.markdown('---')

# --- Dropdown menus:
left_menu, right_menu = st.columns(2)


with left_menu:
    procedure_cat = st.selectbox(
        'Procedure Category',
        ssi_ca['Procedure_Category'].unique())
with right_menu:
    
    ssi_ca = ssi_ca[ssi_ca['Procedure_Category'] == procedure_cat]
    operative_proced = st.selectbox(
        'Operative Procedure',
        ssi_ca['Operative_Procedure'].unique())
    
    ssi_ca = ssi_ca[ssi_ca['Operative_Procedure'] == operative_proced]

# --- Query the data:
ssi_query = ssi_ca
above_benchmark = ssi_query.query('Performance == "Bad"')['Facility_ID'].unique()
query_facilities_count = len(ssi_query.Facility_ID.unique())

# --- Big Numbers:
l, c, r = st.columns(3)

with l:
    st.metric(label='Facilities', value=query_facilities_count)
with c:
    try:
        st.metric(label="Facilities Performing bad (Count)", value=len(above_benchmark))
    except:
        st.metric(label="Facilities Performing well (count)", value='No data')
        
with r:
    try:
        st.metric(label="Facilities Performing bad (%)", value=f'{round(len(above_benchmark)/query_facilities_count*100, 2)} %', delta=None)
    except:
        st.metric(label="Facilities Performing well (%)", value='No data', delta=None)

# --- Create a strip plot:
fig = px.strip(
    ssi_ca,
    y='SSI_ratio',
    facet_col='Hospital_Type',
    hover_data=['Procedure_Count', 'Infection_Count'],
    hover_name='Facility_ID',
    color='Performance',
    color_discrete_sequence=['whitesmoke', '#e87b0e'],
    facet_col_wrap=4,
    stripmode='overlay'
)

# Add a reference line at y = 3% (SSI Benchmark)
fig.add_hline(y=3, line_dash='dash', line_color='#e87b0e', line_width=2, annotation_text='SSI = 3%', annotation_font_color='#e87b0e')

# Update the layout:
fig.update_layout(
    height=450,
    title='SSI ratio (%) by facility',
    xaxis_title='',
    yaxis_title='',
    title_x=0.075,
    title_font_size=24,
    legend_title='Performance against benchmark - greater SSI values indicate a bad performance',
    legend=dict(orientation="h", x=-0.01,y=-0.05)
)
fig.update_xaxes(matches=None)
fig.update_traces(marker=custom_marker_style)
st.markdown('######')
st.plotly_chart(fig)

# --- Tabular data:
def highlight_above_benchmark(s):
    is_above_benchmark = s.str.contains('Bad')
    return ['background-color: #e87b0e; color:white' if v else '' for v in is_above_benchmark]

ssi_ca = ssi_ca.sort_values(by=['SSI_ratio', 'Hospital_Type'], ascending=[False, False])
ssi_ca = ssi_ca.drop('Procedure_Category', axis=1)
ssi_ca = ssi_ca.style.apply(highlight_above_benchmark, subset=['Performance'], axis=1)

st.dataframe(ssi_ca, hide_index=True, use_container_width=True)

st.markdown("""Created by **Vinícius Oviedo** | 
            [Linkedin](https://linkedin.com/in/vinicius-oviedo) | 
            [GitHub](https://github.com/OviedoVR) |
            [WebSite](https://oviedovr.github.io/DataAndLaTeX/)
            """)