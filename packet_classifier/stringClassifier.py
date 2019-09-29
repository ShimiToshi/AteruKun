import pandas as pd
import numpy as np
from sklearn import svm, metrics, preprocessing, model_selection

# https://shimi-shin.com/programming/python/knn-classification/
# https://techacademy.jp/magazine/17375

DEBUG = False


class Classifier:

    def __init__(self, data, target=0, maxstrlen="auto", sp=","):
        if type(data) == str:
            self.init_filename(data, sp=sp)
        elif type(data) == list:
            self.init_data(data)
        else:
            print("Error : ReadData ")
            return 1

        self.df_len = self.df.count()
        self.maxstrlen = maxstrlen
        self.target = target
        self.target_column = list(self.df.columns)[self.target]

        print(self.df)
        print("Complete : Loaded Data -> DataFrame")
        print("Status   : Data Count  -> ", self.df_len)

        # リストの形を学習しやすいように変換
        self.df_ret = change_baseformat(self.df, self.target_column, self.maxstrlen)
        self.df_ret = self.df_ret.fillna(ord(" "))
        self.df_value = self.df["value"]

    def init_filename(self, filename, sp=","):
        self.df = pd.read_csv(filename, sep=sp)

    def init_data(self, data):
        self.df = pd.DataFrame(data)
        self.df.columns = ["sentence", "value"]

    def pre_start(self):
        # まず標準化して、値を使いやすいようにする
        X = self.df_ret
        sc = preprocessing.StandardScaler()
        sc.fit(X)
        self.df_std=sc.transform(X)

    def start(self):
        # 学習開始
        #loss='squared_hinge' #loss="hinge", loss="log"
        self.clf_result=svm.LinearSVC(loss='hinge', C=1.0,class_weight='balanced', random_state=0)
        self.clf_result.fit(self.df_std, self.df_value)

    def check(self):
        # 6：K分割交差検証（cross validation）で性能を評価する---------------------
        scores=model_selection.cross_val_score(self.clf_result, self.df_std, self.df_value, cv=10)
        print("平均正解率 = ", scores.mean())
        print("正解率の標準偏差 = ", scores.std())

    def sep_check(self):
        # 7：トレーニングデータとテストデータに分けて実行してみる------------------
        X_train, X_test, train_label, test_label=model_selection.train_test_split(self.df_std,self.df_value, test_size=0.1, random_state=0)
        self.clf_result.fit(X_train, train_label)

        #正答率を求める
        pre=self.clf_result.predict(X_test)
        ac_score=metrics.accuracy_score(test_label, pre)
        print("正答率 = ",ac_score)

    def pinpoint_check(self, label=None):
        if label == None:
            label = self.df_ret[0]
        # 8：任意のデータに対する識別結果を見てみる------------------
        predicted_label=self.clf_result.predict([1,-1])
        print("このテストデータのラベル = ", predicted_label)

    def allprocess(self):
        print("SetUp Values")
        self.pre_start()
        print("Start MakingClassifier")
        self.start()
        print("Check Classifier")
        self.check()

        print("Check Using separate datas")
        self.sep_check()

        # print("pinpoint_check")
        # self.pinpoint_check()

def strtoint(str, count=None):
    # 文字をアスキーコードに変換してリスト化
    ret = []
    if DEBUG: print(str, type(str))

    if type(str) == bytes:
        mode = 1
    else:
        mode = 0

    for char in str:
        if DEBUG: print(type(char), char)
        if mode:
            ret.append(char)
        else:
            ret.append(ord(char))

    return ret

def change_baseformat(df, target, strmaxlen):
    # ニューラルネットワークに対応した形に変更

    print(target, strmaxlen)
    if strmaxlen == "auto":
        maxlen = max([len(i) for i in df[target]])
        print(maxlen)

    ret = []
    for st in df[target]:
        ret.append(strtoint(st[0:maxlen]))

    print(ret)
    return pd.DataFrame(ret)
