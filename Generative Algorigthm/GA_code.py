# 2048KeyのGA実装。
# 参考にしたサイト：https://tech.mof-mof.co.jp/blog/ga-one-max-problem.html

import random
import custom_functions

from deap import base
from deap import creator
from deap import tools


# 適合度クラスを作成 FitnessMaxとIndividualクラス
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


toolbox = base.Toolbox()
# 鍵の素を生成をする関数を定義(00 - FF をランダムで選ぶ)
toolbox.register("single_byte", custom_functions.random_byte)
# 個体を生成する関数を定義(鍵を作るためにIndividualクラスでsingle_byteの値を32個持つ)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.single_byte, 32)
# 鍵の集団を生成する関数を定義(多量の鍵を持つlist)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# 評価関数はとりあえずランダム関数で置換してｱﾘﾏｽ。
# 評価関数　＞　[00-ff] * 128のリストを渡してるのでそこら辺の変換からが必要。
# ||||||||||||||||||||||||【関数の仕様】||||||||||||||||||||||||
# [00-ff]*128 -> 2048key -> 復号 -> シミズの関数で評価 -> 返す
def evalOneMax(individual):
    return random.random(),
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||


# 評価関数を登録
toolbox.register("evaluate", evalOneMax)
# 交叉関数を定義(二点交叉)
toolbox.register("mate", tools.cxTwoPoint)
# 変異関数を定義(バイト作り直し、変異隔離がバイトあたり5%)
# バイトを作り直すのか、いくつか足すのか、引くのか・・・（とりあえずつくりなおし）
# 関数の形式は：関数(individual, indpb)→戻り値：individual
toolbox.register("mutate", custom_functions.mutate_key, indpb=0.001)
# 選択関数を定義(トーナメント選択、tournsizeはトーナメントの数？)
toolbox.register("select", tools.selTournament, tournsize=3)


if __name__ == '__main__':
    # 初期集団を生成する
    pop = toolbox.population(n=300)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40  # 交差確率、突然変異確率、進化計算のループ回数

    print("進化開始")

    # 初期集団の個体を評価する
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):  # zipは複数変数の同時ループ
        # 適合性をセットする
        ind.fitness.values = fit

    print("  %i の個体を評価" % len(pop))

     # 進化計算開始
    for g in range(NGEN):
        print("-- %i 世代 --" % g)

        ##############
        # 選択
        ##############
         # 次世代の個体群を選択
        offspring = toolbox.select(pop, len(pop))
        # 個体群のクローンを生成
        offspring = list(map(toolbox.clone, offspring))

        # 選択した個体群に交差と突然変異を適応する

        ##############
        # 交叉
        ##############
        # 偶数番目と奇数番目の個体を取り出して交差
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                # 交叉された個体の適合度を削除する
                del child1.fitness.values
                del child2.fitness.values

        ##############
        # 変異
        ##############
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # 適合度が計算されていない個体を集めて適合度を計算
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  %i の個体を評価" % len(invalid_ind))

        # 次世代群をoffspringにする
        pop[:] = offspring

        # すべての個体の適合度を配列にする
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- 進化終了 --")

    best_ind = tools.selBest(pop, 1)[0]
    print(list(best_ind))
    print("最も優れていた個体: %s, %s" % (best_ind, best_ind.fitness.values))
    print(''.join([i[2:] for i in best_ind]))