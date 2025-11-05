import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_data(dept,designations):
    url = requests.get(f'https://www.{dept}.ruet.ac.bd/teacher_list').text
    soup = BeautifulSoup(url, 'lxml')
    profs = soup.find_all('tr')[1:]

    name = []
    desig = []
    phone = []
    email = []
    dep = []

    for i in profs:
        ds = i.find_all('td')[3].text.strip()       
        if ds in designations:
            nm = i.find_all('td')[1].text.strip()
            em = i.find_all('td')[5].text.strip()
            ph = i.find_all('td')[6].text.strip()
            de = i.find_all('td')[4].text.strip()

            name.append(nm)
            desig.append(ds)
            email.append(em)
            phone.append(ph)
            dep.append(de)

    data = pd.DataFrame({'English Name':name, 'Designation':desig, 'Email':email, 'Phone Number':phone, 'Department':dep})
    return data

def main():
    st.title('RUET Professor Information')
    #department selection
    depts = ['EEE', 'CSE', 'CHEM', 'MATH', 'PHY', 'CHEM']
    dept = st.sidebar.selectbox('Select Department', depts).lower()
    st.sidebar.write('Select Designations')
    desigs= []
    
    if st.sidebar.checkbox('Lecturer'):
        desigs.append('Lecturer')
    if st.sidebar.checkbox('Professor'):
        desigs.append('Professor')
    if st.sidebar.checkbox('Associate Professor'):
        desigs.append('Associate Professor')
    if st.sidebar.checkbox('Assistant Professor'):
        desigs.append('Assistant Professor')

    if dept and desigs:
        data = get_data(dept, desigs)
        st.dataframe(data)

main()