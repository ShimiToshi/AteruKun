from mykeras import keras_negapozi as myk

filename = "./DATA4train_test/labled_good_data.pickle"
filename2 = "./DATA4train_test/labled_bad_data.pickle"

cls = myk.NegaPosi(filename, filename2)
cls.pre_convertdata()
cls.makemodel()
cls.start()

cls.plotresult()
cls.resulttest()

cls.savemodel("test")
cls.loadmodel("test")
