import matplotlib.pyplot as plt
import json

path = 'simulation_results/2022_7_4_123'
f = open(path + '/NF_test.json')
data = json.load(f)
f.close()
data = list(data.values())
n = len(data)
NF = list()
for i in range(n-1):
    tem = data[-i-1] - data[-i-2]
    NF.append(tem)

_, axis= plt.subplots(sharex=True, figsize=(10,5))
axis.violinplot(NF, showmeans=True)
plt.savefig(path + '/NF.png')