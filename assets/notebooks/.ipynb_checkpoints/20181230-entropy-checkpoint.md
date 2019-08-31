

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
```


```python
x = np.linspace(.0001, .9999, 400)
y = -np.log(x) * x + -np.log(1-x)*(1-x)
plt.plot(x,y)
plt.show()
```


![png](20181230-entropy_files/20181230-entropy_1_0.png)



```python
import numpy as np
from scipy.stats import entropy
from scipy.stats import chi2
from scipy.stats import expon

dist1 = chi2.rvs(2, size=10000)
plt.figure(1)

plt.subplot(121)

plt.hist(dist1)


def ent(p,q):
    mm = min(min(p),min(q))
    MM = max(max(p), max(q))
    d1 = np.histogram(p, bins=100, range=(mm,MM))[0]/len(p)
    d2 = np.histogram(q, bins=100, range=(mm,MM))[0]/len(q)
    agg = 0
    for prob1, prob2 in zip(d1, d2):
        if prob1 ==0 or prob2 == 0:
            continue
        else:
            agg += prob1 * np.log(prob1/prob2)
    return agg

dist2 = expon.rvs(scale=2, size=10000)
plt.subplot(122)
plt.hist(dist2)
# plt.title('Exponential (scale=2) distribution with 10k draws')
plt.title('Chi2 (df=2, LHS) versus Exponential (scale=2, RHS) distribution with 10k draws')
plt.show()


x = np.linspace(0.1,4.1,100)
y = []
for val in x:
    new_dist = expon.rvs(scale=val, size=10000)
    y.append(ent(dist1,new_dist))
    
plt.figure()
plt.title('Entropy across several Exponential Scale Options')
plt.plot(x,y)
plt.show()
```


![png](20181230-entropy_files/20181230-entropy_2_0.png)



![png](20181230-entropy_files/20181230-entropy_2_1.png)



```python

```




    array([7.982e-01, 1.565e-01, 3.620e-02, 6.400e-03, 2.100e-03, 5.000e-04,
           0.000e+00, 0.000e+00, 0.000e+00, 1.000e-04])


