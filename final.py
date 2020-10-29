import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from io import BytesIO
from PIL import Image
import os
import base64
import requests 
import plotly.graph_objects as go
from plotly.subplots import make_subplots


import urllib
import json                 
from pprint import pprint 


st.sidebar.title("Enter Username and password:")
username=st.sidebar.text_area("Please Enter Username: ",height=1)
password=st.sidebar.text_area("Please Enter Password: ",height=1)


@st.cache(persist=True,suppress_st_warning=True)
def login(username,password):

        if username=="AdminRT" and password=="AdminRT123":
            return True
            
        else:
            st.write("Wrong Credentials")
            return False
            



if st.sidebar.checkbox("Login"):
    if username=="1" and password=="1":
        Collab_Media_id=[]
        Event_id=[]
        Event_name=[]
        Collaborator_Name=[]
        Collaborator_Phone=[]
        Media_file=[]
        Question_chosen_from_suggestion=[]
        Date=[]
        Time=[]
        Download_link=[]
        Collaborator_Cohort=[]  


        for j in range(266,269):
            counter1=1
            temp1=0
            while(temp1 != None):
                url = f"https://api.miljulapp.com/api/v1/api/v1/collab/collabmedia?collab_event={j}&page={counter1}"
                response = urllib.request.urlopen(url)
                text = response.read()
                json_data = json.loads(text)

                temp1=json_data["response"]["response"]["next"]
                print(temp1,j)
                counter1+=1

                c=json_data["response"]["response"]["results"]
                for i in range(0,len(c)):
                    Collab_Media_id.append(c[i]["id"])
                    Event_id.append(c[i]["collab_event"])
                    Event_name.append(c[i]["get_collab_event"]["name"])
                    Collaborator_Name.append(c[i]["get_event_collaborator"]["name"])
                    Collaborator_Phone.append(c[i]["get_event_collaborator"]["mobile"])


                    try:
                        temp=c[i]["media_url"]
                        print(temp)
                        z=temp[-21:]
                        Media_file.append(z)
                    except:
                        Media_file.append("None")

                    try:
                        Question_chosen_from_suggestion.append(c[i]["meta_data"]["questionSelected"])
                    except:
                        Question_chosen_from_suggestion.append("None")




                    Date.append(c[i]["created"][0:10])
                    Time.append(c[i]["created"][11:16])

                    Download_link.append(c[i]["media_url"])

                    try:
                        Collaborator_Cohort.append(c[i]["get_event_collaborator"]["meta_data"]["cohort"])
                    except:
                        Collaborator_Cohort.append("None")





        data = {"Collab_Media_id":Collab_Media_id,
                "Event_id":Event_id,
                "Event_name":Event_name,
                "Collaborator_Name":Collaborator_Name,
                "Collaborator_Phone":Collaborator_Phone,
                "Media_file":Media_file,
                "Question_chosen_from_suggestion":Question_chosen_from_suggestion,
                "Date":Date,
                "Time":Time,
                "Download_link":Download_link,
                "Collaborator_Cohort":Collaborator_Cohort
        }
        column=["Collab_Media_id",
                "Event_id",
                "Event_name",
                "Collaborator_Name",
                "Collaborator_Phone",
                "Media_file",
                "Question_chosen_from_suggestion",
                "Date",
                "Time",
                "Collaborator_Cohort",
                "Download_link"
                ]


        df = pd.DataFrame (data, columns = column)

        df=df.fillna("None")
        df["Collaborator_Phone"]= df["Collaborator_Phone"].replace("", "None") 


        dff=df.copy() 
        # st.dataframe(df)
        #----------------------------------------------------------------------------------------------------------
        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(
                csv.encode()
            ).decode()  # some strings <-> bytes conversions necessary here
            return f'<a href="data:file/csv;base64,{b64}" download="data.csv" style="float: right;">Download csv file</a>'

        st.markdown(get_table_download_link(df), unsafe_allow_html=True)

        #----------------------------------------------------------------------------------------------------------







        # filters = st.sidebar.checkbox("Filter")
        # if filters:
        st.sidebar.title("Filter Columns :")


        options = pd.Series(["All"]).append(df["Event_name"], ignore_index=True).unique()
        choice = st.sidebar.selectbox("Select {}.".format("Event_name."), options)

        if choice != "All":
            dff = dff[dff["Event_name"] == choice]



        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            specs=[[{"type": "table"}],
                    [{"type": "Pie"}]]
        )

        fig.add_trace(
            go.Table(
                header=dict(
                    values=dff.columns,
                    font=dict(size=10),
                    align="left"
                ),
                cells=dict(
                    values=[dff[k].tolist() for k in dff.columns[0:]],
                    align = "left")
            ),
            row=1, col=1
        )
        dd=df["Event_id"].value_counts()
        fig.add_trace(
            go.Pie(labels = dd.index, values = dd.values,title="Event ID %"),
            row=2, col=1
        )
        fig.update_layout(
            height=1000,
            width=1000,
            showlegend=False,
            title_text="Filtered",
        )

        st.plotly_chart(fig)


        Collaborator_Name1=[]
        Collaborator_Phone1=[]
        Date1=[]
        Collaborator_Cohort1=[]  


        for j in range(266,267):
            counter=1
            temp=0
            while(temp != None):
                url=f"https://api.miljulapp.com/api/v1/api/v1/collab/collaborators?collab_event_id={j}&page={counter}"
                response = urllib.request.urlopen(url)
                text = response.read()
                json_data = json.loads(text)
                temp=json_data["response"]["response"]["next"]
                print(temp)
                counter+=1
                c=json_data["response"]["response"]["results"]
                for i in range(0,len(c)):
                    Collaborator_Name1.append(c[i]["name"])

                    Collaborator_Phone1.append(c[i]["mobile"])

                    Date1.append(c[i]["created"][0:16])

                    try:
                        Collaborator_Cohort1.append(c[i]["meta_data"]["cohort"])
                    except:
                        Collaborator_Cohort1.append("None")





            data = {
                    "Collaborator_Name":Collaborator_Name1,
                    "Collaborator_Phone":Collaborator_Phone1,
                    "Date":Date1,
                    "Collaborator_Cohort":Collaborator_Cohort1
            }
            column=[
                    "Collaborator_Name",
                    "Collaborator_Phone",
                    "Date",
                    "Collaborator_Cohort"
                    ]


            data = pd.DataFrame (data, columns = column)

            data=data.fillna("None")
            data["Collaborator_Phone"]= data["Collaborator_Phone"].replace("", "None") 

            data=data.sort_values(by='Date')
            dff1=data.copy()






            # filters = st.sidebar.checkbox("Filter")
            # if filters:
            # st.sidebar.title("Filter Columns :")


            # options = pd.Series(["All"]).append(df["Event_name"], ignore_index=True).unique()
            # choice = st.sidebar.selectbox("Select {}.".format("Event_name."), options)

            # if choice != "All":
            #     dff = dff[dff["Event_name"] == choice]



            fig1 = make_subplots(
                rows=1, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                specs=[[{"type": "table"}]]
            )

            fig1.add_trace(
                go.Table(
                    header=dict(
                        values=dff1.columns,
                        font=dict(size=10),
                        align="left"
                    ),
                    cells=dict(
                        values=[dff1[k].tolist() for k in dff1.columns[0:]],
                        align = "left")
                ),
                row=1, col=1
            )
            fig1.update_layout(
                height=1000,
                width=1000,
                showlegend=False,
                title_text="Event Collaborators Data",
            )

            st.plotly_chart(fig1)

        # st.write(dff["Download_link"].values)

        #----------------------------------------------------------------------------------------------------------

        def download_links(link, file_label='File'):

            href = f'<a href="{link}" download="{os.path.basename("download")}">f{link} {""}</a>'
            return href



        if st.button('Download Images'):
            for i in dff["Download_link"].values:
                print(i)
                if i=="None":
                    pass
                else:

                    image_url = f"{i}"

                st.markdown(download_links(image_url, 'Picture'), unsafe_allow_html=True)


        #----------------------------------------------------------------------------------------------------------

    else:
        st.write("wrong credentials")
