const envBanner = document.getElementById("envBanner");
const alertBox = document.getElementById("alert");
const showFormBtn = document.getElementById("showFormBtn");
const formCard = document.getElementById("formCard");
const formTitle = document.getElementById("formTitle");
const saveBtn = document.getElementById("saveEmployeeBtn");
const cancelBtn = document.getElementById("cancelBtn");
const employeeTableBody = document.querySelector("#employeeTable tbody");
const API_HOST = (!window.location.hostname || window.location.protocol === 'file:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:5000'
  : `${window.location.protocol}//${window.location.host}`;

let editingId = null;
const token = sessionStorage.getItem("ems_token");

if (!token) {
  window.location.href = "index.html";
}

function showAlert(message, type = "error") {
  alertBox.textContent = message;
  alertBox.className = `alert ${type}`;
  alertBox.style.display = "block";
}

async function fetchEnvironment() {
  try {
    const response = await fetch(`${API_HOST}/api/health`, { headers: { Authorization: `Bearer ${token}` } });
    const data = await response.json();
    if (response.ok) {
      envBanner.textContent = `Running in ${data.app_mode} Environment`;
      envBanner.style.background = data.app_mode === "Production" ? "#fde8e8" : data.app_mode === "QA" ? "#f7f2d0" : data.app_mode === "UAT" ? "#e9f7ef" : "#deeefd";
      envBanner.style.borderLeft = data.app_mode === "Production" ? "5px solid #b72d2d" : data.app_mode === "QA" ? "5px solid #8a6d1f" : data.app_mode === "UAT" ? "5px solid #1f7a56" : "5px solid #034d9f";
    }
  } catch (error) {
    showAlert("Unable to resolve environment banner.");
  }
}

async function loadEmployees() {
  try {
    const response = await fetch(`${API_HOST}/api/employees/`, { headers: { Authorization: `Bearer ${token}` } });
    const result = await response.json();
    if (!response.ok) {
      return showAlert(result.message || "Unable to load employees.");
    }
    renderEmployees(result.data);
  } catch (error) {
    showAlert("Employee API unavailable.");
  }
}

function renderEmployees(employees) {
  employeeTableBody.innerHTML = "";
  if (!employees.length) {
    employeeTableBody.innerHTML = '<tr><td colspan="6">No employees found.</td></tr>';
    return;
  }
  employees.forEach((employee) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${employee.name}</td>
      <td>${employee.email}</td>
      <td>${employee.department}</td>
      <td>${employee.designation}</td>
      <td>$${employee.salary.toLocaleString()}</td>
      <td>
        <button class="button secondary" onclick="editEmployee(${employee.id}, '${employee.name}', '${employee.email}', '${employee.department}', '${employee.designation}', ${employee.salary})">Edit</button>
        <button class="button" onclick="deleteEmployee(${employee.id})">Delete</button>
      </td>
    `;
    employeeTableBody.appendChild(row);
  });
}

window.editEmployee = (id, name, email, department, designation, salary) => {
  editingId = id;
  formTitle.textContent = "Edit Employee";
  document.getElementById("employeeName").value = name;
  document.getElementById("employeeEmail").value = email;
  document.getElementById("employeeDepartment").value = department;
  document.getElementById("employeeDesignation").value = designation;
  document.getElementById("employeeSalary").value = salary;
  formCard.style.display = "block";
};

window.deleteEmployee = async (id) => {
  if (!confirm("Delete this employee?")) {
    return;
  }
  try {
    const response = await fetch(`${API_HOST}/api/employees/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    const result = await response.json();
    if (!response.ok) {
      return showAlert(result.message || "Failed to delete record.");
    }
    await loadEmployees();
    showAlert("Employee removed successfully.", "success");
  } catch (error) {
    showAlert("Unable to complete delete request.");
  }
};

showFormBtn.addEventListener("click", () => {
  editingId = null;
  formTitle.textContent = "Add Employee";
  formCard.style.display = "block";
  document.getElementById("employeeName").value = "";
  document.getElementById("employeeEmail").value = "";
  document.getElementById("employeeDepartment").value = "";
  document.getElementById("employeeDesignation").value = "";
  document.getElementById("employeeSalary").value = "";
});

cancelBtn.addEventListener("click", () => {
  formCard.style.display = "none";
  editingId = null;
});

saveBtn.addEventListener("click", async () => {
  const payload = {
    name: document.getElementById("employeeName").value.trim(),
    email: document.getElementById("employeeEmail").value.trim(),
    department: document.getElementById("employeeDepartment").value.trim(),
    designation: document.getElementById("employeeDesignation").value.trim(),
    salary: parseFloat(document.getElementById("employeeSalary").value),
  };

  const method = editingId ? "PUT" : "POST";
  const endpoint = editingId ? `/api/employees/${editingId}` : "/api/employees/";

  try {
    const response = await fetch(`${API_HOST}${endpoint}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok) {
      return showAlert(result.message || "Could not save employee.");
    }
    await loadEmployees();
    showAlert(editingId ? "Employee updated successfully." : "Employee added successfully.", "success");
    formCard.style.display = "none";
    editingId = null;
  } catch (error) {
    showAlert("Employee service unavailable.");
  }
});

fetchEnvironment();
loadEmployees();
