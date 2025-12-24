import pandas as pd

def initialize_data(session_state, initial_df):
    if "sales_data" not in session_state:
        session_state.sales_data = initial_df.copy()

def add_sale(session_state, new_sale):
    session_state.sales_data = pd.concat(
        [session_state.sales_data, pd.DataFrame([new_sale])],
        ignore_index=True
    )

def get_data(session_state):
    return session_state.sales_data
