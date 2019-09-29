import pandas as pd
import numpy as np
from sklearn import svm, metrics, preprocessing, model_selection

# https://shimi-shin.com/programming/python/knn-classification/
# https://techacademy.jp/magazine/17375

def strtoint(str, count=None):
    # 文字をアスキーコードに変換してリスト化
    ret = []
    for char in str:
        print(char, ord(char))
        ret.append(ord(char))

    return ret

filename = "seccup_exp.csv"
df = pd.read_csv(filename, sep=",")
print(df)

d_value = df["value"]

retmat = []
for st in df["sentence"]:
    retmat.append(strtoint(st))

df_retmat = pd.DataFrame(retmat)
print(df_retmat)

X = df_retmat
sc = preprocessing.StandardScaler()
sc.fit(X)
X_std=sc.transform(X)
print(X_std)

clf_result=svm.LinearSVC(loss='hinge', C=1.0,class_weight='balanced', random_state=0)#loss='squared_hinge' #loss="hinge", loss="log"
clf_result.fit(X_std, d_value)

# 6：K分割交差検証（cross validation）で性能を評価する---------------------
scores=model_selection.cross_val_score(clf_result, X_std, d_value, cv=10)
print("平均正解率 = ", scores.mean())
print("正解率の標準偏差 = ", scores.std())

# 7：トレーニングデータとテストデータに分けて実行してみる------------------
X_train, X_test, train_label, test_label=model_selection.train_test_split(X_std,d_value, test_size=0.1, random_state=0)
clf_result.fit(X_train, train_label)
#正答率を求める
pre=clf_result.predict(X_test)
ac_score=metrics.accuracy_score(test_label,pre)
print("正答率 = ",ac_score)

# 8：任意のデータに対する識別結果を見てみる------------------
predicted_label=clf_result.predict()
print("このテストデータのラベル = ", predicted_label)

# 9：識別平面の式を手に入れる--------------------------------
print(clf_result.intercept_)
print(clf_result.coef_ )  #coef[0]*x+coef[1]*y+intercept=0
