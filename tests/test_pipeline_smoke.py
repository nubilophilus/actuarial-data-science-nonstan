from src.data_cleaning import clean_datasets
from src.data_generation import generate_synthetic_insurance_data
from src.feature_engineering import build_analytical_base_table
from src.modeling_liability import train_bodily_injury_model
from src.modeling_severity import train_claim_severity_model


def test_end_to_end_modeling_smoke() -> None:
    bundle = generate_synthetic_insurance_data(claim_count=300, random_seed=7)
    datasets = {
        "claims": bundle.claims,
        "fnol": bundle.fnol,
        "messages": bundle.messages,
        "policy": bundle.policy,
    }

    cleaned = clean_datasets(datasets)
    analytical_base = build_analytical_base_table(cleaned)

    assert len(analytical_base) == 300
    assert "total_incurred" in analytical_base.columns
    assert analytical_base["claim_id"].nunique() == 300

    severity_results = train_claim_severity_model(analytical_base)
    liability_results = train_bodily_injury_model(analytical_base)

    assert severity_results["metrics"]["test"]["rmse"] >= 0
    assert 0 <= liability_results["metrics"]["test"]["roc_auc"] <= 1

