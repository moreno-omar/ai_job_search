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
    cols = df.columns.tolist()
    cols.remove("company_display_name")
    cols.remove("title")
    cols.remove("salary_min")
    cols.remove("redirect_url")
    cols.remove("description")

    new_order = ["company_display_name", "title", "salary_min"] + cols + ["redirect_url", "description"]
    df = df.reindex(columns=new_order) 
    return df