from . import adzuna_get, json_to_df, df_to_html


def main():

    results = adzuna_get.fetch_jobs()
    df = json_to_df.convert_to_df(results.json())
    df_to_html.df_to_html(df)


if __name__ == "__main__":
    main()