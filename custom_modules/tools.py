

# checking target column splits and 
def prepare_class_split(dataframe, target="class_name", p_split=0.30, test_target_split=0.50):
  dataframe = dataframe.copy()
  df_len = len(dataframe)
  class_amount = len(dataframe[target].unique())
  df_split = int(df_len * p_split)
  class_list = list(dataframe[target].unique())
  print(class_list)
  proposed_split = df_split/class_amount
  
  class_counts = dataframe[target].value_counts()
  # print(df_len,df_split,proposed_split,class_counts)
  
  outcomes = []
  
  
  print("Total of Test Split is {} and Proposed split is {}".format(df_split,proposed_split))
  
  
  for lable in class_list:
    percent_split = class_counts[lable] / df_len
    proposed_percent_split = class_counts[lable] / df_split
    
    if class_counts[lable] >= proposed_split * 2:
      print("Class {} is OK!!".format(lable))
      outcomes.append("OK!!")
    elif class_counts[lable] < proposed_split * 2 and class_counts[lable] > proposed_split:
      print("Class {} fails equity threshold, look to augment training dataset ".format(lable))
      outcomes.append("Augment??")
    elif class_counts[lable] < proposed_split:
      print("Class {} is {} and Proposed split is {}".format(lable,class_counts[lable],proposed_split))
      print("Class " + lable + " is less than the proposed split")
      print("Class {} is {} and the proposed split is {}".format(lable,class_counts[lable],proposed_split))
      print("Both augmentation and weights may be necessary!!")
      outcomes.append("Weights/Augment/Split!!")
      
  print(len(class_list))
  print(len(outcomes))
  outcomes_df = pd.DataFrame()
  outcomes_df["Class"] = class_list
  outcomes_df["Percent Split"] = percent_split
  outcomes_df["Outcome"] = outcomes
  outcomes_df.set_index("Class", inplace=True)
  return outcomes_df


# gets weights and graphs changes 
def get_class_frequencies(dataframe,target):
  try:
    dataframe = pd.get_dummies(dataframe[target].astype(str))
  except:
    dataframe = pd.get_dummies(dataframe[target])
    
  f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
  sample_array = np.array(dataframe)
  positive_freq = sample_array.sum(axis=0) / sample_array.shape[0]
  negative_freq = np.ones(positive_freq.shape) - positive_freq
  data = pd.DataFrame({"Class": dataframe.columns, "Label": "Positive", "Value": positive_freq})
  data = data.append([{"Class": dataframe.columns[l], "Label": "Negative", "Value": v} for l, v in enumerate(negative_freq)], ignore_index=True)
  plt.xticks(rotation=90)
  sns.barplot(x="Class", y="Value",hue="Label", data=data, ax=ax1)
  pos_weights = negative_freq
  neg_weights = positive_freq
  pos_contribution = positive_freq * pos_weights
  neg_contribution = negative_freq * neg_weights

  # print("Weight to be added:  ",pos_contribution)
  
  data1 = pd.DataFrame({"Class": dataframe.columns, "Label": "Positive", "Value": pos_contribution})
  data1 = data1.append([{"Class": dataframe.columns[l], "Label": "Negative", "Value": v} for l, v in enumerate(neg_contribution)], ignore_index=True)
  ax1.tick_params(axis='x', labelrotation=90)
  ax2.tick_params(axis='x', labelrotation=90)
  sns.barplot(x="Class", y="Value",hue="Label", data=data1, ax=ax2)
  
  return pos_contribution


def lists2df(list1, list2, title1, title2):
    df = pd.DataFrame(zip(list1, list2), columns =[title1, title2])
    return df