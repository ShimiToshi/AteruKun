from mykeras import keras_negapozi as myk

# filename = "./DATA4train_test/labled_good_data.pickle"
# filename2 = "./DATA4train_test/labled_bad_data.pickle"
filename = "./DATA4train_test/plaintxt10words.pickle"
filename2 = "./DATA4train_test/plaintxt10words_gomi.pickle"

cls = myk.NegaPosi(filename, filename2)
cls.pre_convertdata()
cls.makemodel()
cls.display_cdata()
cls.start()

cls.plotresult()
cls.resulttest()
cls.savemodel("newone")
#
#
# 学習済みはこっち
# cls = myk.NegaPosi(filename, None)
# cdata, clabel = cls.pre_convertdata()
# cls.loadmodel("test")
