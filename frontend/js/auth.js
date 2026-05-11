const loginBtn = document.getElementById("loginBtn");
const alertBox = document.getElementById("alert");

function showAlert(message, type = "error") {
  alertBox.textContent = message;
  alertBox.className = `alert ${type}`;
  alertBox.style.display = "block";
}

const API_HOST = (!window.location.hostname || window.location.protocol === 'file:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:5000'
  : `${window.location.protocol}//${window.location.host}`;

loginBtn.addEventListener("click", async () => {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !password) {
    return showAlert("Both username and password are required.");
  }

  try {
    const response = await fetch(`${API_HOST}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const result = await response.json();
    if (!response.ok) {
      return showAlert(result.message || "Login failed.");
    }

    sessionStorage.setItem("ems_token", result.data.access_token);
    window.location.href = "dashboard.html";
  } catch (error) {
    showAlert("Unable to reach authentication service.");
  }
});
