WITH claim_base AS (
    SELECT
        c.claim_id,
        c.state,
        c.claim_type,
        c.bodily_injury_flag,
        c.attorney_rep_flag,
        c.closed_flag,
        c.reserve_amount,
        c.paid_amount,
        c.reserve_amount + c.paid_amount AS total_incurred,
        c.days_to_close,
        DATEDIFF(day, c.loss_date, c.report_date) AS report_lag_days
    FROM synthetic_claims c
)
SELECT
    state,
    claim_type,
    COUNT(*) AS claim_count,
    AVG(total_incurred) AS avg_total_incurred,
    AVG(CASE WHEN bodily_injury_flag = 1 THEN 1.0 ELSE 0.0 END) AS bi_rate,
    AVG(CASE WHEN attorney_rep_flag = 1 THEN 1.0 ELSE 0.0 END) AS attorney_rep_rate,
    AVG(CASE WHEN closed_flag = 1 THEN 1.0 ELSE 0.0 END) AS closure_rate,
    AVG(days_to_close) AS avg_days_to_close,
    AVG(report_lag_days) AS avg_report_lag_days
FROM claim_base
GROUP BY state, claim_type
ORDER BY avg_total_incurred DESC;

