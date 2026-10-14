-- Média de temperatura por dispositivo e por ambiente (interno ou externo).
-- O dataset tem um único dispositivo ("Room Admin"), então separar por ambiente
-- é o que deixa a comparação útil.
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT device_id,
       ambiente,
       ROUND(AVG(temperature), 2) AS avg_temp,
       COUNT(*)                   AS total_leituras
FROM temperature_readings
GROUP BY device_id, ambiente;

-- Quantas leituras o sensor registrou em cada hora do dia (0 a 23).
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM noted_at)::int AS hora,
       COUNT(*)                         AS contagem
FROM temperature_readings
GROUP BY 1
ORDER BY 1;

-- Temperatura máxima, mínima e média de cada dia.
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT noted_at::date               AS data,
       MAX(temperature)             AS temp_max,
       MIN(temperature)             AS temp_min,
       ROUND(AVG(temperature), 2)   AS temp_media
FROM temperature_readings
GROUP BY 1
ORDER BY 1;
