"""
Data Cleaning Pipeline
====================================================
Goal: Combine 5 years of school incident report files (mix of .xlsx and .csv,
with inconsistent column structures across years) into a single clean
dataframe, ready for SQL/analysis.

The overall approach:
1. Load every year's files.
2. Standardise each dataframe to match the 2020 file's column structure
   (chosen as the reference schema since it's the cleanest/most complete).
3. Combine everything into one dataframe.
4. Fix two known data quality issues discovered during cleaning:
     - "Connected Communities Team 1/2/3" being treated as 3 separate
       Operational Directorates instead of 1.
     - Principal Network Names mapping to more than one Operational
       Directorate, caused by NSW restructuring directorates from 2020
       onward. Fixed using 2023 (the most recent, standardised year) as
       the source of truth for the correct network -> directorate mapping.
5. Export the cleaned result to a new CSV.
"""

import pandas as pd


# ============================================================
# STEP 1: Load 2019 (split across 2 files) and 2020 (reference schema)
# ============================================================
# 2019 was reported in two halves (Term 1&2, Term 3&4) as separate Excel
# files. 2020 is loaded first too, because its column structure will be
# used as the "target" schema that every other year gets standardised to.

df_2019_1 = pd.read_excel('final-redacted-reports-term-1-and-2-2019.xlsx', sheet_name='Sheet1')
df_2019_2 = pd.read_excel('final-redacted-reports-term-3-and-4-2019.xlsx', sheet_name='Sheet1')
df_2020_1 = pd.read_csv('2020-biannual-one-incident-report.csv')


# ============================================================
# STEP 2: Compare column structures across the three files
# ============================================================
# Lines up each dataframe's column list side by side so mismatches
# (missing columns, extra columns, renamed columns) can be spotted visually
# before writing any cleaning code.

comparison = pd.DataFrame({
    'df_2019_1': pd.Series(df_2019_1.columns),
    'df_2019_2': pd.Series(df_2019_2.columns),
    'df_2020_1': pd.Series(df_2020_1.columns)
})
comparison


# ============================================================
# STEP 3: Standardise df_2019_1 to match the 2020 schema
# ============================================================
# df_2019_1 has 3 extra columns that don't exist in 2020's structure
# (Case Record Type, Date of Incident, Time of Incident) and is missing
# 'Secondary Category'. These are dropped since they're redundant/unused
# once 'Date/Time Opened' already exists in this file.

df_2019_1 = df_2019_1.drop(columns=['Case Record Type'])
df_2019_1 = df_2019_1.drop(columns=['Date of Incident'])
df_2019_1 = df_2019_1.drop(columns=['Time of Incident'])

# Missing column added as empty, so it exists for the later concat.
df_2019_1['Secondary Category'] = None


# ============================================================
# STEP 4: Standardise df_2019_2 to match the 2020 schema
# ============================================================
# df_2019_2 doesn't have a 'Date/Time Opened' column, but has an
# equivalent 'Date of Incident' column instead - renamed to match.
# It's also missing 'Secondary Category' and 'Incident Priority Rating',
# both added as empty columns.

df_2019_2 = df_2019_2.rename(columns={'Date of Incident': 'Date/Time Opened'})
df_2019_2['Secondary Category'] = None
df_2019_2['Incident Priority Rating'] = None


# ============================================================
# STEP 5: Strip whitespace from column names
# ============================================================
# Column names from Excel/CSV exports sometimes carry invisible leading
# or trailing whitespace, which causes column matching/renaming to
# silently fail. Stripped here before reordering, to guarantee an exact
# match against df_2020_1's column names.

df_2019_1.columns = df_2019_1.columns.str.strip()
df_2019_2.columns = df_2019_2.columns.str.strip()
df_2020_1.columns = df_2020_1.columns.str.strip()


# ============================================================
# STEP 6: Reorder 2019 columns to match the 2020 reference order
# ============================================================
# Column order doesn't strictly matter for pd.concat(), but keeping it
# consistent makes the data easier to sanity-check visually and avoids
# relying on pandas to auto-align columns by name.

df_2019_1 = df_2019_1[df_2020_1.columns]
df_2019_2 = df_2019_2[df_2020_1.columns]


# ============================================================
# STEP 7: Combine both halves of 2019 into a single dataframe
# ============================================================

df_2019 = pd.concat([df_2019_1, df_2019_2], ignore_index=True)


# ============================================================
# STEP 8: Load the remaining years (2020-2023)
# ============================================================
# Note: some files threw a UnicodeDecodeError when read with the default
# utf-8 encoding (e.g. 'utf-8' codec can't decode byte 0xff...). This
# happens when a file was saved with a different encoding (commonly
# Windows-1252/Latin-1) rather than UTF-8. Fixed by explicitly passing
# encoding='latin1' for the affected files.

df_2020_2 = pd.read_csv('2020-biannual-two-incident-report.csv')
df_2021_1 = pd.read_csv('2021-biannual-one-incident-report.csv')
df_2021_2 = pd.read_csv('2021-biannual-two-incident-report.csv')
df_2022_1 = pd.read_csv('2022-biannual-one-incident-report-summary-1.csv', encoding='latin1')
df_2022_2 = pd.read_csv('2022-biannual-two-incident-report-summary-1.csv')
df_2023_1 = pd.read_csv('2023-biannual-one-incident-report.csv', encoding='latin1')
df_2023_2 = pd.read_csv('2023-biannual-two-incident-report.csv')


# ============================================================
# STEP 9: Strip whitespace from column names across every dataframe
# ============================================================
# Repeats the Step 5 cleanup, but now across all 9 dataframes at once
# using a loop, since every file could independently have the same
# whitespace issue.

dfs = [
    df_2019,
    df_2020_1,
    df_2020_2,
    df_2021_1,
    df_2021_2,
    df_2022_1,
    df_2022_2,
    df_2023_1,
    df_2023_2
]

for df in dfs:
    df.columns = df.columns.str.strip()


# ============================================================
# STEP 10: Verify every dataframe now shares an identical schema
# ============================================================
# Prints each dataframe's columns for a manual visual check, then runs
# an automated check confirming every dataframe's columns exactly match
# the first one. This must return True before it's safe to concatenate
# everything - otherwise pd.concat() would silently introduce NaNs or
# misaligned columns for any dataframe that doesn't match.

for i, df in enumerate(dfs):
    print(f"Dataframe {i}:")
    print(df.columns.tolist())
    print()

all(df.columns.equals(dfs[0].columns) for df in dfs)  # result: True


# ============================================================
# STEP 11: Combine all years (2019-2023) into one dataframe
# ============================================================

school_project = pd.concat(dfs, ignore_index=True)


# ============================================================
# STEP 12: Fix issue #1 - duplicate "Connected Communities" directorates
# ============================================================
# 'Operational Directorate' contained 'Connected Communities Team 1',
# 'Team 2', and 'Team 3' as three separate values, when they should all
# represent the same directorate. Regex replace collapses all three
# variants down to a single consistent 'Connected Communities' value.

school_project["Operational Directorate"] = school_project["Operational Directorate"].replace(
    r"Connected Communities Team \d+",
    "Connected Communities",
    regex=True
)


# ============================================================
# STEP 13: Remove duplicate rows
# ============================================================
# Note: drop_duplicates() is used a few more times further down in this
# script, but for a different purpose each time - here it removes
# duplicate incident rows from the full dataset, whereas later uses
# deduplicate network/directorate pairs when building or checking a
# lookup table (not the same as removing duplicate incidents).

school_project.drop_duplicates(inplace=True)


# ============================================================
# STEP 14: Identify issue #2 - networks mapped to multiple directorates
# ============================================================
# Groups by Principal Network Name and checks how many distinct
# Operational Directorate values each network has. In a clean dataset
# this should always be 1 (a school network belongs to exactly one
# directorate) - any network with more than 1 is flagged as a conflict
# to investigate.

conflicts = school_project.groupby('Principal Network Name')['Operational Directorate'].unique().reset_index()
conflicts = conflicts[conflicts['Operational Directorate'].apply(len) > 1]

print("\nNETWORKS WITH DIRECTORATE CONFLICTS (FIX TARGETS):")
for _, row in conflicts.iterrows():
    print(f"\n- {row['Principal Network Name']}")
    for directorate in row['Operational Directorate']:
        print(f"  -> {directorate}")

# ROOT CAUSE FOUND: NSW restructured Operational Directorates starting in
# 2020, so the same Principal Network Name can appear under a different
# (older, now-incorrect) directorate in pre-2020/early data. Fixed below
# by using the 2023 file - the most recent, standardised year - as the
# source of truth for the correct network -> directorate mapping.


# ============================================================
# STEP 15: Fix issue #2 - remap Operational Directorate using 2023 as reference
# ============================================================

# 15a. Keep a backup of the original column before overwriting anything,
# so the fix can be verified/rolled back if needed.
school_project['Operational Directorate_original'] = school_project['Operational Directorate']

# 15b. Confirm 2023 itself has a clean 1-to-1 network -> directorate
# mapping before trusting it as the reference (otherwise this would just
# reintroduce the same conflict problem).
check_2023 = df_2023_1.groupby('Principal Network Name')['Operational Directorate'].nunique()
print(check_2023[check_2023 > 1])  # should be empty

# 15c. Build a {network: directorate} lookup dictionary from 2023.
network_to_directorate = (
    df_2023_1[['Principal Network Name', 'Operational Directorate']]
    .drop_duplicates()
    .set_index('Principal Network Name')['Operational Directorate']
    .to_dict()
)

# 15d. Check for networks in the full dataset that 2023 has no record of
# (e.g. renamed, merged, or discontinued networks). These need manual
# review before the mapping is applied, since .map() would otherwise
# silently turn them into NaN.
combined_networks = set(school_project['Principal Network Name'].unique())
mapped_networks = set(network_to_directorate.keys())
missing_from_mapping = combined_networks - mapped_networks
print(missing_from_mapping)

# Investigation found two unresolved cases, deliberately left as-is
# rather than guessed:
#   - NaN: rows with no Principal Network Name recorded at all, so there
#     is nothing to map from.
#   - 'Macquarie': found to be an ambiguous legacy name covering two
#     unrelated modern networks in different regions - 'Lake Macquarie
#     North/West/East' (maps to 'Regional North') and
#     'Wambuul-Macquarie' (maps to 'Regional North and West') - as well
#     as an unexplained third value, 'Rural South and West'. Since there
#     is no reliable way to tell which modern network an old 'Macquarie'
#     row belongs to, it is left unresolved rather than assigned a guess.
unresolved = (
    school_project['Principal Network Name'].isna() |
    (school_project['Principal Network Name'] == 'Macquarie')
)

# 15e. Apply the 2023-based mapping to every row.
school_project['Operational Directorate'] = school_project['Principal Network Name'].map(network_to_directorate)

# 15f. Restore the original (pre-fix) value specifically for the two
# unresolved cases above, since .map() would have otherwise overwritten
# them with NaN.
school_project.loc[unresolved, 'Operational Directorate'] = school_project.loc[unresolved, 'Operational Directorate_original']


# ============================================================
# STEP 16: Verify the fix
# ============================================================

# No unexpected new NaNs introduced outside the known unresolved rows.
still_nan = school_project[school_project['Operational Directorate'].isna() & ~unresolved]
print(len(still_nan))  # expect 0

# Every network (excluding the two documented exceptions) now maps to
# exactly one directorate.
final_check = school_project[~unresolved].groupby('Principal Network Name')['Operational Directorate'].nunique()
print(final_check[final_check > 1])  # expect empty

# Every network/directorate pair in the cleaned data actually exists in
# the 2023 reference data (confirms nothing was mismatched).
combined_pairs = (
    school_project[~unresolved][['Principal Network Name', 'Operational Directorate']]
    .drop_duplicates()
    .sort_values('Principal Network Name')
    .reset_index(drop=True)
)
df_2023_pairs = (
    df_2023_1[['Principal Network Name', 'Operational Directorate']]
    .drop_duplicates()
    .sort_values('Principal Network Name')
    .reset_index(drop=True)
)
merged_check = combined_pairs.merge(
    df_2023_pairs,
    on=['Principal Network Name', 'Operational Directorate'],
    how='left',
    indicator=True
)
mismatches = merged_check[merged_check['_merge'] == 'left_only']
print(mismatches)  # expect empty


# ============================================================
# STEP 17: Drop the backup column and export the cleaned dataset
# ============================================================

school_project = school_project.drop(columns=['Operational Directorate_original'])

school_project.to_csv('school_project_cleaned.csv', index=False)

# Verify the export by reading it back in and comparing shape.
check_export = pd.read_csv('school_project_cleaned.csv')
print(check_export.shape)
print(school_project.shape)  # should match
