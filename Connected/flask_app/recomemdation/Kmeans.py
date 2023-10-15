import json
import pandas as pd
import pickle

path_user = r'C:\Users\ASUS\Downloads\Shecodes\Connected\flask_app\AI\data\customers.json'
path_products = r'C:\Users\ASUS\Downloads\Shecodes\Connected\flask_app\AI\data\products.json'
path_ratings = r'C:\Users\ASUS\Downloads\Shecodes\Connected\flask_app\AI\data\ratings.json'

users = pd.read_json(path_user)
users.columns = ["user_id",'username']
#print(users)

products=pd.read_json(path_products)
products.columns = ["product_id","product_name","price"]
#print(products)


ratings=pd.read_json(path_ratings)
ratings.drop("CreateDate",inplace = True, axis=1)
ratings.columns = ["user_id","product_id","rating"]
#print(ratings)


ratings =  pd.merge(ratings, products, on='product_id',how="outer")

ratings = ratings.drop_duplicates(['user_id', 'product_id'])


#non per recomaendation

product_popularity = ratings["product_id"].value_counts()
#print(product_popularity)

average_rating_df = ratings[["product_id", "rating"]].groupby('product_id').mean()
sorted_average_ratings = average_rating_df.sort_values(by="rating", ascending=False)
#print(sorted_average_ratings)


product_popularity = ratings["product_id"].value_counts()
popular_product = product_popularity[product_popularity > 150].index
#print(popular_product)

popular_product_ranking = ratings[ratings["product_id"].isin(popular_product)]
#print(popular_product_ranking)


popular_average_rating_df = popular_product_ranking[["product_id","rating"]].groupby("product_id").mean()
sorted_popular_average_rating_df = popular_average_rating_df.sort_values(by="rating",ascending=False).head()
#print(sorted_popular_average_rating_df)

#non per sug

users = pd.merge(users, ratings, on='user_id',how="outer")
from itertools import permutations
def create_pairs(x):
    pairs = pd.DataFrame(list(permutations(x.values, 2)), columns=["product_1","product_2"])
    return pairs

product_pairs = users.groupby("user_id")["product_id"].apply(create_pairs)
#print(product_pairs.head())


product_pairs = product_pairs.reset_index(drop=True)
#print(product_pairs)

pairs_counts = product_pairs.groupby(["product_1","product_2"]).size()
#print(pairs_counts.head())

pairs_counts = pairs_counts.reset_index(name='size')

import matplotlib.pyplot as plt

pairs_counts.sort_values('size',ascending=False, inplace=True)
recommend_product = pairs_counts[pairs_counts["product_1"] == 46.0][0:10]

recommend_product.plot.bar(x="product_2",y="size")
#plt.show()

# collab


ratings.drop(['price','product_name'],axis=1,inplace=True)
pivot_users_ratings = ratings.pivot(index='user_id', columns='product_id',values='rating')

avg_ratings = pivot_users_ratings.mean(axis = 1)
pivot_users_ratings  = pivot_users_ratings.sub(avg_ratings, axis=0)
pivot_users_ratings = pivot_users_ratings.fillna(0)

pivot_products_ratings = pivot_users_ratings.T
pivot_products_ratings

from sklearn.metrics.pairwise import cosine_similarity

products_similarities = cosine_similarity(pivot_products_ratings)
products_similarities_df = pd.DataFrame(products_similarities, index = pivot_products_ratings.index, columns = pivot_products_ratings.index)


for p in products.values[0:10]:
    productId=p[0]
    productName=p[1]
    result = products_similarities_df.loc[productId]
    order_result = result.sort_values(ascending=False)[:10]
    print("\t Recommend Product [", productName, "]")
    # print( order_result)

similarities = cosine_similarity(pivot_users_ratings)
users_similarities_df = pd.DataFrame(similarities, index = pivot_users_ratings.index, columns = pivot_users_ratings.index)
users_similarities_df


user = users_similarities_df.loc[3]
order_similarities = user.sort_values(ascending = False)
nearest_neighbor = order_similarities[0:10].index
print(nearest_neighbor)

#Make a copy or else I will have to go up and down stairs waiting it run =))
null_pivot_users_ratings = ratings.pivot(index='user_id', columns='product_id',values='rating')
neighbor_ratings = null_pivot_users_ratings.reindex(nearest_neighbor)

copy_pivot_users_ratings = pivot_users_ratings.copy()


# Drop the product we want to predict
copy_pivot_users_ratings.drop(683, axis=1,inplace=True)
#Seperate our user 3
target_user_x = copy_pivot_users_ratings.loc[[3]]
# print(target_user_x)

other_users_y = null_pivot_users_ratings[683]
# print(other_users_y)

other_users_x = copy_pivot_users_ratings[other_users_y.notnull()]
# print(other_users_x)

other_users_y.dropna(inplace = True)
# print(other_users_y)

from sklearn.neighbors import KNeighborsRegressor
user_knn = KNeighborsRegressor(metric='cosine', n_neighbors = 10)
user_knn.fit(other_users_x, other_users_y)
lm = user_user_pred = user_knn.predict(target_user_x)


print(user_user_pred)

path = r'C:\Users\ASUS\Downloads\Shecodes\Connected\flask_app\AI\train_model.sav'

f = open(path, 'wb')
pickle.dump(lm, f)
f.close()