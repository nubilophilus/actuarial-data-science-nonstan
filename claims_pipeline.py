from __future__ import annotations

from .config import ANALYTICAL_BASE_TABLE_FILE, MODEL_RESULTS_FILE, PROCESSED_DIR, RAW_DIR
from .data_cleaning import clean_datasets
from .data_generation import generate_synthetic_insurance_data, save_synthetic_datasets
from .data_ingestion import load_datasets
from .feature_engineering import build_analytical_base_table
from .modeling_liability import train_bodily_injury_model
from .modeling_severity import train_claim_severity_model
from .utils import ensure_directories, write_json


def run_pipeline() -> dict[str, object]:
    ensure_directories([RAW_DIR, PROCESSED_DIR])

    synthetic_bundle = generate_synthetic_insurance_data()
    save_synthetic_datasets(synthetic_bundle)

    datasets = load_datasets()
    cleaned_datasets = clean_datasets(datasets)
    analytical_base = build_analytical_base_table(cleaned_datasets)
    analytical_base.to_csv(ANALYTICAL_BASE_TABLE_FILE, index=False)

    severity_results = train_claim_severity_model(analytical_base)
    liability_results = train_bodily_injury_model(analytical_base)

    results_payload = {
        "severity_model": {
            "features": severity_results["features"],
            "metrics": severity_results["metrics"],
            "interpretation": severity_results["feature_interpretation"],
        },
        "bodily_injury_model": {
            "features": liability_results["features"],
            "metrics": liability_results["metrics"],
            "interpretation": liability_results["feature_interpretation"],
        },
        "row_counts": {
            "claims": int(len(cleaned_datasets["claims"])),
            "fnol": int(len(cleaned_datasets["fnol"])),
            "messages": int(len(cleaned_datasets["messages"])),
            "policy": int(len(cleaned_datasets["policy"])),
            "analytical_base_table": int(len(analytical_base)),
        },
    }
    write_json(results_payload, MODEL_RESULTS_FILE)
    return results_payload


def main() -> None:
    results = run_pipeline()
    print("Pipeline completed successfully.")
    print(results)


if __name__ == "__main__":
    main()

