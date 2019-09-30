from keras.datasets import imdb
from keras import models, layers

DEBUG = True

# https://qiita.com/hkambe/items/8c56ca8f0bbb4f895dee
import pickle
def loadpickle(filename):
    with open(filename, 'rb') as data:
        ret = pickle.load(data)
    return ret

def convertdata(data):
    datax = [i[0] for i in data]
    datay = [i[1] for i in data]
    return datax, datay



filename = "../DATA4train_test/labled_good_data.pickle"
data = loadpickle(filename)
x, y = convertdata(data)

import sys
sys.exit()

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

print(train_data)
print(train_labels)

print(type(train_data), len(train_data), type(train_labels), len(train_labels))

# N :次元数
N = 1000

# ラベルの変数を浮動小数に変更
y_train = np.asarray(train_labels).astype('float32')

#

model = models.Sequential()
model.add(layers.Dense(16, activation="relu", input_shape=(N,)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

if DEBUG:   model.summary()

# optimizer, 損失関数、merticsを指定。
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# データを学習用とバリデーション用に分割
x_val = x_train[:10000]
partial_x_train = x_train[10000:]
y_val = y_train[:10000]
partial_y_train = y_train[10000:]

# 学習開始
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=20,
                    batch_size=512,
                    validation_data=(x_val, y_val))
history_dict = history.history

# 精度確認用
results = model.evaluate(x_test, y_test)
print(results)
