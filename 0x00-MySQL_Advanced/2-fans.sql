-- This script ranks country origins of bands
-- Ordered by the number of (non-unique) fans

SELECT origin, SUM(fans) AS num_fans
FROM metal_bands
GROUP BY origin
ORDER BY num_fans DESC;
