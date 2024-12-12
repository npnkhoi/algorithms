import json
data = json.load(open("out/all_results_merged.json"))
import matplotlib.pyplot as plt

ks = set()
rs = set()

for key in data:
    k, r = key.split('-')
    k = int(k)
    r = float(r)
    ks.add(k)
    rs.add(r)

ks = sorted(list(ks))
rs = sorted(list(rs))
# rs = [0.05, 0.1]

plt.figure(figsize=(8, 6), dpi=150)
for r in rs:
    values = [data[f"{k}-{r}"]['accidents'][0] for k in ks]
    print(ks, values)
    plt.plot(ks, values, label=f"r={r}", marker="o")
plt.legend()
plt.xscale('log')
plt.ylabel('log likelihood')
plt.xlabel('num components (k)')
plt.title('Random Forest of CL Trees on "accidents" dataset')

plt.savefig("plot.png")
