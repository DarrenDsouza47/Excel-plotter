import streamlit as st
import pandas as pd
from pandasai import SmartDataframe,Agent
from pandasai.llm import BambooLLM
from pandasai.responses.streamlit_response import StreamlitResponse
import os,glob
from pandasai.ee.agents.judge_agent import JudgeAgent
from excel_storage import excel_storage
pwd=os.getcwd()


llm=BambooLLM(api_key="$2a$10$8r2QLC5WyQe1UdXlSoegKOxxS/Fnwpiwg4OGmULgCfZ9RHHMduYpa")
st.title("Chat with excel file")
file=st.file_uploader("upload your file")

if file:
    df=pd.read_csv(file)
    agent=Agent(df,config={"llm":llm,"response_parser":StreamlitResponse,"save_charts":True,"save_charts_path":pwd})
    options=['chat','plot']

    selected_option=st.selectbox("choose an option",options)

    if selected_option=="chat":
        query=st.text_input("enter your query")
        if query:
            response=agent.chat(query)
            st.write(response)

    if selected_option=="plot":
        query=st.text_input("enter your query",key="plot")
        if query:
            btn=st.button("submit")
            file=glob.glob(pwd+"/*.png")
            if file:
                os.remove(file[0])
            if btn:
                response=agent.chat(query,output_type="plot")
                code=agent.last_code_executed
                file=glob.glob(pwd+"/*.png")
                if file:
                    st.image(image=file[0],caption="plot for :"+ query,width=1024) 
                st.write(code)
                excel_storage(code,df)
            
            
            
            
        