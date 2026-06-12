# Recommended Final Kaggle Upload Structure

```
dataset/
├── raw/
│   └── (Original scraped JSONs: all_egypt.json, etc.)
├── processed/
│   └── (Cleaned CSV/Parquet files used for training)
├── models/
│   └── (Final pickled models or CatBoost info, if any)
├── docs/
│   └── data_dictionary.md
├── dataset-metadata.json
└── README.md
```
