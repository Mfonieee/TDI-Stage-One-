# import the necessary libraries
import pandas as pd
import numpy as ny
import matplotlib.pyplot as plt
import seaborn as sns

# load the dataset
df= pd.read_csv('Comprehensive_Banking_Database.csv')
df.head()

# cleaning of the data
# check the structure of the data
df.info()
# change the data types of the dates column
date_cols = ['Date Of Account Opening','Last Transaction Date','Transaction Date','Approval/Rejection Date',
                'Payment Due Date', 'Last Credit Card Payment Date','Feedback Date','Resolution Date']
df[date_cols]= df[date_cols].apply(pd.to_datetime,errors='coerce')
# Check the data types again
df.dtypes
# Confirm if there are any invalid dates
for col in date_cols:
    print(f"{col}:{df[col].isna().sum()} invalid dates")

#check for missing values
df.isnull().sum()

# check for duplicates
df.duplicated().sum()

# To show all the columns at once
pd.set_option("display.max_columns",None)

#check the statistical frequency and outlier
df.describe()

# Check for outlier in the Loan amount column
sns.boxplot(x=df['Loan Amount'], color='skyblue')
plt.title(['Boxplot Loan Amount'])
plt.tight_layout()
plt.show()

# Check for outlier in the Account Balance After Transaction column
sns.boxplot(x=df['Account Balance After Transaction'], color='skyblue')
plt.title(['Bokplot'])
plt.tight_layout()
plt.show()

# Check for outlier in the Transaction Amount column
sns.boxplot(x=df['Transaction Amount'], color='skyblue')
plt.title(['Bokplot'])
plt.tight_layout()
plt.show()

# Check for outlier in the Interest Rate column
sns.boxplot(x=df['Interest Rate'], color='skyblue')
plt.title(['Bokplot'])
plt.tight_layout()
plt.show()
