import pandas as pd

def convert_to_df(data: dict) -> pd.DataFrame:

    # Extract results array and normalize into DataFrame
    results = data.get("results", [])
    df = pd.json_normalize(results, sep="_")

    # Drop metadata-only and unnecessary columns
    columns_to_drop = [col for col in df.columns if col.endswith("__CLASS__")]
    columns_to_drop.extend(["latitude", "adref", "category_label", "category_tag", "location_area"])
    df = df.drop(columns=columns_to_drop, errors="ignore")

    # Reindex to rearrange columns: company first, then title, salary_min,
    # middle columns, then redirect_url and description at end
    all_cols = df.columns.tolist()
    front_columns = ["company_display_name", "title", "salary_min"]
    end_columns = ["redirect_url", "description"]

    # Middle columns are all columns except those explicitly placed at front or end
    middle_columns = [c for c in all_cols if c not in front_columns + end_columns]

    new_order = (
        [c for c in front_columns if c in all_cols]
        + middle_columns
        + [c for c in end_columns if c in all_cols]
    )
    df = df.reindex(columns=new_order)
    return df