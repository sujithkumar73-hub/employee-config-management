const envBanner = document.getElementById("envBanner");
const envName = document.getElementById("envName");
const apiStatus = document.getElementById("apiStatus");
const dbStatus = document.getElementById("dbStatus");
const employeeCount = document.getElementById("employeeCount");
const statusAlert = document.getElementById("statusAlert");
const API_HOST = (!window.location.hostname || window.location.protocol === 'file:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:5000'
  : `${window.location.protocol}//${window.location.host}`;

const token = sessionStorage.getItem("ems_token");
if (!token) {
  window.location.href = "index.html";
}

async function loadStatus() {
  try {
    const response = await fetch(`${API_HOST}/api/health`, { headers: { Authorization: `Bearer ${token}` } });
    const data = await response.json();
    if (!response.ok) {
      statusAlert.style.display = "block";
      statusAlert.className = "alert error";
      statusAlert.textContent = data.message || "Unable to fetch status.";
      apiStatus.textContent = "Offline";
      dbStatus.textContent = "Unknown";
      return;
    }

    envName.textContent = data.app_mode;
    apiStatus.textContent = "Healthy";
    dbStatus.textContent = data.database === "ready" ? "Healthy" : "Error";
    setBanner(data.app_mode);
  } catch (error) {
    statusAlert.style.display = "block";
    statusAlert.className = "alert error";
    statusAlert.textContent = "Could not connect to API.";
    apiStatus.textContent = "Offline";
    dbStatus.textContent = "Offline";
  }

  try {
    const response = await fetch(`${API_HOST}/api/status`, { headers: { Authorization: `Bearer ${token}` } });
    const data = await response.json();
    employeeCount.textContent = data.data.total_employees;
  } catch (error) {
    employeeCount.textContent = "N/A";
  }
}

function setBanner(environment) {
  const colors = {
    Development: ["#deeefd", "#034d9f"],
    QA: ["#f7f2d0", "#8a6d1f"],
    UAT: ["#e9f7ef", "#1f7a56"],
    Production: ["#fde8e8", "#b72d2d"],
  };
  const [background, border] = colors[environment] || ["#eef2fb", "#1f3b70"];
  envBanner.style.background = background;
  envBanner.style.borderLeft = `5px solid ${border}`;
  envBanner.textContent = `Running in ${environment} Environment`;
}

loadStatus();
