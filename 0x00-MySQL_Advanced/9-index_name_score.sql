-- This script creates an index idx_name_first_score
-- On the table names and the first letter of name
-- And the score

CREATE INDEX idx_name_first_score
ON names(name(1), score);
