---
layout: post
title: "Linear regression in Python"
author: "tomrod"
use_math: true
tags: [regression, probability, information, ML fundamentals ]
---

## Context

Linear regression is a fundamental methodology used in virtually all quantitative analysis. At its heart, you start with a model

$$Y_i = \beta X_i + \epsilon_i$$

where 

- $$Y_i$$ is the dependent variable
- $$\beta$$ is a vector of $$k{\times}1$$ coefficients
- $$X_i$$ is a $$k{\times}1$$ vector of independent data
- $$\epsilon_i$$ is normally distributed model error, $$\epsilon \sim N(0,\sigma^2)$$

Then, to find coefficients $$\beta$$, you find the expected value $$E(Y\|X)$$. This is equivalent to minimizing the sum of squared errors, $$\min_{\beta} \|Y-X\beta\|$$.

Linear regression's usefulness comes from it being the best linear unbiased estimator when a set of assumptions known as the [Gauss-Markov assumptions](https://en.wikipedia.org/wiki/Gauss%E2%80%93Markov_theorem) are satisfied. Basically:

- Irreducible model error are mean zero
- Model errors conditioned on explanatory variables are mean zero ( exogeneity )
- Errors are homoskedastic -- at different regions of the input space error distributions are equal

What does "Best Least Unbiased Estimator" mean? It means the statistical estimator with the least variance.

If you're coming from another statistical language like R, Python can sometimes feel cumbersome. However, Python excels at producing code reproducibility--allowing for workflow standardization. This post will review Python's common least squares approaches, and provide some boilerplate workflow code.

For this exercise we will use linear regression to build a model of *miles per gallon* (mpg) predicted by horsepower, engine cylinders, engine displacement, weight, acceleration, model year, origin, and car model. The data is sourced from the University of California Irvine's Donald Bren School of Information and Computer Science[^1] and has been used numerous times[^2].

## Prequisites

- Python 3
  - `pandas` (0.23.0)
  - `statsmodel` (0.9.0)
  - `matplotlib` (2.2.2)
- Internet access
- Working knowledge of linear regression


## Setting up data

The data source will be downloaded from the linked external site in a fixed-width format (fwf). It consists of the following fields:

1. mpg:           continuous
2. cylinders:     multi-valued discrete
3. displacement:  continuous
4. horsepower:    continuous
5. weight:        continuous
6. acceleration:  continuous
7. model year:    multi-valued discrete
8. origin:        multi-valued discrete
9. car name:      string (unique for each instance)

MPG (miles per gallon) is the regressand in our study. The remainder are regressors. Of these, 'multi-valued discrete' variables will be transformed to categorical variables. We will also drop all bad data represented by `np.nans`. We initialize and create the data using the following code.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_fwf('http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data', header=None)
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
```


## Generating training and validation datasets

We use an 80/20% split for training and validation. There are many ways to approach this. As the data is small, a simple choice rule using a uniform random varible `np.random.rand`. Three random vectors are also generated to add noise to highlight that stuffing a training set does result in higher fit on the training set, but does not improve fit on the testing set.

```python
msk = np.random.rand(len(df_clean)) < .8
df_clean['noise1'] = np.random.rand(len(df_clean)) < .8
df_clean['noise2'] = np.random.rand(len(df_clean)) < .8
df_clean['noise3'] = np.random.rand(len(df_clean)) < .8
train = df_clean[msk]
test = df_clean[~msk]
```

Multiple models are generated using `statsmodels`' formula designation. Each of these strings will server as a model. the term `C( variable, Sum)` forces the model to use a Categorical designation[^3]. More specifically, the `Sum` input uses Deviation Coding, which separates the effect of the categorical variable classes from the intercept. A hold out is still used -- in this case, the value of the hold-out coefficient is the negative sum of all the other coefficients within the group. So for example, an 8-cylinder's MPG average will be the sum area of origin 3 will be area of origin 1 and 2's coefficient multiplied by `-1`.

```python
models = {
    1 : 'mpg ~ weight',

    2 : 'mpg ~ weight + displacement',

    3 : 'mpg ~ weight + displacement + np.log(acceleration)',

    4 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int)',

    5 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) '
        '+ C(cylinders, Sum)',

    6 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) '
        '+ C(cylinders, Sum) + C(model_year, Sum)',

    7 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) '
        '+ C(cylinders, Sum) + C(model_year, Sum) + C(origin, Sum)',

    8 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) '
        '+ C(cylinders, Sum) + C(model_year, Sum) + C(origin, Sum) + C(car_name, Sum)',

    9 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) '
        '+ C(cylinders, Sum) + C(model_year, Sum) + C(origin, Sum) + C(car_name, Sum) + noise1',

    10 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) '
        '+ C(cylinders, Sum) + C(model_year, Sum) + C(origin, Sum) + C(car_name, Sum) + noise1 + noise2',

    11 : 'mpg ~ weight + displacement + np.log(acceleration) + np.log(horsepower_int) '
        '+ C(cylinders, Sum) + C(model_year, Sum) + C(origin, Sum) + C(car_name, Sum) + noise1 + noise2 + noise3',
}
```

## Validation assessment

`statsmodel` contains most standard fit metrics, including AIC, BIC, $$R^2$$, and similar. However, fit comparisons for testing data are not included. Accordingly, the class `Validation_fits` is created to assist with model fit for testing data.


```python
class Validation_fits():
    def __init__(self, results):
        self.train_results = results
        self.regressand = results.summary().tables[0].data[0][1]
    def ssres(self, test=None):
        if test is None: return self.train_results.ssr
        else: return sum((test[self.regressand] - self.train_results.predict(test))**2)
    def rsquared(self, test=None):
        if test is None: return self.train_results.rsquared
        else:
            m = test[self.regressand].mean()
            return 1 - self.ssres(test=test)/sum((test[self.regressand]-m)**2)
```

This class is used across each model to calculate the mean-squared error. Note that the MSE is directly calculated. `statsmodel` includes an MSE calculation, but normalizes by the model degrees of freedom rather than the number of observations. For our comparison purposes, we keep the MSE denominator as the number of observations[^4].

```python
train_mse = []
test_mse = []
for model_num in models:
    results = smf.ols(models[model_num], data=train).fit()
    v = Validation_fits(results)
    train_mse.append(v.train_results.ssr/len(train.mpg))
    test_mse.append(v.ssres(test)/len(test.mpg))
```

Finally, the relative fit for each of the models are plotted.

```python
plt.figure(figsize=(10,6))
plt.style.use('fivethirtyeight')
plt.plot(range(len(train_mse)), train_mse)
plt.plot(range(len(test_mse)), test_mse)
plt.xlabel('Model number id (increasing complexity)')
plt.ylabel('MSE')
plt.legend(['Train','Test'])
plt.show()
```

![png](/assets/images/20190111_bias_variance.png)

I hope you find this quick review of linear regression in Python using statsmodel to be helpful. To summarize what was accomplished:

- `pandas read_fwf` format for fixed-width format was shown
- Using data in Pandas from a web source was shown
- Using R-style formula for linear regression was shown. Note that this approach is not easily scalable -- alternatives will be discussed in a future post.
- OLS methodology was introduced
- Fit metrics for testing data were shown how to calculate
- How to use Python classes was shown

Each component is modular -- the data used, the models ran, the model methodology adopted, the test/train split, and so forth are substitutable.


## Footnotes


[^1]: Dua, D. and Karra Taniskidou, E. (2017). [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml). Irvine, CA: University of California, School of Information and Computer Science.

[^2]: [http://archive.ics.uci.edu/ml/datasets/Auto+MPG](http://archive.ics.uci.edu/ml/datasets/Auto+MPG)

[^3]: Categorical handling is actually one of the harder items to keep straight. It is good practice to double check this item during testing and code reviews. The Python package [`statsmodel`](https://www.statsmodels.org/dev/contrasts.html) handles at least four different types of categorical coding at time of writing.

[^4]: This means our measurement is biased (but consistent!) for the training MSE statistics. However, there is a tradeoff with interpretation. In order for the training and testing data to be compared with an "apples-to-apples" comparison, the normalization of the model fit should be consistent, such as with the number of observations. Using the residual degrees of freedom would result in a disparate measure between the training data and any data with a different number of observations.