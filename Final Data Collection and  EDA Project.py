#!/usr/bin/env python
# coding: utf-8

# 
# 

# In[ ]:


#import liabraries
import requests
from bs4 import BeautifulSoup
import time


# In[2]:


# url from flipkart
page="https://www.flipkart.com/search?q=washing+machine&sid=j9e%2Cabm%2C8qx&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&as-pos=1&as-type=RECENT&suggestionId=washing+machine%7CWashing+Machines&requestId=e5be74ee-8075-436c-9e29-b02799683793&as-searchtext=washing%20machine"


# In[3]:


response=requests.get(page)


# In[4]:


response


# In[5]:


product_names=[]
prices=[]

# no. of pages to scrape
num_page=20


#loop for multiple pages
for i in range(1,num_page + 1):
    url=f"https://www.flipkart.com/search?q=washing+machine&sid=j9e%2Cabm%2C8qx&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&as-pos=1&as-type=RECENT&suggestionId=washing+machine%7CWashing+Machines&requestId=e5be74ee-8075-436c-9e29-b02799683793&as-searchtext=washing+machine&page={i}"
    print(f"Scraping URL : {url}")
    page=requests.get(url)
    soup=BeautifulSoup(page.text,'html.parser')
    products=soup.find_all('div',{'class':'tUxRFH'})
    for product in products:
        title=product.find('div',{'class':'KzDlHZ'})
        price=product.find('div',{'class':'Nx9bqj _4b5DiR'})
        if title and price:
            product_names.append(title.get_text())
            prices.append(price.get_text())
        
        
            print(f"product:{title.get_text()} - Price:{price.get_text()}")
    else:
        print(f"Failed to retrieve page {i}")
    
    
    time.sleep(3)
  

    


# In[6]:


products=soup.find_all('div',{'class':'tUxRFH'})


# In[7]:


# loop through each product found on page
for product in products:
    title=product.find('div',{'class':'KzDlHZ'})
    price=product.find('div',{'class':'Nx9bqj _4b5DiR'})
    if title and price:
        product_names.append(title.get_text())
        prices.append(price.get_text())
        
        # print product title and price
        print(f"product:{title.get_text()}-Price:{price.get_text()}")
    else:
        print(f"Failed to retrieve page {i}")
    
    
    time.sleep(3)
  

    


# In[118]:


import pandas as pd
# read csv file
df = pd.read_csv('washing_machine.csv')


# In[119]:


df


# 
# 

# In[120]:


# import regular expression
import re
df['Brand Name']=df['Product Name'].apply(lambda x :re.findall(r'^[A-Za-z]+(?: [A-Za-z]+)?',x)[0])


# In[121]:


df.head(2)    


# In[122]:


df['model']=df['Product Name'].apply(lambda x : re.findall(r'^[A-Za-z]+(?: [A-Za-z]+)?(.*)',x)[0])


# In[123]:


df.head(2)
   


# In[124]:


df['capacity']=df['Product Name'].apply(lambda x : re.findall(r'\d+\s*kg',x))


# In[125]:


df.head(5)


# In[126]:


df['type']=df['Product Name'].apply(lambda x : re.findall(r'\b(Semi\s?Automatic|Fully\s?Automatic|Top\s?Load|Front\s?Load|Pulsator|Inverter|Washer only|Aqua\s?Magic|Balance\s?Clean)\b',x))
df


# In[127]:


df.drop(columns=['Product Name'],inplace=True)
df.head(2)


# In[128]:


df['capacity']=df['capacity'].astype(str)
df['type']=df['type'].astype(str)
df['Price']=df['Price'].str.replace('₹','').str.replace(',','').astype(float)


# In[129]:


df['capacity']=df['capacity'].str.replace('[','').str.replace(']','')
df['type']=df['type'].str.replace('[','').str.replace(']','')
df



# In[130]:


df['type']=df['type'].str.strip()


# In[131]:


# replace empty list
df['type']=df['type'].replace('','Not available')

# fill missing values
df['Price'].fillna(df['Price'].median(),inplace=True)
print(df.head())


# In[157]:


import  pandas as pd


# In[158]:


# save cleaned data
df.to_csv('cleaned.csv')


# In[159]:


df.head(1)


# In[165]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[166]:


mean_price=df['Price'].mean()
median_price=df['Price'].median()
var_price=df['Price'].var()
std_price=df['Price'].std()


# In[171]:


# calculate mean , median, variance, standard  value of the price column

print(f"Mean Price:{mean_price}")
print(f"Median Price:{median_price}")
print(f"Variance Price:{var_price}")
print(f"Standard Price:{std_price}")


# In[176]:


#histogram/ price distribution plot 

plt.figure(figsize=(11,6))
sns.histplot(df['Price'], bins=20,kde=True)
plt.title('Price Distribution')
plt.show()


# In[250]:


#histogram/  brand distribution plot

plt.figure(figsize=(30,6))
sns.histplot(df['Brand_name'], bins=10,kde=True)
plt.title('brand Distribution')
plt.show()


# In[254]:


df['Product_Info']=df['Brand_name']+'- ₹' 
df['Product_Info']=df['Price_INR'].astype(str)


# In[255]:


df['Product_Info']


# In[256]:


df.rename(columns={'Brand Name':'Brand_name'},inplace= True)
df.rename(columns={'Price':'Price_INR'},inplace= True)


# In[257]:


print(df)


# In[258]:


print(df.describe())


# In[ ]:


# create boxplot to visualise of Price_INR in the DataFrame


# In[259]:


sns.boxplot(data=df,x='Price_INR')


# In[260]:


# plot style
sns.set(style='whitegrid')


# In[261]:


plt.figure(figsize=(10,6))
sns.histplot(df['Price_INR'],kde=True,bins=15,color='green')
plt.title('Washing machines price distribution')
plt.xlabel('Price_INR')
plt.ylabel("frequency")
plt.show()


# In[262]:


# statistics summary for price
print('statistics summary for Price_INR')
print(df['Price_INR'].describe())


# In[263]:


# bivariate analysis - price vs brand

plt.figure(figsize=(10,6))
sns.boxplot(x='Brand_name',y='Price_INR',data=df)
#adding title and labels
plt.xticks(rotation=90)
plt.title('Price distribution by Brand')
plt.xlabel('Brand_Name')
plt.ylabel('Price_INR')
plt.show()


# In[268]:


# average price barchart
Brand_avg_price=df.groupby("Brand_name")['Price_INR'].mean().sort_values(ascending=False)


# plotting bar chart
plt.figure(figsize=(10,6))
sns.barplot(x=Brand_avg_price.index,y=Brand_avg_price.values,palette='viridis')


#adding tilte and labels
plt.title("Average Price by Brand",fontsize=16)
plt.xlabel('Brand_name',fontsize=12)
plt.ylabel('Average Price (INR)',fontsize=12)
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
plt.show()


# In[271]:


# lowest price barchart
Brand_lowest_price=df.groupby("Brand_name")['Price_INR'].mean().sort_values(ascending=False)


# plotting bar chart
plt.figure(figsize=(12,6))
sns.barplot(x=Brand_avg_price.index,y=Brand_avg_price.values,palette='viridis')


#adding tilte and labels
plt.title("lowest Price by Brand",fontsize=16)
plt.xlabel('Brand_name',fontsize=12)
plt.ylabel('lowest Price (INR)',fontsize=12)
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
plt.show()


# In[272]:


# highest price barchart
Brand_highest_price=df.groupby("Brand_name")['Price_INR'].mean().sort_values(ascending=False)


# plotting bar chart
plt.figure(figsize=(12,6))
sns.barplot(x=Brand_avg_price.index,y=Brand_avg_price.values,palette='viridis')


#adding tilte and labels
plt.title("Highest Price by Brand",fontsize=16)
plt.xlabel('Brand_name',fontsize=12)
plt.ylabel('Highest Price (INR)',fontsize=12)
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




