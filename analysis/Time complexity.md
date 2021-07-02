Related to https://engineering.upside.com/a-beginners-guide-to-optimizing-pandas-code-for-speed-c09ef2c6a4d6

- Don't use parseTime as a 'converter' in the `pd.read_csv` call. Takes 8 times as long otherwise.
- Use json_parser as converter for the columns we need to use json.loads() on. Saves ~10% of time.
- Implementing custom value_counts().to_dict() is much faster if we can guarantee the identity of the values (which we can, in our case)
- get_group is much faster on groups that are slices of their parent dataframe:
    - So this:
    ```python
        grouped = df[[field1, field2]].groupby(field1)
        grouped.get_group(field1value)
    ```
    - will be considerably faster than this:
    ```python
        grouped = df.groupby(field1)
        grouped.get_group(field1value)
    ```