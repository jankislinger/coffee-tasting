import polars as pl


def main() -> None:
    data = pl.DataFrame(
        [
            ("Ethiopia", "La boheme", 499, 7.3),
            ("Kenya", "Mama coffee", 299, 8.3),
            ("Start", "Doubleshot", 319, 4.5),
        ],
        schema=["Coffee", "Roastery", "Price", "Rating"],
        orient="row",
    ).with_columns(pl.col("Rating").map_elements(str_bar, return_dtype=pl.String))

    md_config = pl.Config(
        tbl_formatting="MARKDOWN",
        tbl_hide_column_data_types=True,
        tbl_hide_dataframe_shape=True,
        fmt_str_lengths=44,
        apply_on_context_enter=True,
    )

    with md_config:
        print(data)


def str_bar(value: float) -> str:
    width = 40
    k1 = num_chars(value, 10.0, width)
    k2 = width - k1
    return "=" * k1 + " " * k2 + str(value)


def num_chars(value: float, max_val: float, max_chars: int) -> int:
    value = value * (max_chars + 1) / max_val
    if value >= max_chars:
        return max_chars
    return int(value)


if __name__ == "__main__":
    main()
