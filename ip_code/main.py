# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import seaborn as sns
import os

from scipy.stats import beta, norm
from numpy import histogram
import pylab

from module.model.ModelFactory import ModelFactory
from module.model.GaussianModel import GaussianModel

baseDir = os.getcwd()

model = GaussianModel()

log_rho_b_random = model.gaussian_random(np.log10(10), np.log10(100), 50)
model.plot_gaussian_random(log_rho_b_random, x_axis= 'log Rho_b')
plt.show()
rho_b_random = 10**(log_rho_b_random)
print('rho_b random : \n', rho_b_random)
print('min max rho_b :', rho_b_random.min(), rho_b_random.max())

log_rho_filePath = input("log_rho_b_random file name ::: ")
rho_b_filePath = input("rho_b_random file name ::: ")
log_filePath = baseDir + "\\" + log_rho_filePath
rho_filePath = baseDir + "\\" + rho_b_filePath
# save file
np.savetxt(log_filePath, log_rho_b_random)
np.savetxt(rho_filePath, rho_b_random)

'''
log_rho_b_random = gaussian_random(min_val = np.log10(10), max_val = np.log10(100), amount= 50)
plot_gaussian_random(log_rho_b_random, x_axis= 'log Rho_b')

rho_b_random = 10**(log_rho_b_random)
print('rho_b random : \n', rho_b_random)
print('min max rho_b :', rho_b_random.min(), rho_b_random.max())

#### change the min, max, amount
min_value = np.log10(10)
max_value = np.log10(100)
amount = 50

### list for the std deviation
lst = np.array([1, 1/2, 1/4])


#### plotting and make list random number for each sigma value 
plt.figure(figsize=(10,7))
for i in range(len(lst)):
    exec(f'log_rho_b_{i+1} = gaussian_random_2(min_val = min_value, max_val = max_value, amount= amount, multiplier = lst[i])')
    exec(f'rho_b_{i+1} = 10**(log_rho_b_{i+1})')
    exec(f'sns.distplot(log_rho_b_{i+1}, label = str(lst[i]))')
plt.xlabel('log rho b')
plt.legend()
plt.show()

plot_gaussian_random(log_rho_b_1, x_axis= 'log Rho_b')

print('fixed min max:', min_value, max_value)
#### save the result
### choose which data to be used --> change the name of data 

np.savetxt('log_rho_b_random.csv', log_rho_b_1)
np.savetxt('rho_b_random.csv', rho_b_1)
#### calculate gaussian random number - 3

#### change the min, max, amount
min_value = 0.05
max_value = 0.8
amount = 20

### list for the std deviation
lst = np.array([1, 15, 30])


#### plotting and make list random number for each lst value 
plt.figure(figsize=(10,7))
for i in range(len(lst)):
    exec(f'charg_{i+1} = gaussian_random_3(a= lst[i], b= lst[i], min_val = min_value, max_val = max_value, amount= amount)')
    exec(f'sns.distplot(charg_{i+1}, label = str(lst[i]))')
plt.xlabel('charg')
plt.legend()
plt.show()

#### result:
#### make varible for each lst
#### variable name results:
#### charg_1 --> used lst = 1
#### charg_2 --> used lst = 15
#### charg_3 --> used lst = 30


plot_gaussian_random(charg_1, x_axis= 'charg')

print('fixed min max:', min_value, max_value)

np.savetxt('charg_random.csv', charg_1)

#### calculate gaussian random number - 3

#### change the min, max, amount
min_value = np.log10(1E-7)
max_value = np.log10(100)
amount = 20

### list for the std deviation
lst = np.array([1, 15, 30])


#### plotting and make list random number for each sigma value 
plt.figure(figsize=(10,7))
for i in range(len(lst)):
    exec(f'log_tau_{i+1} = gaussian_random_3(a= lst[i], b= lst[i], min_val = min_value, max_val = max_value, amount= amount)')
    exec(f'tau_{i+1} = 10**(log_tau_{i+1})')
    exec(f'sns.distplot(log_tau_{i+1}, label = str(lst[i]))')
plt.xlabel('log tau')
plt.legend()
plt.show()


#### result:
#### make varible for each lst
#### variable name results:
#### log_tau_1 --> used lst = 1
#### log_tau_2 --> used lst = 15
#### log_tau_3 --> used lst = 30

tau_1

#### plotting only for one sigma

plot_gaussian_random(log_tau_1, x_axis= 'log_tau')

print('fixed min max:', min_value, max_value)

#### save the result
### choose which data to be used --> change the name of data 

np.savetxt('log_tau_random.csv', log_tau_1)
np.savetxt('tau_random.csv', tau_1)

#### calculate gaussian random number - 1

c_random = gaussian_random(min_val = 0.1, max_val = 0.6, amount = 5)
plot_gaussian_random(c_random, x_axis= 'c')

#### save the result
np.savetxt('c_random.csv', c_random)
#### calculate gaussian random number - 3

#### change the min, max, amount
min_value = 0.1
max_value = 0.6
amounts = 5

### list for the std deviation
lst = np.array([1, 15, 30])


#### plotting and make list random number for each sigma value 
plt.figure(figsize=(10,7))
for i in range(len(lst)):
    exec(f'c_{i+1} = gaussian_random_3(a= lst[i], b= lst[i], min_val = min_value, max_val = max_value, amount= amount)')
    exec(f'sns.distplot(c_{i+1}, label = str(lst[i]))')
plt.xlabel('c')
plt.legend()
plt.show()


#### result:
#### make varible for each lst
#### variable name results:
#### c_1 --> used lst = 1
#### c_2 --> used lst = 15
#### c_3 --> used lst = 30

#### plotting only for one sigma

plot_gaussian_random(c_1, x_axis= 'c')

print('fixed min max:', min_value, max_value)

#### save the result
### choose which data to be used --> change the name of data

np.savetxt('c_random.csv', c_1)

### https://stackoverflow.com/questions/62364477/python-random-number-generator-within-a-normal-distribution-with-min-and-max-val

from scipy.stats import beta, norm
from numpy import histogram
import pylab

max_time = 5
min_time = 0.5

a, b = 7, 11
dist = beta(a, b)
# dist = norm(a, b)

for _ in range(1):
    sample2 = min_time + dist.rvs(size=1000) * (max_time - min_time)
    his, bins = histogram(sample2, bins=20, density=True)
    pylab.plot(bins[:-1], his, ".")
pylab.xlabel("Reaction time [s]")
pylab.ylabel("Probability density [1/s]")
pylab.grid()
pylab.show()

min_value = 0.05
max_value = 0.8
amount = 20

result_1 = gauss_calc(a= 1, b= 1, min_value= min_value, max_value= max_value, amount= amount)
result_2 = gauss_calc(a= 15, b= 15, min_value= min_value, max_value= max_value, amount= amount)
result_3 = gauss_calc(a= 30, b= 30, min_value= min_value, max_value= max_value, amount= amount)

sns.distplot(result_1, label='1')
sns.distplot(result_2, label='2')
sns.distplot(result_3, label='3')
plt.legend()

print(result_1.min(), result_1.max())
print(result_2.min(), result_2.max())
print(result_3.min(), result_3.max())

def for_log_val(min_val, max_val, amount):
    log_list = np.linspace(np.log10(min_val), np.log10(max_val), amount)
    ori_num_list = 10**(log_list)
    return log_list
    
rho_zero_list = for_log_val(min_val= 10, max_val= 100, amount= 50)
rho_zero_list

log_rho_zero = np.linspace(np.log10(10), np.log10(100), 50)
log_rho_zero

#### LINEAR SPACING
#### definition for log value
def for_log_val(min_val, max_val, amount):
    log_list = np.linspace(np.log10(min_val), np.log10(max_val), amount)
    ori_num_list = 10**(log_list)
    return ori_num_list
    
rho_zero_linear = for_log_val(min_val= 10, max_val= 100, amount= 50)
tau_linear = for_log_val(min_val= 1E-7, max_val= 100, amount= 50)

charg_linear = np.linspace(0.05, 0.8, 20)
c_linear = np.linspace(0.1, 0.6, 5)

np.savetxt('rho_zero_linear.csv', rho_zero_linear)
np.savetxt('charg_linear.csv', charg_linear)
np.savetxt('tau_linear.csv', tau_linear)
np.savetxt('c_linear.csv', c_linear)
'''


