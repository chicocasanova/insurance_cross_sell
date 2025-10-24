def sanitizer(df):
    df = df.copy()
    df.columns = [c.lower() for c in df.columns]
    for col in ["policy_sales_channel", "region_code"]:
        if col in df.columns:
            df[col] = df[col].astype("Int64")
    return df