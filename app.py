import streamlit as st
import cohere
import os
from dotenv import load_dotenv
from sklearn.cluster import KMeans, DBSCAN, AffinityPropagation
import matplotlib.pyplot as plt
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

# cluster
cluster = KMeans(n_clusters=10, random_state=0).fit(X)
# cluster = DBSCAN(eps=0.5, min_samples=5).fit(X)
# cluster = AffinityPropagation(random_state=42)
cluster_labels = cluster.fit_predict(X)
df['cluster'] = cluster_labels

# # plot the clusters with colors across different pairs of dimensions
# from itertools import combinations

fig, ax = plt.subplots(figsize=(10, 10))
ax.scatter(X[:, 0], X[:, 1], c=cluster_labels, cmap='tab10')
ax.set_xlabel('Dimension {}'.format(1))
ax.set_ylabel('Dimension {}'.format(2))
ax.set_title('Scatter Plot of X')

st.pyplot(fig)