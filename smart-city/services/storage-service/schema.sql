CREATE TABLE IF NOT EXISTS locations (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(128) NOT NULL,
  city VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS sensors (
  id VARCHAR(64) PRIMARY KEY,
  type VARCHAR(32) NOT NULL,
  location_id VARCHAR(64) NOT NULL REFERENCES locations(id),
  status VARCHAR(24) NOT NULL DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS sensor_data (
  id BIGSERIAL PRIMARY KEY,
  sensor_id VARCHAR(64) NOT NULL REFERENCES sensors(id),
  type VARCHAR(32) NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  rolling_avg DOUBLE PRECISION NULL,
  is_valid BOOLEAN NOT NULL DEFAULT TRUE,
  recorded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sensor_data_type_time ON sensor_data(type, recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_sensor_data_sensor_time ON sensor_data(sensor_id, recorded_at DESC);
