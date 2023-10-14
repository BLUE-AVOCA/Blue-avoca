import numpy as np
import pandas as pd

ratings =pd.read_json("data/ratings.json")
ratings.drop("CreateDate",inplace = True, axis=1)

customers=pd.read_json("data/customers.json")

products=pd.read_json("data/products.json")


class MatrixFactorization(object):
    def __init__(self, Y,customers,products, K, lam = 0.1, Xinit = None, Winit = None, learning_rate = 0.5, max_iter = 1000, print_every = 100):
        self.Y = Y # represents the utility matrix
        self.K = K
        self.lam = lam # regularization parameter
        self.learning_rate = learning_rate # for gradient descent
        self.max_iter = max_iter # maximum number of iterations
        self.print_every = print_every # print loss after each a few iters
        self.customers=customers
        self.products=products
        self.n_users = int(np.max(Y[:, 0])) + 1
        self.n_items = int(np.max(Y[:, 1])) + 1
        #self.n_users = customers.size
        #self.n_items = products.size
        self.n_ratings = Y.shape[0] # number of known ratings
        self.X = np.random.randn(self.n_items, K) if Xinit is None\
        else Xinit
        self.W = np.random.randn(K, self.n_users) if Winit is None\
        else Winit
        self.b = np.random.randn(self.n_items) # item biases
        self.d = np.random.randn(self.n_users) # user biases
    def loss(self):
        L = 0
        for i in range(self.n_ratings):
            # user_id, item_id, rating
            n, m, rating = int(self.Y[i,0]), int(self.Y[i,1]), self.Y[i,2]
            L += 0.5*(self.X[m].dot(self.W[:, n])\
            + self.b[m] + self.d[n] - rating)**2
        L /= self.n_ratings
        # regularization, don’t ever forget this
        return L + 0.5*self.lam*(np.sum(self.X**2) + np.sum(self.W**2))
    def updateXb(self):
        products = np.array(self.products["Id"])
        for m in range(0,products.size):
            pId = products[m]
            # get all users who rated item m and corresponding ratings
            ids = np.where(self.Y[:, 1] == pId)[0] # row indices of items m
            if ids.size>0:
                user_ids, ratings=self.Y[ids, 0].astype(np.int32),self.Y[ids, 2]
                Wm, dm = self.W[:, user_ids], self.d[user_ids]
                for i in range(30): # 30 iteration for each sub problem
                    xm = self.X[m]
                    error = xm.dot(Wm) + self.b[m] + dm - ratings
                    grad_xm = error.dot(Wm.T)/self.n_ratings + self.lam*xm
                    grad_bm = np.sum(error)/self.n_ratings
                    # gradient descent
                    self.X[m] -= self.learning_rate*grad_xm.reshape(-1).astype('float64')
                    self.b[m] -= self.learning_rate*grad_bm
    def updateWd(self): # and d
        customers = np.array(self.customers["Id"])
        for n in range(0,customers.size):
            custId=customers[n]
            # get all items rated by user n, and the corresponding ratings
            ids = np.where(self.Y[:,0] == custId)[0] #indexes of items rated by n
            if ids.size>0:
                item_ids,ratings=self.Y[ids, 1].astype(np.int32), self.Y[ids, 2]
                Xn, bn = self.X[item_ids], self.b[item_ids]
                for i in range(30): # 30 iteration for each sub problem
                    wn = self.W[:, n]
                    error = Xn.dot(wn) + bn + self.d[n] - ratings
                    grad_wn = Xn.T.dot(error)/self.n_ratings + self.lam*wn
                    grad_dn = np.sum(error)/self.n_ratings
                    grad_dn=grad_dn
                    # gradient descent
                    self.W[:, n] -= self.learning_rate*grad_wn.reshape(-1).astype('float64')
                    self.d[n] -= self.learning_rate*grad_dn
    def fit(self):
        for it in range(self.max_iter):
            self.updateWd()
            self.updateXb()
            if (it + 1) % self.print_every == 0:
                rmse_train = self.evaluate_RMSE(self.Y)
                print("iter = %d, loss = %.4f, RMSE train = %.4f"%(it + 1,
                self.loss(), rmse_train))
    def predict(self, u, i):
        """
        predict the rating of user u for item i
        """
        try:
            u, i = int(u), int(i)
            pred = self.X[i, :].dot(self.W[:, u]) + self.b[i] + self.d[u]
            return max(0, min(5, pred))  # 5-scale in Ecommerce
        except:
            return  0        
    def evaluate_RMSE(self, rate_test):
        n_tests = rate_test.shape[0] # number of test
        SE = 0 # squared error
        for n in range(n_tests):
            pred = self.predict(rate_test[n, 0], rate_test[n, 1])
            SE += (pred - rate_test[n, 2])**2
        RMSE = np.sqrt(SE/n_tests)
        return RMSE

rate_train =ratings[0:129000]
rate_train = np.array(rate_train)
rate_test = ratings[129001:]
rate_test= np.array(rate_test)

print('Number of traing rates:', rate_train.shape[0])
print('Number of test rates:', rate_test.shape[0])

#indices start from 0
rate_train[:, :2] -= 1
rate_test[:, :2] -= 1
mf = MatrixFactorization(rate_train,customers,products,K = 50, lam = .01, print_every = 5, learning_rate = 50,max_iter = 30)
mf.fit()
# evaluate on test data
RMSE = mf.evaluate_RMSE(rate_test)
print("\nMatrix Factorization CF, RMSE = %.4f" %RMSE)
expected_score=3.8
print("Expected Score =",expected_score)
for c in customers.values[0:10]:
    customerId=c[0]
    customerName=c[1]
    print("Customer [",customerId,customerName,"], recommendation products:")
    for p in products.values:
        productId=p[0]
        productName=p[1]
        result=mf.predict(customerId,productId)
        if result>=expected_score:
            print("\t Recommend Product [",productName, "] Score=",result)