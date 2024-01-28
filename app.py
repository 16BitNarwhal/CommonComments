import streamlit as st
import cohere
import os
from dotenv import load_dotenv
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import random

# setup
load_dotenv(dotenv_path='.env')
co = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))

if st.button('Preprocess Data'):
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
  df['cluster'] = df['cluster'].astype(str)

  st.session_state['df'] = df

if 'df' in st.session_state:
  df = st.session_state['df']

  # multiselect widget
  selected_clusters = st.multiselect('Select Clusters to Display', 
                                    options=df['cluster'].unique(),
                                    default=df['cluster'].unique())

  # filter dataframe
  df = df[df['cluster'].isin(selected_clusters)]

  # generate random colors
  num_clusters = df['cluster'].nunique()
  colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for i in range(num_clusters)]
  color_map = {i: colors[i] for i in range(num_clusters)}

  # plot the clusters with colors across different pairs of dimensions
  import plotly.express as px
  fig = px.scatter(df, x='x', y='y', hover_data=['comments'], 
                  color='cluster', color_discrete_map=color_map)
  st.title('Comments Clustering')
  st.plotly_chart(fig)
