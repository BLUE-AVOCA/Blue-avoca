import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import KNeighborsRegressor


path_user = r'C:\Users\ASUS\Downloads\Shecodes\Connected\flask_app\recomemdation\data\customers.json'
path_products = r'C:\Users\ASUS\Downloads\Shecodes\Connected\flask_app\recomemdation\data\products.json'
path_ratings = r'C:\Users\ASUS\Downloads\Shecodes\Connected\flask_app\recomemdation\data\ratings.json'




users=pd.read_json(path_user)
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

# Find the similarities between products
products_similarities = cosine_similarity(pivot_products_ratings)
products_similarities_df = pd.DataFrame(products_similarities, index = pivot_products_ratings.index, columns = pivot_products_ratings.index)


def recommend(product_id):
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
    print(recommend_products)
    return recommend_products

filename = 'trained_model.sav'
f = open(filename,'wb')
pickle.dump(products_similarities,f)
f.close()
#Turn to our users-------------------------------------------
# users_similarities = cosine_similarity(pivot_users_ratings)
# users_similarities_df = pd.DataFrame(users_similarities, index = pivot_users_ratings.index, columns = pivot_users_ratings.index)

# def KNN(user_id, product_id_want_to_pred):
#     user = users_similarities_df.loc[user_id]
#     order_user_similarities = user.sort_values(ascending = False)
#     nearest_neighbor = order_user_similarities[0:10].index #can use order_user_similarities[0:10] to limit alike users
#     neighbor_ratings = pivot_ratings.reindex(nearest_neighbor)

#     print("His neighbor rating is: {}".format(neighbor_ratings[product_id_want_to_pred].mean()))
#     copy_pivot_users_ratings = pivot_users_ratings.copy()
#     # Drop the product we want to predict
#     copy_pivot_users_ratings.drop(product_id_want_to_pred, axis=1,inplace=True)
#     #Separate our user 
#     target_user_x = copy_pivot_users_ratings.loc[[user_id]]
#     other_users_y = pivot_ratings[product_id_want_to_pred]
#     #We only care about the users who have retailed the products
#     other_users_x = copy_pivot_users_ratings[other_users_y.notnull()]
#     #Now drop NaN values
#     other_users_y.dropna(inplace = True)

#     #Time for the show
#     user_knn = KNeighborsRegressor(metric='cosine', n_neighbors = 10) #model
#     user_knn.fit(other_users_x, other_users_y)
#     user_user_pred = user_knn.predict(target_user_x)

#     filename = 'trained_model.sav'
#     f = open(filename, 'wb')
#     pickle.dump(user_knn,f)
#     f.close

#     print("His predicted KNN rating is: {}".format(user_user_pred[0]))
#     return user_user_pred



