import numpy as np
import pandas as pd
from itertools import permutations

users=pd.read_json("data/customers.json")
users.columns = ["user_id",'username']

products=pd.read_json("data/products.json")
products.columns = ["product_id","product_name","price"]

ratings=pd.read_json("data/ratings.json")
ratings.drop("CreateDate",inplace = True, axis=1)
ratings.columns = ["user_id","product_id","rating"]

users = pd.merge(users, ratings, on='user_id',how="outer")
users = users.drop_duplicates(['user_id', 'product_id'])
print(users)

def create_pairs(x):
    pairs = pd.DataFrame(list(permutations(x.values, 2)), columns=["product_1","product_2"])
    return pairs

product_pairs = users.groupby("user_id")["product_id"].apply(create_pairs)
product_pairs = product_pairs.reset_index(drop=True)
pairs_counts = product_pairs.groupby(["product_1","product_2"]).size()
pairs_counts = pairs_counts.reset_index(name='size')
pairs_counts.sort_values('size',ascending=False, inplace=True)
print(pairs_counts)

#remember to turn product_clicked_id into integer
def recommend(product_clicked_id):
    recommend_products = []
    recommend_product = pairs_counts[pairs_counts["product_1"] == product_clicked_id]
    products_idxs = recommend_product["product_2"].astype(int).values.tolist()
    for idx in products_idxs:
        product = products[products["product_id"] == idx]
        product= {
            "product_id": product["product_id"].values[0], 
            "product_name": product["product_name"].values[0],
            "price": product["price"].values[0]
        }
        recommend_products.append(product)
    print(recommend_products)
    return recommend_products

recommend(2)