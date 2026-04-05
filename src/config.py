from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
DOCS_DIR = BASE_DIR / "docs"

CLAIMS_FILE = RAW_DIR / "synthetic_claims.csv"
FNOL_FILE = RAW_DIR / "synthetic_fnol.csv"
MESSAGES_FILE = RAW_DIR / "synthetic_messages.csv"
POLICY_FILE = RAW_DIR / "synthetic_policy.csv"

ANALYTICAL_BASE_TABLE_FILE = PROCESSED_DIR / "analytical_base_table.csv"
MODEL_RESULTS_FILE = PROCESSED_DIR / "model_results.json"

RANDOM_SEED = 42
DEFAULT_CLAIM_COUNT = 1500

STATES = ["CA", "TX", "FL", "NV", "AZ", "GA"]
CLAIM_TYPES = ["collision_pd", "rear_end_bi", "side_impact_bi", "minor_pd", "mixed_injury"]
REPORTING_CHANNELS = ["phone", "mobile_app", "web_portal", "agent"]
LOSS_LOCATIONS = ["urban_arterial", "highway", "residential_street", "parking_lot", "intersection"]
WEATHER_CONDITIONS = ["clear", "rain", "fog", "wind", "night_clear"]
POINTS_OF_IMPACT = ["rear_end", "front_end", "left_side", "right_side", "multi_point"]
LIABILITY_DECISIONS = ["insured_at_fault", "comparative_negligence", "not_at_fault", "under_investigation"]
RISK_TIERS = ["tier_1", "tier_2", "tier_3", "tier_4"]
