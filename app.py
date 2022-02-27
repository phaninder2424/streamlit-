from ast import increment_lineno
import streamlit as st
import pandas as pd 
import numpy as np
from textblob import TextBlob
import seaborn as sns
import textblob

encoding='utf8'


def explore(df_reviews):
  
  st.write('Data:')
  st.pyplot(sns.displot(df_reviews['Star']))
  st.pyplot(sns.countplot(x='Star',data=df_reviews).figure)
  textblob_object=TextBlob(df_reviews['Text'][1])
  st.write(textblob_object.sentiment)
  st.write('Polarity is float which lies in the range of [-1,1] where 1 means positive statement and -1 means a negative statement. Subjective sentences generally refer to personal opinion, emotion or judgment whereas objective refers to factual information. Subjectivity is also a float which lies in the range of [0,1].')
  
  polarity=[]
  subjectivity=[]
  for i in df_reviews['Text'].values:
      try:
          analysis=TextBlob(i)
          polarity.append(analysis.sentiment.polarity)
          subjectivity.append(analysis.sentiment.subjectivity)
      except:
          polarity.append(0)
          subjectivity.append(0)
  df_reviews['polarity']=polarity
  df_reviews['subjectivity']=subjectivity
  st.write(df_reviews)
          
  
  
  p=df_reviews['positive/negative']=np.where(df_reviews['polarity']>=0.05,True,False)
  st.write(df_reviews)
  k=df_reviews.loc[p]
  k = k[(k['Star']<3) ]
  st.write(k)
  st.pyplot(sns.barplot(x='Star',y='polarity',data=k).figure)
  st.write('These users are to be suggested to change their stars as their reviews are good')
  
  
def transform(df):
  # Select sample size
  frac = st.slider('Random sample (%)', 1, 100, 100)
  if frac < 100:
    df = df.sample(frac=frac/100)
  # Select columns
  cols = st.multiselect('Columns', 
                        df.columns.tolist(),
                        df.columns.tolist())
  df = df[cols]
  st.write(df)
  st.write('sentiment analysis begins')

  return df

def get_df(file):
  # get extension and read file
  extension = file.name.split('.')[1]
  if extension.upper() == 'CSV':
    df = pd.read_csv(file)
  elif extension.upper() == 'XLSX':
    df = pd.read_excel(file, engine='openpyxl')
  elif extension.upper() == 'PICKLE':
    df = pd.read_pickle(file)
  return df
def main():
  names = ['evaluator']
  usernames = ['eval']
  passwords = ['123']

  hashed_passwords = stauth.hasher(passwords).generate()
  authenticator = stauth.authenticate(names,usernames,hashed_passwords,'cookie_name', 'signature_key',cookie_expiry_days=30)
  name, authentication_status = authenticator.login('Login','sidebar')

  if authentication_status:
   st.write('Welcome *%s*' % (name))
  elif authentication_status == False:
    st.error('Username/password is incorrect')
  elif authentication_status == None:
     st.warning('Please enter your username and password')
     
  st.title('Explore a dataset')
  st.write('A general purpose data exploration app')
  file = st.file_uploader("Upload file", type=['csv'])
  if not file:
    st.write("Upload a .csv or .xlsx file to get started")
    return
  df = get_df(file)
  df_reviews = transform(df)
  
  explore(df_reviews)
main()
