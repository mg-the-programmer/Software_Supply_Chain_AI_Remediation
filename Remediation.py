import streamlit as st
from openai import OpenAI as openai
import PyPDF2
from dotenv import load_dotenv
import json
import os 


load_dotenv()

client=openai()

query_responses = []

json_file_path = os.path.abspath("../../json files/data.json")


st.set_page_config(page_title="Trivy Remediation", page_icon="📈",layout="wide")

st.markdown("""
<nav class="custom-navbar">
    <a href="/">
        <img src="data:image/png;base64,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" class="imgCon" alt="Logo" >    
    </a>
    <div class="navContainer">
        <button class="btn">About Product</button>
        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
        </svg>
    </div>
</nav>
""", unsafe_allow_html=True)

with open('./ptc_style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


triple_quote = ''' 
The Policy Validator automates the comparison of Rego code against user-provided policy documents to ensure compliance and correct enforcement. It streamlines policy validation, enhancing security and governance by identifying discrepancies and non-adherence efficiently.'''


st.title("Trivy Remediation")

uploaded_file = st.file_uploader("Upload a JSON Trivy file", type=["json"])
    
if uploaded_file:
    file_contents = uploaded_file.read()

    try:
        data = json.loads(file_contents)
        # st.write("JSON data:")
        # st.write(data)
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid JSON file.")
    
    # trivy_data = 
    def fetch_information(results):
      fetched_data = []
      for result in results:
          vulnerabilities = result.get("Vulnerabilities")
          target = result.get("Target")
          class_type = result.get("Class")
          type_pom = result.get("Type")
          for vulnerability in vulnerabilities:
            pkg_name = vulnerability.get("PkgName")
            installed_version = vulnerability.get("InstalledVersion")
            required_version = vulnerability.get("FixedVersion")
            title = vulnerability.get("Title")
            description = vulnerability.get("Description")
            vulnerability_id = vulnerability.get("VulnerabilityID")
            fetched_data.append({
                "Pkg Name": pkg_name,
                "Installed Version": installed_version,
                "Required Version": required_version,
                "Title": title,
                "Description": description,
                "VulnerabilityID": vulnerability_id,
                "Target": target,
                "Class": class_type,
                "Type": type_pom
            })
      return fetched_data

    fetched_data = fetch_information(data["Results"])
    print(fetched_data)

    for item in fetched_data:
        target = item.get("Target")
        required_version = item.get("Required Version")

    query = f''' As an Developer, that reads the {fetched_data} and for the vulnerabilites you need to give the fixed version that is replaced in the dependency files to fix the vulnerabilities. 
    1 - With the Type, Target and PKG name with these find which languages it is and use the `required version` in the output.
    2 - You job mainly will be installing the required version for that give content to replace it in the dependency files or package management files eg - requirement.txt or package.json. 
    3 - Remember give package installation suggesstion for all the items in the one list it will easy for the user to copy paste the updated version the targeted file package installer file. 
    4 - If the package language is python suggest the things to be changed in the requirement.txt with the fixed version, so that multiple package can be installed with a single command. Don't give code suggestion to create requirement.txt just give the requirement contents to copy paste.
    5 - Always what ever the language it is try to give a single fix. Like For Example if it is react we use package.json for the fixed version keep all the package in one single fix and give the output. 
    6 - Always recommend how to rewrite the target file to upgrade the package. In the Fetched data `target file` location will be there give instruction to how to install in that particular directory. For example App/requirement.txt will have some upgrades and some requirement.txt will have some upgrades. So Accroding to the target file group them one by one. 
    7 - Sometimes the installing the fixed version will cause conflict, because transtive dependencies give warning that if it cause any conflict how to upgrade the package just give the upgrade cmd template because you don't know which package it is conflicting. REMEMBER there will be multiple required version will be there in that always always chose the latest among those

    Desired format: 

    Steps to reinstall the packages : ```

    If there is multiple target location founded, Use this formatting, 
        Location 1 : Things to replace in the location & how to install it
        Location 2 : Things to replace in the location & how to install it

    If there is only one Target location founded, use this formatting:
        Location : Things to replace in the location & how to install it
        
    ```
    '''

    query1 = f''' Your task is to perform the following actions: 
     1 - Read the following text <{fetched_data}>
     2 - Group the vulnerbility fix by the target location mentioned. 
     3 - For each vulnerability group, there will be multiple fix version will be there take the lastest one and give instruction on how to install package for the particular language package for example for python there will be requirement.txt in the what are the things i need to copy paste and how to run it give that type of instruction. After that this particular version might after the other package give instruction on how to update the dependecies package.

     Use the following format: 
        Location : <Target Location>
        Instruction to fix : <Vulnerbility Fix>
    
       '''
    
    openai_response = client.chat.completions.create(  # Use the chat endpoint
    model="gpt-4",  
    messages=[
        {
            "role": "system",
            "content":query,
        }
        ]
    )
    openai_output = openai_response.choices[0].message.content
        
    query_responses.append((query,openai_output))
    # print(query_responses)
    
    st.write(openai_output)
    