import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds
from scipy.sparse import csc_matrix

users=pd.read_json("data/customers.json")
users.columns = ["user_id",'username']

products=pd.read_json("data/products.json")
products.columns = ["product_id","product_name","price"]

ratings=pd.read_json("data/ratings.json")
ratings.drop("CreateDate",inplace = True, axis=1)
ratings.columns = ["user_id","product_id","rating"]
ratings = ratings.drop_duplicates(['user_id', 'product_id'])

pivot_ratings = ratings.pivot(index='user_id', columns='product_id',values='rating')
# Process NaN values
avg_ratings = pivot_ratings.mean(axis = 1)
# User's pivot
user_ratings_centered  = pivot_ratings.sub(avg_ratings, axis=0)
user_ratings_centered.fillna(0, inplace = True)

user_ratings_centered_sparse = csc_matrix(user_ratings_centered)
# Decompose the matrix
U, sigma, Vt = svds(user_ratings_centered_sparse)
sigma = np.diag(sigma)
recalculated_ratings = np.dot(np.dot(U,sigma), Vt)
recalculated_ratings = recalculated_ratings + avg_ratings.values.reshape(-1,1)

pred_SVC = pd.DataFrame(recalculated_ratings, 
                        index=pivot_ratings.index,
                        columns=pivot_ratings.columns)
print(1)
def recommend(user_id):
    recommend_products = []
    user_ratings = pred_SVC.loc[user_id,:].sort_values(ascending=False)
    products_idxs = user_ratings.index.tolist()
    for idx in products_idxs:
        product = products[products["product_id"] == idx]
        product= {
            "product_id": product["product_id"].values[0], 
            "product_name": product["product_name"].values[0],
            "price": product["price"].values[0]
        }
        recommend_products.append(product)

    user = users[users['user_id'] == user_id]
    userName = user['username'].values[0]
    userId = user["user_id"].values[0]
    print("User id: {} Username: {} /n".format(userId, userName))
    print(recommend_products[:10])
    return recommend_products

recommend(10)