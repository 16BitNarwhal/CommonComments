import streamlit as st
import cohere
import os
from dotenv import load_dotenv
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

# setup
load_dotenv(dotenv_path='.env')
co = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))

# read data
df = pd.read_csv('comments.csv')

# preprocess
df = df.dropna()
df['comments'] = df['comments'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
comments = df['comments'].tolist()

# embeddings
response = co.embed(
  texts=comments,
  model='embed-english-v3.0',
  input_type='clustering'
)
embeddings = pd.DataFrame(response)
X = np.array(embeddings)

df[['x', 'y']] = X[:, :2]  # Assuming you're using the first two dimensions

# cluster
cluster = KMeans(n_clusters=10, random_state=0).fit(X)
df['cluster'] = cluster.labels_

# plot the clusters with colors across different pairs of dimensions
import plotly.express as px
fig = px.scatter(df, x='x', y='y', hover_data=['comments'], color='cluster')
st.title('Comments Clustering')
st.plotly_chart(fig)
