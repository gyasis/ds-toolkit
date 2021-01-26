import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


## Function to choose two columns for least squares 

# enter dataframe, and column names 

def LeastSquares(df,X,Y):

    
    # slice dataframe after input of desired X and Y variables 

    tempdf = df[[X, Y]]
    
    # add columns 

    tempdf['X2'] = tempdf[X].apply(lambda x:(x**2))
    tempdf['XY'] = tempdf[X] * tempdf[Y]

    # build variables 
   
    x_mean = tempdf.X.mean()
    y_mean = tempdf.Y.mean()
    x_sum = tempdf.X.sum()
    y_sum = tempdf.Y.sum()
    x2_sum = tempdf.X2.sum()
    xy_sum = tempdf.XY.sum()
    
    # find slop of regression line 
    # y = mx + b ----> m, slope and b, y-intercept

    N = len(tempdf.X)
    m = (N * xy_sum - x_sum * y_sum)/(N * x2_sum - (x_sum ** 2))
    b = (y_sum - m * x_sum)/ N


    # return Dataframe and info ...needs to be an array
    Result = [tempdf, m, b, x_sum, y_sum, x2_sum, xy_sum, x_mean, y_mean]
    print(Result[1:])

    #plot the data
    plt.style.use('seaborn-whitegrid')
    plt.scatter(data.X, data.Y)
    plt.plot(data.X,(m * data.X + b), color='r')
    return Result
