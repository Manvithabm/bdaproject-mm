-- Hive script for comprehensive crop yield trend analysis

-- Create external table for cleaned yield data
CREATE EXTERNAL TABLE IF NOT EXISTS crop_yield (
    crop TEXT,
    year INT,
    yield FLOAT,
    temperature FLOAT,
    rainfall FLOAT,
    soil_type TEXT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SKIP.HEADER.LINE.COUNT=1
LOCATION '/crop_yield/cleaned';

-- Query 1: Average yield by crop with statistics
SELECT 
    crop,
    COUNT(*) as record_count,
    ROUND(AVG(yield), 2) as avg_yield,
    ROUND(MIN(yield), 2) as min_yield,
    ROUND(MAX(yield), 2) as max_yield,
    ROUND(STDDEV_POP(yield), 2) as stddev_yield
FROM crop_yield
GROUP BY crop
ORDER BY avg_yield DESC;

-- Query 2: Yield trends over years with growth analysis
SELECT 
    year,
    COUNT(*) as record_count,
    ROUND(AVG(yield), 2) as avg_yield,
    ROUND(SUM(yield), 2) as total_yield,
    ROUND(AVG(temperature), 2) as avg_temp,
    ROUND(AVG(rainfall), 2) as avg_rainfall
FROM crop_yield
GROUP BY year
ORDER BY year;

-- Query 3: Impact of temperature on yield
SELECT 
    ROUND(temperature, 1) as temp_range,
    COUNT(*) as record_count,
    ROUND(AVG(yield), 2) as avg_yield,
    ROUND(MIN(yield), 2) as min_yield,
    ROUND(MAX(yield), 2) as max_yield
FROM crop_yield
WHERE temperature IS NOT NULL
GROUP BY ROUND(temperature, 1)
ORDER BY temp_range;

-- Query 4: Impact of rainfall on yield
SELECT 
    ROUND(rainfall / 100) * 100 as rainfall_range,
    COUNT(*) as record_count,
    ROUND(AVG(yield), 2) as avg_yield,
    ROUND(MIN(yield), 2) as min_yield,
    ROUND(MAX(yield), 2) as max_yield
FROM crop_yield
WHERE rainfall IS NOT NULL
GROUP BY ROUND(rainfall / 100)
ORDER BY rainfall_range;

-- Query 5: Performance by soil type
SELECT 
    soil_type,
    COUNT(*) as record_count,
    ROUND(AVG(yield), 2) as avg_yield,
    ROUND(AVG(temperature), 2) as avg_temp,
    ROUND(AVG(rainfall), 2) as avg_rainfall
FROM crop_yield
WHERE soil_type IS NOT NULL
GROUP BY soil_type
ORDER BY avg_yield DESC;

-- Query 6: Top performing crops by year
SELECT 
    year,
    crop,
    ROUND(AVG(yield), 2) as avg_yield,
    ROW_NUMBER() OVER (PARTITION BY year ORDER BY AVG(yield) DESC) as rank
FROM crop_yield
GROUP BY year, crop
HAVING ROW_NUMBER() OVER (PARTITION BY year ORDER BY AVG(yield) DESC) <= 5;

-- Query 7: Correlation between climate factors and yield
SELECT 
    crop,
    year,
    ROUND(AVG(temperature), 2) as avg_temperature,
    ROUND(AVG(rainfall), 2) as avg_rainfall,
    ROUND(AVG(yield), 2) as avg_yield
FROM crop_yield
GROUP BY crop, year
ORDER BY crop, year;

-- Query 8: Year-over-year yield comparison
SELECT 
    crop,
    year,
    ROUND(AVG(yield), 2) as avg_yield,
    LAG(AVG(yield)) OVER (PARTITION BY crop ORDER BY year) as prev_year_yield,
    ROUND(AVG(yield) - LAG(AVG(yield)) OVER (PARTITION BY crop ORDER BY year), 2) as yoy_change
FROM crop_yield
GROUP BY crop, year
ORDER BY crop, year;