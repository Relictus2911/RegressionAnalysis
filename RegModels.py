from pandas import read_csv, DataFrame
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from warnings import simplefilter


simplefilter(action='ignore', category=FutureWarning)


def reg_methods(models, dataset): # Построение регрессионных моделей
    trg = dataset[['likes']]
    trn = dataset.drop(['likes'], axis=1)
    x_trn, x_test, y_trn, y_test = train_test_split(trn, trg, test_size=0.4)
    test_models = DataFrame()
    tmp = {}
    for model in models:
        m = str(model)
        tmp['Model'] = m[:m.index('(')]
        model.fit(x_trn, y_trn.iloc[:, 0])
        tmp['Reg1'] = r2_score(y_test.iloc[:, 0], model.predict(x_test))
        test_models = test_models.append([tmp], sort=True)
        if m.__contains__('RandomForestRegressor'):
            j=0
            name_of_rows = ['coms', 'favs', 'size']
            for feature in model.feature_importances_:
                print(name_of_rows[j], feature)
                j+=1
    test_models.set_index('Model', inplace=True, )
    paint_reg_methods(test_models)


def paint_reg_methods(test_models): # Построение графика
    fig, axes = plt.subplots(figsize=(16, 4))
    test_models.Reg1.plot(kind='barh', title='Regression Methods', fontsize=10, stacked=True)
    fig.savefig('result.png')


dataset = read_csv('main.tsv', '\t')
print(dataset.corr())
dataset_copy = dataset.copy()
print()

scaler = StandardScaler()
dataset_copy = scaler.fit_transform(dataset_copy)
dataset_copy = DataFrame(dataset_copy, columns=['likes', 'coms', 'favs', 'size'])
models = [LinearRegression(),  # метод наименьших квадратов
          RandomForestRegressor(n_estimators=100, max_features='sqrt'),  # случайный лес
          KNeighborsRegressor(n_neighbors=6),  # метод ближайших соседей
          SVR(kernel='linear', max_iter=100000)  # метод опорных векторов с линейным ядром
          ]

reg_methods(models, dataset_copy)
