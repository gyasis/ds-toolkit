def get_class_frequencies():
  positive_freq = s_array.sum(axis=0) / s_array.shape[0]
  negative_freq = np.ones(positive_freq.shape) - positive_freq
  return positive_freq, negative_freq

p,n = get_class_frequencies()

data = pd.DataFrame({"Class": df1.columns, "Label": "Positive", "Value": p})
data = data.append([{"Class": df1.columns[l], "Label": "Negative", "Value": v} for l, v in enumerate(n)], ignore_index=True)
plt.xticks(rotation=90)
f = sns.barplot(x="Class", y="Value",hue="Label", data=data)
plt.savefig("skewness.png")

pos_weights = n
neg_weights = p
pos_contribution = p * pos_weights
neg_contribution = n * neg_weights
print(p)
print(n)
print("Weight to be added:  ",pos_contribution)
def get_class_frequencies():
  positive_freq = s_array.sum(axis=0) / s_array.shape[0]
  negative_freq = np.ones(positive_freq.shape) - positive_freq
  return positive_freq, negative_freq

p,n = get_class_frequencies()
data = pd.DataFrame({"Class": df1.columns, "Label": "Positive", "Value": p})
data = data.append([{"Class": df1.columns[l], "Label": "Negative", "Value": v} for l, v in enumerate(n)], ignore_index=True)
plt.xticks(rotation=90)
f = sns.barplot(x="Class", y="Value",hue="Label", data=data)
plt.savefig("skewness.png")

pos_weights = n
neg_weights = p
pos_contribution = p * pos_weights
neg_contribution = n * neg_weights
print(p)
print(n)
print("Weight to be added:  ",pos_contribution)

data = pd.DataFrame({"Class": df1.columns, "Label": "Positive", "Value": pos_contribution})
data = data.append([{"Class": df1.columns[l], "Label": "Negative", "Value": v} for l, v in enumerate(neg_contribution)], ignore_index=True)
plt.xticks(rotation=90)
g = sns.barplot(x="Class", y="Value",hue="Label", data=data)