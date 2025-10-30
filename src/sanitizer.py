import pandas as pd

def sanitizer(df):
    df = df.copy()
    
    df.columns = [c.lower() for c in df.columns]
    
 #   for col in ["policy_sales_channel", "region_code"]:
 #       if col in df.columns:
 #           df[col] = df[col].astype("Int64")
 #   return df

    cols_int = ['id', 'age', 'driving_license', 'region_code',
            	'previously_insured', 'annual_premium',
            	'policy_sales_channel', 'vintage']

    cols_str = ['gender', 'vehicle_age', 'vehicle_damage']

    for col in cols_int:
        df[col] = pd.to_numeric(df[col], errors='coerce').round().astype('Int64')

    for col in cols_str:
        df[col] = df[col].astype(str).str.strip()

    return df
        