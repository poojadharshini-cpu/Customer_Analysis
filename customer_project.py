#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[8]:


# Load dataset
df = pd.read_excel(r"C:\Users\Lenovo\Downloads\Data Analytics (DM)\customer.xlsx", sheet_name='customer')


# In[6]:


get_ipython().system('pip install openpyxl')


# In[9]:


# Check structure and missing values
print("--- Dataset Info ---")
print(df.info())
print("\n--- Missing Values Audit ---")
print(df.isnull().sum())


# In[10]:


# Feature Engineering: Total Revenue and Age Groups
df['total_revenue'] = df['quantity'] * df['price']

def categorize_age(age):
    if 18 <= age <= 30:
        return '18-30 (Young Adults)'
    elif 31 <= age <= 50:
        return '31-50 (Middle-Aged)'
    elif 51 <= age <= 70:
        return '51-70 (Seniors)'
    else:
        return 'Other'

df['age_group'] = df['age'].apply(categorize_age)
print("\nData successfully prepared with Total Revenue and Age Groups!")


# In[11]:


# Gender Summary
gender_summary = df.groupby('gender').agg(
    total_transactions=('invoice_no', 'count'),
    total_quantity=('quantity', 'sum'),
    total_revenue=('total_revenue', 'sum')
).reset_index()

print("=== GENDER SUMMARY ===")
print(gender_summary)


# In[12]:


# Age Group Summary
age_summary = df.groupby('age_group').agg(
    total_transactions=('invoice_no', 'count'),
    total_quantity=('quantity', 'sum'),
    total_revenue=('total_revenue', 'sum')
).reset_index()

print("\n=== AGE GROUP SUMMARY ===")
print(age_summary)


# In[13]:


# Payment Method Summary
payment_summary = df.groupby('payment_method').agg(
    total_transactions=('invoice_no', 'count'),
    total_revenue=('total_revenue', 'sum')
).reset_index()

print("=== PAYMENT METHOD SUMMARY ===")
print(payment_summary)


# In[15]:


import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(14, 5))

# Chart 1: Revenue by Gender & Category
plt.subplot(1, 2, 1)
cat_gender = df.groupby(['category', 'gender'])['total_revenue'].sum().unstack()
cat_gender.plot(kind='bar', ax=plt.gca(), colormap='viridis')
plt.title('Revenue by Product Category & Gender')
plt.xlabel('Product Category')
plt.ylabel('Total Revenue (TL)')
plt.xticks(rotation=45)

# Chart 2: Revenue by Age Group
plt.subplot(1, 2, 2)
age_rev = df.groupby('age_group')['total_revenue'].sum()
age_rev.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Revenue Share by Age Group')
plt.ylabel('')

plt.tight_layout()
plt.savefig('project_charts.png', dpi=300)
plt.show()
print("The charts are generated")


# In[17]:


df['total_revenue'] = df['quantity'] * df['price']
df['invoice_date'] = pd.to_datetime(df['invoice_date'])

# 1. Total Sales and Revenue by Category
category_performance = df.groupby('category').agg(
    total_units_sold=('quantity', 'sum'),
    total_revenue_tl=('total_revenue', 'sum'),
    transaction_count=('invoice_no', 'count')
).sort_values(by='total_units_sold', ascending=False)

print("=== CATEGORY PERFORMANCE SUMMARY ===")
print(category_performance)

# 2. Monthly Demand Trend for Categories
df['month'] = df['invoice_date'].dt.month_name()
monthly_demand = df.groupby(['month', 'category'])['quantity'].sum().unstack(fill_value=0)
print("\n=== MONTHLY DEMAND TREND ===")
print(monthly_demand[['Clothing', 'Shoes', 'Cosmetics', 'Technology']])


# In[ ]:




