import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels

def dummy_prep(data, method=None, error_none=True):
    varlist = data.select_dtypes(include='category').columns
    if len(varlist) == 0 and error_none: return
    if len(varlist) == 0 and not error_none: 
        raise ValueError('dummy_prep expects a categoricical variable')
    if not method: 
        return pd.get_dummies(data[varlist])
    if method == 'drop_first':
        return pd.get_dummies(data[varlist], drop_first=True)
    if method == 'deviation':
        dummies = pd.get_dummies(data[varlist])
        dummylist = {i:[x for x in dummies.columns if i in x] for i in varlist}
        for var in dummylist:
            dropout = dummylist[var][0]
            keepers = dummylist[var][1:]
            dummies.loc[dummies[dropout]==1, keepers] = -1
            del dummies[dropout]
        dummies.replace(255,-1,inplace=True)
        return dummies
    
def features_prep(data, dummy_method=None):
    if sum(data.dtypes=='object') > 0: raise ValueError(
        'Data should have object dtypes replaced with categoricals'
        ' or otherwise cleaned before running feature_prep function')
    categoricals = dummy_prep(data, method=dummy_method)
    numericals = data.select_dtypes(exclude=['object','category'])
    return pd.concat([numericals, categoricals], axis=1)

def rsquared(x, p):
    mean = x.mean()
    sstot = sum((x-mean)*(x-mean))
    ssres = sum((x-p)*(x-p))
    return 1 - ssres / sstot

def aic(x,p, k):
    ssres = sum((x-p)**2)
    aic = 2 * k - 2 * np.log(ssres)
    return aic

df = pd.read_fwf('~/auto-mpg.data', header=None)
df.columns=['mpg','cylinders','displacement',
            'horsepower','weight','acceleration',
            'model_year','origin','car_name']
df['horsepower_int'] = pd.to_numeric(df.horsepower,errors='coerce')
df['car_name'] = pd.Categorical(df.car_name)
df['origin'] = pd.Categorical(df.origin)
df['model_year'] = pd.Categorical(df.model_year)
df['cylinder'] = pd.Categorical(df.cylinders)
del df['horsepower']
df_clean = df.dropna()

msk = (np.random.rand(len(df_clean)) < .8)
df_clean['noise1'] = (np.random.rand(len(df_clean)) < .8)
df_clean['noise2'] = (np.random.rand(len(df_clean)) < .8)
df_clean['noise3'] = (np.random.rand(len(df_clean)) < .8)
train = df_clean.loc[msk,:].copy(deep=True)
test = df_clean.loc[~msk, :].copy(deep=True)

models = {
#     0 : 'mpg ~ 1',
    1 : 'mpg ~ weight',
    2 : 'mpg ~ weight + displacement',
    3 : 'mpg ~ weight + displacement + np.log(acceleration)',
    4 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int)',
    5 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) + C(cylinders, Sum)',
    6 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) + C(cylinders, Sum) + C(model_year, Sum)',
    7 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) + C(cylinders, Sum) + C(model_year, Sum) + C(origin, Sum)',
    8 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) + C(cylinders, Sum) + C(model_year, Sum) + C(origin, Sum) + C(car_name, Sum)',
    9 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) + C(cylinders, Sum) + C(model_year, Sum) + C(origin, Sum) + C(car_name, Sum) + noise1',
    10 :'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) + C(cylinders, Sum) + C(model_year, Sum) + C(origin, Sum) + C(car_name, Sum) + noise1 + noise2',
    11 :'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) + C(cylinders, Sum) + C(model_year, Sum) + C(origin, Sum) + C(car_name, Sum) + noise1 + noise2 + noise3',
}


class Validation_fits():
    def __init__(self, results):
        self.train_results = results
        self.regressand = results.summary().tables[0].data[0][1]
    
    def ssres(self, test=None):
        if test is None: return self.train_results.ssr
        else: return sum((test[self.regressand] - self.train_results.predict(test))**2)
    
    def aic(self, test=None):
        if test is None: aic = self.train_results.aic
        else: 
            aic = 2 * self.train_results.df_resid + self.train_results.nobs * (1 + np.log(np.pi) + 
                np.log(self.ssres(test)))
        return aic
    
    def rsquared(self, test=None):
        if test is None: return self.train_results.rsquared
        else:
            m = test[self.regressand].mean()
            return 1 - self.ssres(test=test)/sum((test[self.regressand]-m)**2)

train_results = []
test_results = []
for model in models:
    results = smf.ols(
        models[model]
    , data=train).fit()
    v = Validation_fits(results)
    train_results.append(results.ssr/len(train))
    test_results.append(v.ssres(test)/len(test))
    
dd = pd.DataFrame(test_results, columns=['Test_Results'])
dd['Train_Results'] = train_results
dd.to_csv('~/results.csv', index=False)