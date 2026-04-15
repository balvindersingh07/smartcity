import { useEffect, useMemo, useState } from "react";

const API_BASE = import.meta.env.VITE_SMART_CITY_API_BASE || "http://localhost:8004";

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function statusFromMetric(key, value) {
  if (key === "aqi") return value <= 60 ? "safe" : value <= 90 ? "moderate" : "danger";
  if (key === "temperature") return value <= 30 ? "safe" : value <= 38 ? "moderate" : "danger";
  if (key === "humidity") return value <= 65 ? "safe" : value <= 80 ? "moderate" : "danger";
  if (key === "noise") return value <= 65 ? "safe" : value <= 80 ? "moderate" : "danger";
  return "moderate";
}

export function App() {
  const [metrics, setMetrics] = useState(null);
  const [sensors, setSensors] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const [m, s, a] = await Promise.all([
          fetchJson(`${API_BASE}/metrics`),
          fetchJson(`${API_BASE}/sensors`),
          fetchJson(`${API_BASE}/alerts`),
        ]);
        setMetrics(m);
        setSensors(Array.isArray(s) ? s : []);
        setAlerts(Array.isArray(a?.items) ? a.items : []);
      } catch (err) {
        setError(err.message || "Failed to fetch dashboard data");
      }
    };
    load();
  }, []);

  const metricCards = useMemo(() => {
    if (!metrics) return [];
    return [
      { label: "AQI", key: "aqi", value: Math.round(metrics.aqi?.latest ?? 0) },
      { label: "Temperature", key: "temperature", value: Math.round(metrics.temperature?.latest ?? 0), unit: "C" },
      { label: "Humidity", key: "humidity", value: Math.round(metrics.humidity?.latest ?? 0), unit: "%" },
      { label: "Noise", key: "noise", value: Math.round(metrics.noise?.latest ?? 0), unit: "dB" },
    ].map((card) => ({ ...card, status: statusFromMetric(card.key, card.value) }));
  }, [metrics]);

  return (
    <div className="page">
      <header>
        <h1>Smart City Monitoring (React)</h1>
        <p>Live data from API service: {API_BASE}</p>
      </header>

      {error ? <div className="error">{error}</div> : null}

      <section className="metrics">
        {metricCards.map((card) => (
          <article key={card.label} className={`card status-${card.status}`}>
            <h3>{card.label}</h3>
            <p>
              {card.value}
              {card.unit || ""}
            </p>
          </article>
        ))}
      </section>

      <section className="grid">
        <article className="card">
          <h2>Sensors</h2>
          <ul>
            {sensors.map((sensor) => (
              <li key={sensor.id}>
                {sensor.id} - {sensor.type} ({sensor.location_id})
              </li>
            ))}
          </ul>
        </article>

        <article className="card">
          <h2>Alerts</h2>
          <ul>
            {alerts.map((alert, idx) => (
              <li key={`${alert.sensor_id || "alert"}-${idx}`}>
                {alert.message || "Threshold event"} ({alert.severity || "warning"})
              </li>
            ))}
          </ul>
        </article>
      </section>
    </div>
  );
}
