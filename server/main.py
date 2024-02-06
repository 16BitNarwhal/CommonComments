from fastapi import FastAPI
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import random

import typing
import strawberry
from strawberry.asgi import GraphQL

@strawberry.type
class Comment:
    id: int
    text: str
    x: float
    y: float
    cluster: int

@strawberry.type
class Cluster:
    id: int
    x: float
    y: float
    cluster: int

@strawberry.type
class Query:
    @strawberry.field
    def comments(self, clusters: int) -> typing.List[Comment]:
        embeddings = pd.read_csv('embed.csv')
        X = np.array(embeddings)
        df = pd.read_csv('comments.csv')

        df = df.dropna()
        df['comments'] = df['comments'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
        
        df[['x', 'y']] = X[:, :2]
        clusters = KMeans(n_clusters=clusters, random_state=42).fit(X)
        df['cluster'] = clusters.labels_
        df['cluster'] = df['cluster'].astype(str)
        df = df.sort_values(by='cluster')
        return [
            Comment(id=i, text=row['comments'], x=row['x'], y=row['y'], cluster=row['cluster']) for i, row in df.iterrows()
        ]

schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/cluster")
# def read_item(cluster: str):
#     embeddings = pd.read_csv('embed.csv')
#     X = np.array(embeddings)
#     df = pd.read_csv('comments.csv')
#     df[['x', 'y']] = X[:, :2]
#     cluster = KMeans(n_clusters=cluster, random_state=42).fit(X)
#     df['cluster'] = cluster.labels_
#     df['cluster'] = df['cluster'].astype(str)
#     df = df.sort_values(by='cluster')
#     num_clusters = df['cluster'].nunique()
#     colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
#             for i in range(num_clusters)]

#     return df