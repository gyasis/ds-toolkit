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