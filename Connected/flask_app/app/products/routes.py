from app.products import bp
from app.models.test2 import Product
import pandas as pd 
import numpy as np


from scipy.sparse.linalg import svds
from scipy.sparse import csc_matrix

from flask import render_template, request, url_for, redirect
from sklearn.metrics.pairwise import cosine_similarity
import os
from sklearn.neighbors import KNeighborsRegressor



SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
path_user = os.path.join(SITE_ROOT, "data", "customers.json")

path_products = os.path.join(SITE_ROOT, "data", "products.json")
path_ratings = os.path.join(SITE_ROOT, "data", "ratings.json")



users=pd.read_json(path_user)
# users = json.load(open(path_user))
users.columns = ["user_id",'username']


products=pd.read_json(path_products)
products.columns = ["product_id","product_name","price"]

ratings=pd.read_json(path_ratings)
ratings.drop("CreateDate",inplace = True, axis=1)
ratings.columns = ["user_id","product_id","rating"]
ratings = ratings.drop_duplicates(['user_id', 'product_id'])

pivot_ratings = ratings.pivot(index='user_id', columns='product_id',values='rating')
# Process NaN values
avg_ratings = pivot_ratings.mean(axis = 1)
# User's pivot
pivot_users_ratings  = pivot_ratings.sub(avg_ratings, axis=0)
pivot_users_ratings = pivot_users_ratings.fillna(0)
# Product pivot
pivot_products_ratings = pivot_users_ratings.T


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
def recommend_user(user_id):
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

def recommend(product_id):

    # Find the similarities between products
    products_similarities = cosine_similarity(pivot_products_ratings)
    products_similarities_df = pd.DataFrame(products_similarities, index = pivot_products_ratings.index, columns = pivot_products_ratings.index)
    
    recommend_products = []
    recommend_product = products_similarities_df.loc[product_id].sort_values(ascending=False)[1:] # remove the itself at the top :v
    
    products_idxs = recommend_product.index.tolist()
    for idx in products_idxs:
        product = products[products["product_id"] == idx]
        product= {
            "product_id": product["product_id"].values[0], 
            "product_name": product["product_name"].values[0],
            "price": product["price"].values[0]
        }
        recommend_products.append(product)
    return recommend_products

users_similarities = cosine_similarity(pivot_users_ratings)
users_similarities_df = pd.DataFrame(users_similarities, index = pivot_users_ratings.index, columns = pivot_users_ratings.index)



@bp.route('/')
def index():
    products = Product.query.limit(200).all()
    return render_template('products/product_layout.html',products = products)

@bp.route('/search', methods=('GET', 'POST'))
def search():
    search_value = "Please search the items"
    products = []
    if request.method == 'POST':
        search_value = request.form['search_product']
        products = Product.query.filter(Product.product_name.contains(search_value)).all()
        return render_template('products/product_layout.html',products = products )
    return search_value

@bp.route('/find', methods = ('GET', 'POST'))
def recomendation_in_product():
    products = Product.query.all();
    if request.method == 'POST':
        id_product = request.form.get('id_product')
        return redirect(url_for('products.recomendation', id_product = id_product))
    return render_template('products/product_layout.html', products = products)


@bp.route('/recomendation',  methods=['GET', 'POST'])
def recomendation():
    id_product = request.args.get('id_product', None)
    s = id_product.split()
    if (s[0] == None):
        return render_template('products/test_product.html')
    else :  
        output = []
        output = recommend((int(s[0])))
        return render_template('products/recomendation_test.html', id_product = id_product , output = output)
    
@bp.route('/recomendation_user')
def recomendation_user():
    output = recommend_user(3)
    return render_template('products/user_recomendation.html', output = output) 


