const metricData = [
  { key: "aqi", label: "Air Quality Index (AQI)", value: 68, unit: "", status: "moderate", icon: "AQ", trend: "+4.2%" },
  { key: "temp", label: "Temperature", value: 29, unit: "°C", status: "safe", icon: "TP", trend: "+1.1%" },
  { key: "humidity", label: "Humidity", value: 74, unit: "%", status: "moderate", icon: "HM", trend: "-0.6%" },
  { key: "noise", label: "Noise Level", value: 81, unit: "dB", status: "danger", icon: "NS", trend: "+3.4%" },
];

const sensors = [
  { id: "S-1001", zone: "North", x: 18, y: 35, aqi: 52, temp: 27, humidity: 64, noise: 61, status: "safe", sync: "5s ago" },
  { id: "S-1002", zone: "Downtown", x: 44, y: 48, aqi: 96, temp: 31, humidity: 76, noise: 88, status: "danger", sync: "2s ago" },
  { id: "S-1003", zone: "West", x: 31, y: 66, aqi: 72, temp: 29, humidity: 71, noise: 72, status: "moderate", sync: "6s ago" },
  { id: "S-1004", zone: "East", x: 67, y: 34, aqi: 59, temp: 28, humidity: 62, noise: 63, status: "safe", sync: "8s ago" },
  { id: "S-1005", zone: "South", x: 78, y: 70, aqi: 109, temp: 33, humidity: 79, noise: 84, status: "danger", sync: "1s ago" },
];

const alerts = [
  { title: "Critical AQI", message: "Downtown AQI crossed 95 threshold", level: "critical", time: "1 min ago" },
  { title: "Noise Spike", message: "South zone noise reached 84 dB", level: "warning", time: "4 min ago" },
  { title: "Humidity Stable", message: "North zone returned to safe humidity", level: "normal", time: "8 min ago" },
];

const notifications = [
  { title: "Ingestion service healthy", text: "No packet loss in the last 30 minutes." },
  { title: "Stream processor deployed", text: "Version 2.4 rolled out to staging cluster." },
  { title: "Budget alert", text: "Monthly cloud spend reached 68% of forecast." },
];
const API_BASE_URL = window.SMART_CITY_API_BASE || "http://localhost:8004";

const statusClassByValue = {
  safe: "green",
  moderate: "yellow",
  danger: "red",
};

function titleCase(value) {
  return value[0].toUpperCase() + value.slice(1);
}

function getStatusFromAqi(aqi) {
  if (aqi <= 60) return "safe";
  if (aqi <= 90) return "moderate";
  return "danger";
}

function getStatusChip(status) {
  const map = {
    safe: { cls: "status-green", label: "Safe" },
    moderate: { cls: "status-yellow", label: "Moderate" },
    danger: { cls: "status-red", label: "Danger" },
  };
  return map[status];
}

function renderMetrics() {
  const grid = document.getElementById("metricsGrid");
  grid.innerHTML = metricData
    .map((metric) => {
      const status = getStatusChip(metric.status);
      const trendArrow = metric.trend.startsWith("-") ? "DOWN" : "UP";
      return `
      <article class="metric-card glass-card">
        <div class="metric-card__head">
          <p class="metric-card__label">${metric.label}</p>
          <div class="metric-card__icon">${metric.icon}</div>
        </div>
        <p class="metric-card__value">${metric.value}${metric.unit}</p>
        <div class="metric-card__foot">
          <span class="metric-card__status ${status.cls}">
            <span class="dot"></span>${status.label}
          </span>
          <span class="metric-card__trend">${trendArrow} ${metric.trend}</span>
        </div>
      </article>`;
    })
    .join("");
}

function renderMapSensors() {
  const map = document.getElementById("cityMap");
  const tooltip = document.getElementById("mapTooltip");

  sensors.forEach((sensor) => {
    const marker = document.createElement("button");
    marker.className = `sensor-marker sensor-marker--${sensor.status}`;
    marker.type = "button";
    marker.style.left = `${sensor.x}%`;
    marker.style.top = `${sensor.y}%`;
    marker.title = `${sensor.id} - ${sensor.zone}`;

    marker.addEventListener("click", () => {
      const status = getStatusChip(sensor.status);
      tooltip.hidden = false;
      tooltip.style.left = `min(calc(${sensor.x}% + 20px), calc(100% - 228px))`;
      tooltip.style.top = `max(calc(${sensor.y}% - 62px), 12px)`;
      tooltip.innerHTML = `
        <p class="map-tooltip__title">${sensor.id} / ${sensor.zone}</p>
        <p class="map-tooltip__meta">Live station telemetry</p>
        <div class="map-tooltip__stats">
          <span>AQI <strong>${sensor.aqi}</strong></span>
          <span>Temp <strong>${sensor.temp}°C</strong></span>
          <span>Humidity <strong>${sensor.humidity}%</strong></span>
          <span>Noise <strong>${sensor.noise} dB</strong></span>
        </div>
        <span class="map-tooltip__chip ${status.cls}">
          <span class="dot"></span>${status.label}
        </span>
      `;
    });

    map.appendChild(marker);
  });

  map.addEventListener("click", (event) => {
    if (!event.target.classList.contains("sensor-marker")) {
      tooltip.hidden = true;
    }
  });
}

function renderAlerts() {
  const icons = {
    critical: "!",
    warning: "~",
    normal: "+",
  };

  const list = document.getElementById("alertsList");
  list.innerHTML = alerts
    .map(
      (item) => `
    <li class="alert-item alert-item--${item.level}">
      <div class="alert-title">
        <span class="alert-title__left"><span class="alert-icon">${icons[item.level]}</span>${item.title}</span>
        <span>${item.time}</span>
      </div>
      <p class="alert-meta">${item.message}</p>
    </li>`
    )
    .join("");
}

function renderTable() {
  const body = document.getElementById("sensorTableBody");
  body.innerHTML = sensors
    .map((sensor) => {
      const badgeClass =
        sensor.status === "safe" ? "badge--online" : sensor.status === "danger" ? "badge--danger" : "badge--warning";
      return `
      <tr>
        <td>${sensor.id}</td>
        <td>${sensor.zone}</td>
        <td><span class="badge ${badgeClass}">${titleCase(sensor.status)}</span></td>
        <td>${sensor.sync}</td>
      </tr>
      `;
    })
    .join("");
}

function renderNotifications() {
  const list = document.getElementById("notificationsList");
  list.innerHTML = notifications
    .map(
      (item) => `
      <li class="notification-item">
        <strong>${item.title}</strong>
        <p>${item.text}</p>
      </li>
    `
    )
    .join("");
}

function commonChartOptions() {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 450,
      easing: "easeOutQuart",
    },
    interaction: {
      intersect: false,
      mode: "index",
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: "rgba(8,16,32,0.92)",
        borderColor: "rgba(79,209,197,0.42)",
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        ticks: { color: "#9fb0d4" },
        grid: { color: "rgba(255,255,255,0.08)" },
      },
      y: {
        ticks: { color: "#9fb0d4" },
        grid: { color: "rgba(255,255,255,0.08)" },
      },
    },
  };
}

function makeGradient(context, first, second) {
  const { chart } = context;
  const { ctx, chartArea } = chart;
  if (!chartArea) return first;
  const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
  gradient.addColorStop(0, first);
  gradient.addColorStop(1, second);
  return gradient;
}

function upsertChart(canvasId, chartConfig) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const existing = Chart.getChart(canvas);
  if (existing) {
    existing.destroy();
  }
  return new Chart(canvas, chartConfig);
}

function renderCharts() {
  if (typeof Chart !== "function") {
    showToast("Chart Engine Missing", "Charts could not load. Check network/CDN access.");
    return;
  }

  const labels = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"];
  const tempSeries = [24, 25, 27, 28, 29, 31, 32, 33, 31, 30, 29, 28];
  const aqiSeries = [40, 48, 53, 59, 70, 85, 94, 88, 83, 77, 71, 68];
  const compactAxis = window.matchMedia("(max-width: 520px)").matches;

  const temperatureOptions = commonChartOptions();
  const aqiOptions = commonChartOptions();
  const noiseOptions = commonChartOptions();

  if (compactAxis) {
    [temperatureOptions, aqiOptions, noiseOptions].forEach((opts) => {
      opts.scales.x.ticks.maxRotation = 0;
      opts.scales.x.ticks.autoSkip = true;
      opts.scales.x.ticks.maxTicksLimit = 6;
    });
  }

  upsertChart("temperatureChart", {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          data: tempSeries,
          borderColor: "#4fd1c5",
          borderWidth: 2.5,
          pointRadius: 0,
          tension: 0.42,
          fill: true,
          backgroundColor: (ctx) => makeGradient(ctx, "rgba(79,209,197,0.35)", "rgba(79,209,197,0.02)"),
        },
      ],
    },
    options: temperatureOptions,
  });

  upsertChart("aqiChart", {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          data: aqiSeries,
          borderColor: "#7f5af0",
          borderWidth: 2.5,
          pointRadius: 0,
          tension: 0.42,
          fill: true,
          backgroundColor: (ctx) => makeGradient(ctx, "rgba(127,90,240,0.34)", "rgba(127,90,240,0.03)"),
        },
      ],
    },
    options: aqiOptions,
  });

  const zones = ["North", "Downtown", "West", "East", "South"];
  const zoneNoise = sensors.map((sensor) => sensor.noise);

  upsertChart("noiseChart", {
    type: "bar",
    data: {
      labels: zones,
      datasets: [
        {
          data: zoneNoise,
          borderRadius: 10,
          borderSkipped: false,
          backgroundColor: zoneNoise.map((val) => {
            if (val <= 65) return "rgba(46,204,113,0.8)";
            if (val <= 75) return "rgba(255,200,87,0.82)";
            return "rgba(255,77,79,0.82)";
          }),
        },
      ],
    },
    options: noiseOptions,
  });
}

function updateMetricFromSensors() {
  const avg = (arr) => Math.round(arr.reduce((sum, n) => sum + n, 0) / arr.length);
  const avgAqi = avg(sensors.map((sensor) => sensor.aqi));
  const avgTemp = avg(sensors.map((sensor) => sensor.temp));
  const avgHumidity = avg(sensors.map((sensor) => sensor.humidity));
  const avgNoise = avg(sensors.map((sensor) => sensor.noise));

  metricData[0] = {
    key: "aqi",
    label: "Air Quality Index (AQI)",
    value: avgAqi,
    unit: "",
    status: getStatusFromAqi(avgAqi),
    icon: "AQ",
    trend: "+4.2%",
  };
  metricData[1] = {
    key: "temp",
    label: "Temperature",
    value: avgTemp,
    unit: "°C",
    status: avgTemp <= 30 ? "safe" : "moderate",
    icon: "TP",
    trend: "+1.1%",
  };
  metricData[2] = {
    key: "humidity",
    label: "Humidity",
    value: avgHumidity,
    unit: "%",
    status: avgHumidity < 65 ? "safe" : "moderate",
    icon: "HM",
    trend: "-0.6%",
  };
  metricData[3] = {
    key: "noise",
    label: "Noise Level",
    value: avgNoise,
    unit: "dB",
    status: avgNoise <= 70 ? "moderate" : "danger",
    icon: "NS",
    trend: "+3.4%",
  };
}

function showToast(title, text) {
  const stack = document.getElementById("toastStack");
  const toast = document.createElement("article");
  toast.className = "toast";
  toast.innerHTML = `<strong>${title}</strong><p>${text}</p>`;
  stack.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3600);
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json();
}

function inferStatusFromValue(type, value) {
  if (type === "aqi") return value <= 60 ? "safe" : value <= 90 ? "moderate" : "danger";
  if (type === "temperature") return value <= 30 ? "safe" : value <= 38 ? "moderate" : "danger";
  if (type === "humidity") return value < 65 ? "safe" : value <= 80 ? "moderate" : "danger";
  if (type === "noise") return value <= 65 ? "safe" : value <= 80 ? "moderate" : "danger";
  return "moderate";
}

async function hydrateFromBackend() {
  try {
    const [metricsResp, sensorsResp, alertsResp] = await Promise.all([
      fetchJson(`${API_BASE_URL}/metrics`),
      fetchJson(`${API_BASE_URL}/sensors`),
      fetchJson(`${API_BASE_URL}/alerts`),
    ]);

    if (Array.isArray(sensorsResp) && sensorsResp.length) {
      const mappedSensors = sensorsResp.map((sensor, idx) => ({
        id: sensor.id,
        zone: sensor.location_id || `Zone-${idx + 1}`,
        x: 15 + ((idx * 13) % 70),
        y: 25 + ((idx * 11) % 55),
        aqi: 60 + (idx % 6) * 8,
        temp: 26 + (idx % 5),
        humidity: 60 + (idx % 8) * 3,
        noise: 62 + (idx % 6) * 4,
        status: sensor.status === "active" ? "safe" : "moderate",
        sync: "live",
      }));
      sensors.splice(0, sensors.length, ...mappedSensors);
    }

    if (metricsResp && typeof metricsResp === "object") {
      const nextMetrics = [
        {
          key: "aqi",
          label: "Air Quality Index (AQI)",
          value: Math.round(metricsResp.aqi?.latest ?? metricData[0].value),
          unit: "",
          icon: "AQ",
          trend: "+0.8%",
        },
        {
          key: "temp",
          label: "Temperature",
          value: Math.round(metricsResp.temperature?.latest ?? metricData[1].value),
          unit: "°C",
          icon: "TP",
          trend: "+0.4%",
        },
        {
          key: "humidity",
          label: "Humidity",
          value: Math.round(metricsResp.humidity?.latest ?? metricData[2].value),
          unit: "%",
          icon: "HM",
          trend: "-0.3%",
        },
        {
          key: "noise",
          label: "Noise Level",
          value: Math.round(metricsResp.noise?.latest ?? metricData[3].value),
          unit: "dB",
          icon: "NS",
          trend: "+1.2%",
        },
      ].map((metric) => ({
        ...metric,
        status: inferStatusFromValue(metric.key, metric.value),
      }));
      metricData.splice(0, metricData.length, ...nextMetrics);
    }

    if (alertsResp && Array.isArray(alertsResp.items)) {
      const mappedAlerts = alertsResp.items.slice(0, 8).map((alert) => ({
        title: `${alert.type?.toUpperCase() || "Sensor"} Alert`,
        message: alert.message || "Threshold breached",
        level: alert.severity === "critical" ? "critical" : "warning",
        time: "live",
      }));
      if (mappedAlerts.length) {
        alerts.splice(0, alerts.length, ...mappedAlerts);
      }
    }

    notifications.unshift({
      title: "API Connected",
      text: `Live data source: ${API_BASE_URL}`,
    });
  } catch (_) {
    notifications.unshift({
      title: "Offline Mode",
      text: "Backend unavailable. Showing simulated real-time data.",
    });
  }
}

function renderToasts() {
  showToast("Smart City Console", "Live sensor grid connected.");
  setTimeout(() => showToast("Alert Feed", "1 critical alert requires attention."), 650);
}

function setupSidebarNavigation() {
  const navButtons = document.querySelectorAll(".sidebar__nav .nav-item");
  if (!navButtons.length) return;

  navButtons.forEach((button) => {
    button.addEventListener("click", () => {
      navButtons.forEach((item) => item.classList.remove("nav-item--active"));
      button.classList.add("nav-item--active");

      const targetId = button.dataset.target;
      if (!targetId) return;

      const targetEl = document.getElementById(targetId);
      if (!targetEl) return;

      targetEl.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });

      const label = button.textContent?.trim() || "Section";
      showToast("Navigation", `${label} section opened.`);
    });
  });
}

function setupResponsiveChartRefresh() {
  let resizeTimer = null;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      renderCharts();
    }, 180);
  });
}

async function initDashboard() {
  await hydrateFromBackend();
  updateMetricFromSensors();
  renderMetrics();
  renderMapSensors();
  renderAlerts();
  renderTable();
  renderNotifications();
  renderCharts();
  setupSidebarNavigation();
  setupResponsiveChartRefresh();
  renderToasts();
}

initDashboard();
