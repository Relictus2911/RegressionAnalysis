import csv
from rpy2 import robjects
import sys
import subprocess
from rpy2.robjects import r, DataFrame
#r.png("scatter_regression.png", width=700, height=750)
# r.abline(a=yintercept, b=gradient, col="red")
print('hi')

dataset = DataFrame.from_csvfile('result.tsv', header=True, sep='\t')
print(r.cor(dataset))
nla = r.lm(formula='likes~.', data=dataset)
r.plot(nla)
#print(r.summary(nla))
#robjects.r["dev.off"]()
