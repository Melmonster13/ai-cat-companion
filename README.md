# ai-cat-companion
Gamified AI cat companion that evolves as an ML agent learns cat behavior.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Regenerating Models
Trained model files (`.pkl`) are not committed to this repo. To regenerate them, run the notebooks in order from the `notebooks/` directory:

1. `01_data_generation.ipynb` — generates the synthetic dataset
2. `02_eda_pandas.ipynb` — cleans and explores the data
3. `03_model_training.ipynb` — trains models and saves artifacts to `artifacts/models/`

## Project Structure
- `src/data/` — data generation and preprocessing
- `src/models/` — training, evaluation, and inference modules
- `notebooks/` — documented Jupyter notebooks for each phase
- `data/raw/` — synthetic cat behavior dataset
- `data/processed/` — cleaned dataset
- `artifacts/` — generated locally only (models, figures, logs)
