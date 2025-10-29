def sanitizer(df):
    df = df.copy()
    
    df.columns = [c.lower() for c in df.columns]
    
 #   for col in ["policy_sales_channel", "region_code"]:
 #       if col in df.columns:
 #           df[col] = df[col].astype("Int64")
 #   return df

    cols_int = ['id', 'Age', 'Driving_License',
                'Region_Code', 'Previously_Insured',
                'Annual_Premium', 'Policy_Sales_Channel', 'Vintage']

    cols_str = ['Gender', 'Vehicle_Age', 'Vehicle_Damage']

    for col in cols_int:
        df[col] = pd.to_numeric(df[col], errors='coerce').round().astype('Int64')

    for col in cols_str:
        df[col] = df[col].astype(str).str.strip()
        