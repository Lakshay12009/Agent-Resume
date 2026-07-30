#======LOAD MODULES========
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np


# to show web-app : complete page layout 
st.set_page_config(layout="wide")

# to give title 
st.title("AI RESUME GENERATOR ")
st.write("""This app helps user to  build customized professional 
resume with latest jobs apply links""")

st.image("bg.png")

st.sidebar.title("Fill Important Details")
st.sidebar.image("bg.png")


#======API KEYS========
TAVILY_API_KEY = st.sidebar.text_input("Tavily-API",type = "password") 
GOOGLE_API_KEY = st.sidebar.text_input("Gemini-API",type = "password")
GROQ_API_KEY = st.sidebar.text_input("Groq-API",type = "password")

all_API = [TAVILY_API_KEY, GOOGLE_API_KEY,GROQ_API_KEY]

if not all(all_API):
    st.error("Must give API keys")
    st.stop()
elif all(all_API):
    st.success("API kEYS LOADED SUCEESSFULLY")
else:
    st.info("PASS ALL API KEYS")

# MULTISELECT OPTION 
options = ["Delhi","Banglore",Mumbai","Pune",
                            "Gurugram/Gurgaon"]
loaction  = st.sidebar.multiselect("Select Loaction", options = options)

profile_op = ["Data Analysts","AI Engineer","GEN AI Developer", 
                              "Full-Stack Dev","Data scientist"]

profile = st.sidebar.multiselect("Select job profile ", options =  profile_op)

#============ GET USER INFO============
st.markdown("""### GET USER INFO""")
user_info = st.text_area("""write your resume description:""")

#=========model ========
model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY,
)

# response = model.invoke("HEllo Buddy!")
# response.content[-1]['text']

#=====Tools=====
def search_latest_news_jobs(query):
  """This function helps to fetch latest
  news or jobs related article using tavily"""

  client = TavilyClient(
      api_key = TAVILY_API_KEY
  )
  response = client.search(query)
  return response

#======Agent creation========
agent = create_agent(
    model = model,
    tools = [search_latest_news_jobs]
)
# agent

# ===fetching info with help of def func====
def main_agent (agent, query):
  """This is main agent , or leader agent
  orchestrate aub agents"""

  # Giving prompt to create detailed prompt for code generation
  prompt = """You are AI assistant and below given as a prompt , your task is
  to give detailed prompt for this .
  you are a professional generator where user will give their personal info,
  you have to created a detailed resume for students or professional one , it must
  be with dynamic UI and UX and , with advanced CSS professional designing
  it must be with dynamic UI and UX and, with advanced CSS Professional Designing
  Make sure to give output in HTML format only no markdowns allowed
  """
  response = agent.invoke({'messages': [{'role': 'user',
                                        'content': prompt}]})
  detailed_prompt = response['messages'][-1].content[-1]['text' ]
  # SAVE PROMPT using File Handling
  with open ('prompt. txt', 'w') as f:
    f.write(detailed_prompt)

  user_details = f"""Below Given is a user details
  generate resume based on that , if not given keep : Default Resume:
  python Developer user details: {query}"""

  final_prompt = prompt + detailed_prompt + user_details
  
  # code generation

  response = agent.invoke({'messages': [{'role': 'user',
                                        'content': final_prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code



# display 

# code = main_agent(agent,"LAKSHAY, GEN AI EXPERT")
# from IPython import display as DISPLAY
# DISPLAY.HTML(code)


# Fetch latest Domain related Jobs using tavily

def get_jobs(agent,
             Location = "Noida,Delhi",
             Profile = "data Analysts, AI Engineer"):
  Location = "Noida,DeLhi"
  profile = "Data Analysts, AI Engineer"

  prompt = f"""Based on user given Job profile,
  fetch latest jobs or job apply article using Naukri,
  Linkedin, Indeed, or all popular Job apply platforms,
  Show Results with JOB PROFILE NAME, LOCATION, SALARY,
  COMPANY NAME, SHOW jobs only related to given {Location }
  and {Profile}. Output must be in Professional HTML Naukri
  theme cards with Dynamic Design, Show atleast Top 5-10
  results with direct apply link"""
  response = agent.invoke({'messages': [{'role': 'user',
                                        'content': prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code

# displaying jobs 
# code = get_jobs(agent)
# DISPLAY.HTML(code)

if st.button ("Generate Resume"):
            with st.spinner("Agent Running"):
                code = main_agent(agent,user_info)
                st.html(code , width="stretch",
                        unsafe_allow_javascript=True)
                st.divider() # to give horizontal div
                jobe_code = get_jobs (agent, location, profile)
                st.html (job_code , width="stretch" ,
                         unsafe_allow_javascript=True)
                
                
