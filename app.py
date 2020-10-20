import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from io import BytesIO

fp = st.sidebar.file_uploader("Upload the data here:") 

df = st.cache(pd.read_csv)(fp)




# df = st.cache(pd.read_csv)("fake_data.csv")
is_check = st.checkbox("Display Data")
if is_check:
    st.write(df)


st.sidebar.title("Filter data")

#Checkbox for Hospitals
Filter = st.sidebar.selectbox("Select Query", ["Event ID","Collaborator Cohort","Date of uploads"])
print(Filter)
if Filter=="Event ID":
    dff=df["Event ID"].value_counts()
    fig = px.pie(df, values=dff.values, names=dff.index,title='Event ID %')
    st.plotly_chart(fig)



    rslt_df1 = df.loc[(df['Event ID'] == 1)]
    data1=rslt_df1["Question from suggestion"].value_counts()


    rslt_df2 = df.loc[(df['Event ID'] == 2)]
    data2=rslt_df2["Question from suggestion"].value_counts()

    rslt_df3 = df.loc[(df['Event ID'] == 3)]
    data3=rslt_df3["Question from suggestion"].value_counts()

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=data1.index,
                    y=data1.values,
                    name='1',
                    marker_color='rgb(55, 83, 109)'
                    ))
    fig2.add_trace(go.Bar(x=data2.index,
                    y=data2.values,
                    name='2',
                    marker_color='rgb(26, 118, 255)'
                    ))
    fig2.add_trace(go.Bar(x=data3.index,
                    y=data3.values,
                    name='3',
                    marker_color='rgb(165,0,38)'
                    ))

    fig2.update_layout(
        title='Event ID - No of Question from suggestion',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Question Count',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=1,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1 
    )
    st.plotly_chart(fig2)

elif Filter=="Collaborator Cohort":
    fig3 = px.histogram(df, x="Collaborator Cohort",title='Collaborator Cohort')
    st.plotly_chart(fig3)

elif Filter=="Date of uploads":
    fig4 = px.line(df, x=range(1,df.shape[0]+1),y="Date",title='Overview of all the submission:')
    st.plotly_chart(fig4)



    fig5 = px.line(df, x='Date',y="Event ID",title='Date of upload and Event Id')
    st.plotly_chart(fig5)


    time1 = df.loc[(df['Event ID'] == 1)]
    fig6 = px.line(time1, x=range(1,time1.shape[0]+1),y="Date",title="Event ID 1 submission Dates")
    st.plotly_chart(fig6)

    time2 = df.loc[(df['Event ID'] == 2)]
    fig7 = px.line(time2, x=range(1,time2.shape[0]+1),y="Date",title="Event ID 2 submission Dates")
    st.plotly_chart(fig7)

    time3 = df.loc[(df['Event ID'] == 3)]
    fig8 = px.line(time3, x=range(1,time3.shape[0]+1),y="Date",title="Event ID 3 submission Dates")
    st.plotly_chart(fig8)




def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download csv file</a>'

st.sidebar.markdown(get_table_download_link(df), unsafe_allow_html=True)