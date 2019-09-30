from keras.keras_negaposi import NegaPosi

filename = "./DATA4train_test/labled_good_data.pickle"
filename2 = "./DATA4train_test/labled_bad_data.pickle"

cls = NegaPosi(filename, filename2)
