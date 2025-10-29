import pandas as pd
import re
import unicodedata

# canônicos que seu pipeline espera (ajuste conforme seu modelo)
REQUIRED = ["Age", "Annual_Premium", "Vintage"]  # acrescente os demais

# aliases para tolerar variações comuns que vêm do Sheets/CSV
ALIASES = {
    "Age": ["age", "idade"],
    "Annual_Premium": ["annual_premium", "annual premium", "prêmio anual", "premio anual"],
    "Vintage": ["vintage", "dias_cliente", "dias como cliente"],
    # ... complete para todas as features que o pipeline usa
}

def _clean_header(s: str) -> str:
    s = unicodedata.normalize("NFKC", str(s))
    s = s.replace("\ufeff", "")   # BOM
    s = s.replace("\u200b", "")   # zero-width space
    s = s.replace("\xa0", " ")    # NBSP -> espaço normal
    s = re.sub(r"\s+", " ", s.strip())
    return s

def _apply_aliases(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # primeiro limpa todos os headers
    cleaned = [_clean_header(c) for c in df.columns]
    df.columns = cleaned

    # cria mapa normalizado -> original
    norm2orig = { _clean_header(c).lower(): c for c in df.columns }

    renames = {}
    for canonical, variants in ALIASES.items():
        for cand in [canonical] + variants:
            key = _clean_header(cand).lower()
            if key in norm2orig:
                renames[norm2orig[key]] = canonical
                break  # achou um, segue pro próximo canônico
    if renames:
        df = df.rename(columns=renames)
    return df

def sanitizer(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    df = _apply_aliases(df)

    # erro descritivo se faltar algo
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        # log útil para debug: mostra cabeçalhos recebidos com repr()
        raise ValueError(
            f"Missing required columns after header normalization: {missing}. "
            f"Received columns: {[repr(c) for c in df.columns]}"
        )

    # coerções (só mexe se a coluna existir)
    integer_like = ["Age", "Vintage"]
    float_like   = ["Annual_Premium"]

    for col in integer_like:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").round().astype("Int64")

    for col in float_like:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
