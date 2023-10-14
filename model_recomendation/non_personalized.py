import numpy as np
import pandas as pd

users=pd.read_json("data/customers.json")
users.columns = ["user_id",'username']

products=pd.read_json("data/products.json")
products.columns = ["product_id","product_name","price"]

ratings=pd.read_json("data/ratings.json")
ratings.drop("CreateDate",inplace = True, axis=1)
ratings.columns = ["user_id","product_id","rating"]

ratings =  pd.merge(ratings, products, on='product_id',how="outer")
ratings = ratings.drop_duplicates(['user_id', 'product_id'])

# Create a list of only products appearing > 150 times in the dataset
product_popularity = ratings["product_id"].value_counts()
popular_product = product_popularity[product_popularity > 150].index

popular_product_ranking = ratings[ratings["product_id"].isin(popular_product)]
popular_average_rating_df = popular_product_ranking[["product_id","rating"]].groupby("product_id").mean()
sorted_popular_average_rating_df = popular_average_rating_df.sort_values(by="rating",ascending=False)

def predict():
    recommend_products = []
    for idx in sorted_popular_average_rating_df.index:
        product = products[products["product_id"] == idx]
        product= {
            "product_id": product["product_id"].values[0], 
            "product_name": product["product_name"].values[0],
            "price": product["price"].values[0]
        }
        recommend_products.append(product)
        print(recommend_products[:10])
        return recommend_products
    
predict()