import streamlit as st
# import cohere
# import os
# from dotenv import load_dotenv
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import pandas as pd
import numpy as np
import random

# setup
# load_dotenv(dotenv_path='.env')
# co = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))

# preprocess options
col1, col2, col3 = st.columns(3)
with col1:
  num_clusters = st.number_input('Number of Clusters', min_value=1, max_value=20, value=10)
with col2:
  random_state = st.number_input('Random State', min_value=0, max_value=100, value=42)
with col3:
  st.markdown("<style>div.row-widget.stButton > div{margin-bottom: 0px;}</style>", unsafe_allow_html=True)
  preprocess_button = st.button('Preprocess Data')
  
if preprocess_button:
  # read data
  df = pd.read_csv('comments.csv')

  # preprocess
  df = df.dropna()
  df['comments'] = df['comments'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
  comments = df['comments'].tolist()

  # # embeddings
  # response = co.embed(
  #   texts=comments,
  #   model='embed-english-v3.0',
  #   input_type='clustering'
  # )
  # embeddings = pd.DataFrame(response)
  # X = np.array(embeddings)
  
  # load embeddings
  embeddings = pd.read_csv('embed.csv')
  X = np.array(embeddings)

  df[['x', 'y']] = X[:, :2]  # assume first two dimensions

  # cluster
  cluster = KMeans(n_clusters=num_clusters, random_state=random_state).fit(X)
  df['cluster'] = cluster.labels_
  df['cluster'] = df['cluster'].astype(str)

  # summarize each cluster
  closest, _ = pairwise_distances_argmin_min(cluster.cluster_centers_, X)
  densest_cluster = closest[np.bincount(cluster.labels_).argmax()]
  
  representatives = []

  st.title('Representative Comment by Cluster')
  for i, center in enumerate(cluster.cluster_centers_):
    # match cluster to comments
    closest, _ = pairwise_distances_argmin_min([center], X)
    c = df['comments'].iloc[closest]
    representatives.append(c.values[0])

  # save to session state
  st.session_state['df'] = df
  st.session_state['selected_clusters'] = set(df['cluster'].unique())
  st.session_state['representatives'] = representatives

  # generate colors
  num_clusters = df['cluster'].nunique()
  colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for i in range(num_clusters)]
  color_map = {i: colors[i] for i in range(num_clusters)}
  st.session_state['colors'] = color_map

if 'df' in st.session_state and 'selected_clusters' in st.session_state \
    and 'colors' in st.session_state:
  df = st.session_state['df']
  df = df.sort_values(by='cluster')
  color_map = st.session_state['colors']

  # sidebar for cluster selection
  st.sidebar.title('Select Clusters (Graph)')
  unique_clusters = sorted(df['cluster'].unique())
  for cluster in unique_clusters:
    on = st.sidebar.toggle(f"Cluster {cluster}", cluster in st.session_state['selected_clusters'])

    if on and cluster not in st.session_state['selected_clusters']:
      st.session_state['selected_clusters'].add(cluster)
    elif not on and cluster in st.session_state['selected_clusters']:
      st.session_state['selected_clusters'].remove(cluster)

  selected_clusters = st.session_state['selected_clusters']
  
  # filter dataframe
  df = df[df['cluster'].isin(selected_clusters)]

  import plotly.express as px

  # plot pie chart containing number of comments per cluster
  fig = px.pie(df, names='cluster', title='Comments per Cluster')
  st.title('Comments per Cluster')
  st.plotly_chart(fig)

  # plot the clusters with colors across different pairs of dimensions
  fig = px.scatter(df, x='x', y='y', hover_data=['comments'], 
                  color='cluster', color_discrete_map=color_map)
  st.title('Comments Clustering')
  st.plotly_chart(fig)

  # sidebar for cluster selection
  st.sidebar.title('Select Cluster (List)')
  unique_clusters = sorted(df['cluster'].unique())
  selected_cluster = st.sidebar.selectbox('View Cluster List', unique_clusters)

  # representative comment
  st.title(f"Representative Comment for Cluster {selected_cluster}")
  representative = st.session_state['representatives'][int(selected_cluster)]
  st.info(representative)

  # Main area for displaying comments
  st.title(f"Comments for Cluster {selected_cluster}")
  cluster_comments = df[df['cluster'] == selected_cluster]['comments'].tolist()
  for comment in cluster_comments:
    st.info(comment)