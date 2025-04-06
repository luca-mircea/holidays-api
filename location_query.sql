WITH holiday_location_selection AS (
    SELECT
        *
    FROM holidays
    LEFT JOIN locations
    ON holidays.country = locations.country_code
    UNION ALL
    SELECT
        *
    FROM holidays
    LEFT JOIN locations
    ON holidays.subdivisions = locations.subdivision_code
)

SELECT *
FROM holiday_location_selection
WHERE location_id = '9415913d-fffa-41f9-9323-6d62e6100a31'
AND observed_string >= '2024-01-01'
AND observed_string <= '2024-02-01'
