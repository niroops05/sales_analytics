import pandas as pd

def prepare_month_column(df):
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M").astype(str)
    return df

def calculate_kpis(df):
    total_revenue = df["Revenue"].sum()
    best_product = df.groupby("Product")["Revenue"].sum().idxmax()
    best_region = df.groupby("Region")["Revenue"].sum().idxmax()
    return total_revenue, best_product, best_region

def monthly_trend(df):
    return df.groupby("Month")["Revenue"].sum().reset_index()

def product_performance(df):
    return df.groupby("Product")["Revenue"].sum().reset_index()

def region_performance(df):
    return df.groupby("Region")["Revenue"].sum().reset_index()
