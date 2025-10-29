import pandas as pd
import re
import unicodedata

# Liste aqui TODAS as colunas que o modelo precisa para funcionar
REQUIRED = [
    "Age",
    "Annual_Premium",
    "Vintage",
    "Driving_License",
    "Previously_Insured",
    "Region_Code",
    "Policy_Sales_Channel",
    "Vehicle_Age",
    "Vehicle_Damage",
    "Gender"
]

def _clean_header(s: str) -> str:
    """
    Remove caracteres invisíveis, espaços extras e normaliza Unicode.
    """
    s = unicodedata.normalize("NFKC", str(s))
    s = s.replace("\ufeff", "")   # BOM (Byte Order Mark)
    s = s.replace("\u200b", "")   # Zero-width space
    s = s.replace("\xa0", " ")    # NBSP → espaço comum
    s = re.sub(r"\s+", " ", s.strip())
    return s

def sanitizer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa cabeçalhos, valida colunas obrigatórias e ajusta tipos.
    """
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    # Copia para não alterar o original
    df = df.copy()

    # 1️⃣ Limpar nomes das colunas
    df.columns = [_clean_header(c) for c in df.columns]

    # 2️⃣ Validar colunas obrigatórias
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(
            "Missing required columns after header normalization: "
            + ", ".join(missing)
            + f". Received: {[repr(c) for c in df.columns]}"
        )

    # 3️⃣ Converter colunas numéricas para tipos corretos
    integer_like = [
        "Age",
        "Vintage",
        "Driving_License",
        "Previously_Insured",
        "Region_Code",
        "Policy_Sales_Channel",
        "Annual_Premium"
    ]

    float_like = []

    for col in integer_like:
        df[col] = pd.to_numeric(df[col], errors="coerce").round().astype("Int64")

    for col in float_like:
        df[col] = pd.to_numeric(df[col], errors="coerce")

#    # 4️⃣ Padronizar textos simples (opcional)
#    if "Vehicle_Damage" in df.columns:
#        df["Vehicle_Damage"] = (
#            df["Vehicle_Damage"].astype(str).str.strip().str.title()
#        )
#
#    if "Vehicle_Age" in df.columns:
#        df["Vehicle_Age"] = (
#            df["Vehicle_Age"].astype(str).str.strip().replace({
#                "<1": "< 1 Year",
#                "< 1": "< 1 Year",
#                "1-2": "1-2 Year",
#                "1 to 2": "1-2 Year",
#                ">2": "> 2 Years",
#                "> 2": "> 2 Years"
#            })
#        )
#
#    if "Gender" in df.columns:
#        df["Gender"] = (
#            df["Gender"].astype(str).str.strip().str.title()
#        )
#
#    return df
