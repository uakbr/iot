-- Monitor average temperature over a 5-minute window for each device
CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" (
  "device_id" VARCHAR(50),
  "avg_temperature" FLOAT,
  "window_end" TIMESTAMP
);

CREATE OR REPLACE PUMP "STREAM_PUMP" AS
  INSERT INTO "DESTINATION_SQL_STREAM"
  SELECT
    "device_id",
    AVG("temperature") AS "avg_temperature",
    STEP("timestamp", INTERVAL '5' MINUTE) AS "window_end"
  FROM "SOURCE_SQL_STREAM_001"
  GROUP BY
    "device_id",
    STEP("timestamp", INTERVAL '5' MINUTE);