WITH message_summary AS (
    SELECT
        claim_id,
        COUNT(*) AS message_count,
        AVG(sentiment_score) AS avg_sentiment_score,
        AVG(response_latency_minutes) AS avg_response_latency_minutes,
        AVG(CASE WHEN escalation_flag = 1 THEN 1.0 ELSE 0.0 END) AS escalation_rate
    FROM synthetic_messages
    GROUP BY claim_id
)
SELECT
    c.claim_id,
    c.state,
    c.claim_type,
    f.reporting_channel,
    f.weather_condition,
    f.point_of_impact,
    f.police_report_flag,
    f.witness_flag,
    f.injury_reported_at_fnol,
    c.attorney_rep_flag,
    c.reserve_amount + c.paid_amount AS total_incurred,
    COALESCE(ms.message_count, 0) AS message_count,
    COALESCE(ms.avg_sentiment_score, 0.0) AS avg_sentiment_score,
    COALESCE(ms.avg_response_latency_minutes, 0.0) AS avg_response_latency_minutes,
    COALESCE(ms.escalation_rate, 0.0) AS escalation_rate,
    CASE
        WHEN f.injury_reported_at_fnol = 1
             OR c.attorney_rep_flag = 1
             OR COALESCE(ms.escalation_rate, 0.0) > 0.25
             OR COALESCE(ms.avg_sentiment_score, 0.0) < -0.25
        THEN 'HIGH_TOUCH'
        WHEN f.police_report_flag = 1
             OR f.witness_flag = 1
             OR COALESCE(ms.message_count, 0) >= 4
        THEN 'MODERATE'
        ELSE 'STANDARD'
    END AS fnol_triage_segment
FROM synthetic_claims c
JOIN synthetic_fnol f
    ON c.claim_id = f.claim_id
LEFT JOIN message_summary ms
    ON c.claim_id = ms.claim_id
ORDER BY total_incurred DESC, fnol_triage_segment DESC;

