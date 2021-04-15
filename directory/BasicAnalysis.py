def collectNames(dataframe):
        columns = list(dataframe.columns)
        return columns 
       

def collectgraph(dataframe, columns):

    #future feature - ask for a Y variable to drop
    
    #Scaling is needed correctly show all variables distribution at the same time -> Scaling prep
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    
    scaler = StandardScaler()
    minmax = MinMaxScaler()


    tempdf = dataframe.select_dtypes(exclude=['object'])
    o_length = len(columns)
    new_length = len(list(tempdf.columns))
    dropped_columns = o_length - new_length

    #scale data
    tempdf = scaler.fit_transform(tempdf)

    #warn of dropped columns
    if (dropped_columns > 0):
        print(dropped_columns,"columns were dropped")
        print("try to convert the dropped columns")

    #Print preliminary info of original data frame
    print(dataframe.info())
    print(dataframe.isna().sum())
    print(dataframe.isna().sum() * 100)

    
    #graphing
    fig, (ax1) = plt.subplots(ncols=1, figsize=(10, 8))
    ax1.set_title('Original Distributions')
    sns.kdeplot(data = tempdf,ax=ax1, legend=True)
    
    sns.heatmap(dfTrain.corr(),ax=ax1 annot=True);

    sns.pairplot(dataframe,ax=ax1 diag_kind='kde')

    
def buildgraph(dataframe):
    columns = collectNames(dataframe)
    collectgraph(dataframe, columns)