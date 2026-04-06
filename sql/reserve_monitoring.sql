SELECT
    c.state,
    c.claim_type,
    c.bodily_injury_flag,
    c.attorney_rep_flag,
    COUNT(*) AS open_claims,
    SUM(c.reserve_amount) AS total_open_reserve,
    AVG(c.reserve_amount) AS avg_open_reserve,
    AVG(c.paid_amount) AS avg_paid_amount,
    AVG(
        CASE
            WHEN c.reserve_amount > 0 THEN c.paid_amount / c.reserve_amount
            ELSE NULL
        END
    ) AS avg_paid_to_reserve_ratio
FROM synthetic_claims c
WHERE c.closed_flag = 0
GROUP BY
    c.state,
    c.claim_type,
    c.bodily_injury_flag,
    c.attorney_rep_flag
ORDER BY total_open_reserve DESC;

