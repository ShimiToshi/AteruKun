import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras import models, layers
from keras.models import model_from_json

def loadpickle(filename):
    with open(filename, 'rb') as data:
        ret = pickle.load(data)
    return ret

def convertdata(data):
    datax = [i[0] for i in data]
    datay = [i[1] for i in data]
    return datax, datay

def strtoint(str, count=None):
    # 文字をアスキーコードに変換してリスト化
    ret = []
    if type(str) == bytes:
        mode = 1
    else:
        mode = 0

    for char in str:
        if mode:
            ret.append(char)
        else:
            ret.append(ord(char))
    return ret

def change_baseformat(df):
    # 入力次元数を合わせるため、最大次元数を調べる
    maxlen = max([len(str(i)) for i in df.values])
    print("MAX Dimension :", maxlen)

    ret = []
    for values in df.values:
        ret.append(strtoint(str(values)))
    return pd.DataFrame(ret), maxlen

class NegaPosi:

    base1_data = []
    base1_label = []
    base2_data = []
    base2_label = []

    train_data = []
    train_label = []
    test_data = []
    test_label = []

    history_dict = {}

    def __init__(self, filename, filename2=None):
        self.filename = filename
        bdata = loadpickle(filename)
        self.base1_data, self.base1_label = convertdata(bdata)

        print("Loaded and Converted Datas 1: ", len(self.base1_data))

        if filename:
            self.filename2 = filename2
            bdata = loadpickle(filename2)
            self.base2_data, self.base2_label = convertdata(bdata)
            print("Loaded and Converted Datas 2: ", len(self.base2_data))

        self.separate_datas()

    def separate_datas(self):
        # datas をtrain とtestデータに分割（2等分）
        harf = int(len(self.base1_data) / 2)

        self.train_data  = self.base1_data[0:harf]
        self.test_data   = self.base1_data[harf:]
        self.train_label = self.base1_label[0:harf]
        self.test_label  = self.base1_label[harf:]

        if self.filename2:
            harf = int(len(self.base2_data) / 2)
            self.train_data.extend(self.base2_data[0:harf])
            self.test_data.extend(self.base2_data[harf:])
            self.train_label.extend(self.base2_label[0:harf])
            self.test_label.extend(self.base2_label[harf:])

        print("Separated Train and Test Datas :")
        print("Train Status (LEN: data, label):", len(self.train_data), len(self.train_label))
        print(" Test Status (LEN: data, label):", len(self.test_data), len(self.test_label))

    def pre_convertdata(self):
        self.ctrain_data, self.ctrain_label = self.convertdata(self.train_data, self.train_label)
        print("Converted Train Status (LEN: data, label):", len(self.ctrain_data), len(self.ctrain_label))
        self.ctest_data, self.ctest_label = self.convertdata(self.test_data, self.test_label)
        print("Converted  Test Status (LEN: data, label):", len(self.ctest_data), len(self.ctest_label))

    def convertdata(self, data, label):
        df = pd.DataFrame(data)
        print(df.head())

        # リストの形を学習しやすいように変換
        ctrain_data, self.maxdimension = change_baseformat(df)
        cdata = ctrain_data.fillna(ord(" ")).values
        cdata = cdata.astype("float32")
        clabel = label
        return cdata, clabel

    def makemodel(self):
        self.model = models.Sequential()
        self.model.add(layers.Dense(16, activation="relu", input_shape=(self.maxdimension,)))
        self.model.add(layers.Dense(16, activation='relu'))
        self.model.add(layers.Dense(1, activation='sigmoid'))

        print(self.model.summary())

    def start(self):
        # optimizer, 損失関数、merticsを指定。
        self.model.compile(optimizer='rmsprop',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        # データを学習用とバリデーション用に分割
        x_val = self.ctrain_data[::2]
        partial_x_train = self.ctrain_data[1::2]
        y_val = self.ctrain_label[::2]
        partial_y_train =self.ctrain_label[1::2]

        # 学習開始
        history = self.model.fit(partial_x_train,
                            partial_y_train,
                            epochs=20,
                            batch_size=512,
                            validation_data=(x_val, y_val))
        self.history_dict = history.history

    def resulttest(self):
        print("Test Results :")
        results = self.model.evaluate(self.ctest_data, self.ctest_label)
        print(results)

    def plotresult(self):
        print("Requested Plot Histroy :")
        if self.history_dict:
            print(self.history_dict)
            loss_values = self.history_dict['loss']
            val_loss_values = self.history_dict['val_loss']
            acc = self.history_dict['accuracy']

            epochs = range(1, len(acc) + 1)

            plt.plot(epochs, loss_values, 'bo', label='Training loss')
            plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
            plt.title('Training and validation loss')
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.legend()
            print("Ploted")
            plt.show()

            val_acc_values = self.history_dict['val_accuracy']
            plt.plot(epochs, acc, 'bo', label='Training acc')
            plt.plot(epochs, val_acc_values, 'b', label='Validation acc')
            plt.title('Training and validation accuracy')
            plt.xlabel('Epochs')
            plt.ylabel('Accuracy')
            plt.legend()

            plt.show()
        else:
            print("Cant Solve Request... -> Not start")

    def loadmodel(self, filename):
        self.model = model_from_json(open(filename + ".json", 'r').read())
        # 重みの読み込み
        self.model.load_weights(filename + ".h5")

        print("savefile : ", filename, "(json, h5)", )

    def savemodel(self, savename):
        open(savename +".json", "w").write(self.model.to_json())

        # 学習済みの重みを保存
        self.model.save_weights(savename + '.h5')
        print("loadfile : ", savename, "(json, h5)", )
