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

  df[['x', 'y']] = X[:, :2]  # assume first two dimensions

  # cluster
  cluster = KMeans(n_clusters=10, random_state=0).fit(X)
  df['cluster'] = cluster.labels_
  df['cluster'] = df['cluster'].astype(str)

  st.session_state['df'] = df

if 'df' in st.session_state:
  df = st.session_state['df']
  df = df.sort_values(by='cluster')

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

  # display dropdowns for each cluster
  left_column, right_column = st.columns(2)

  # Iterate through each cluster
  unique_clusters = sorted(df['cluster'].unique())
  for cluster in unique_clusters:
    with left_column:
      if st.button(f'Show Cluster {cluster}', key=f'button_{cluster}'):
        cluster_comments = df[df['cluster'] == cluster]['comments'].tolist()

        with right_column:
          st.write(f"Comments for Cluster {cluster}:")
          for comment in cluster_comments:
            st.text(comment)