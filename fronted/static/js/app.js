// frontend/static/js/app.js
const API_BASE_URL = "http://127.0.0.1:8000";

class BankingApp {
  constructor() {
    this.token = localStorage.getItem("banking_token");
    this.user = JSON.parse(localStorage.getItem("banking_user") || "null");
    this.init();
  }

  init() {
    this.bindForms();
    this.bindUI();
    this.checkAuthOnLoad();
  }

  bindForms() {
    const l = document.getElementById("loginForm");
    const r = document.getElementById("registerForm");
    const showR = document.getElementById("showRegister");
    const showL = document.getElementById("showLogin");

    if (l) l.addEventListener("submit", (e) => this.handleLogin(e));
    if (r) r.addEventListener("submit", (e) => this.handleRegister(e));
    if (showR) showR.addEventListener("click", (e) => { e.preventDefault(); this.toggleForms(); });
    if (showL) showL.addEventListener("click", (e) => { e.preventDefault(); this.toggleForms(); });
  }

  bindUI() {
    const logoutBtn = document.getElementById("logoutBtn");
    const filter = document.getElementById("transactionFilter");
    const toggleSidebar = document.getElementById("toggleSidebar");
    if (logoutBtn) logoutBtn.addEventListener("click", () => this.logout());
    if (filter) filter.addEventListener("change", () => this.filterTransactions());
    if (toggleSidebar) toggleSidebar.addEventListener("click", () => {
      const s = document.getElementById("sidebar");
      if (s) s.classList.toggle("hidden");
    });
  }

  toggleForms() {
    const l = document.getElementById("loginForm");
    const r = document.getElementById("registerForm");
    const msg = document.getElementById("message");
    if (l && r) { l.classList.toggle("hidden"); r.classList.toggle("hidden"); }
    if (msg) msg.classList.add("hidden");
  }

  showMessage(msg, type = "error") {
    const el = document.getElementById("message");
    if (!el) return;
    el.textContent = msg;
    el.className = `message ${type}`;
    el.classList.remove("hidden");
    setTimeout(() => el.classList.add("hidden"), 3800);
  }

  async handleLogin(e) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    try {
      const res = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: data.email, password: data.password })
      });
      const payload = await res.json();
      if (!res.ok) {
        this.showMessage(payload.detail || "Login failed", "error");
        return;
      }
      this.token = payload.access_token;
      this.user = payload.user;
      localStorage.setItem("banking_token", this.token);
      localStorage.setItem("banking_user", JSON.stringify(this.user));
      window.location.href = "dashboard.html";
    } catch (err) {
      console.error(err);
      this.showMessage("Network error", "error");
    }
  }

  async handleRegister(e) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    try {
      const res = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: data.username, email: data.email, password: data.password })
      });
      const payload = await res.json();
      if (!res.ok) {
        this.showMessage(payload.detail || "Registration failed", "error");
        return;
      }
      this.showMessage("Account created. Please sign in.", "success");
      setTimeout(() => this.toggleForms(), 1200);
    } catch (err) {
      console.error(err);
      this.showMessage("Network error", "error");
    }
  }

  checkAuthOnLoad() {
    const onLoginPage = !!document.getElementById("loginForm");
    if (this.token && this.user && onLoginPage) {
      window.location.href = "dashboard.html";
      return;
    }
    if (!this.token && !onLoginPage) {
      window.location.href = "index.html";
      return;
    }
    if (!onLoginPage) {
      this.loadDashboard();
    }
  }

  async loadDashboard() {
    if (!this.token) return;
    try {
      const welcome = document.getElementById("welcomeMessage");
      const em = document.getElementById("userEmail");
      if (welcome && this.user) welcome.textContent = `Welcome, ${this.user.username}`;
      if (em && this.user) em.textContent = this.user.email;

      const res = await fetch(`${API_BASE_URL}/transactions`, {
        headers: { "Authorization": `Bearer ${this.token}` }
      });
      if (res.status === 401) {
        this.logout();
        return;
      }
      const payload = await res.json();
      this.renderTransactions(payload.transactions || []);
      this.updateSummary(payload.transactions || []);
    } catch (err) {
      console.error(err);
      this.showMessage("Could not load transactions", "error");
    }
  }

  renderTransactions(txns = []) {
    const list = document.getElementById("transactionsList");
    if (!list) return;
    if (txns.length === 0) {
      list.innerHTML = `<div class="transaction-item"><div class="tx-desc muted">No transactions found</div></div>`;
      return;
    }
    list.innerHTML = txns.map(t => `
      <div class="transaction-item" data-type="${t.type}">
        <div class="left">
          <div class="icon-circle">
            ${t.type === "credit" ? "💚" : "🔻"}
          </div>
          <div>
            <div class="tx-desc">${t.description || "Transaction"}</div>
            <div class="tx-meta">${t.category || ""} • ${new Date(t.date).toLocaleString()}</div>
          </div>
        </div>
        <div class="transaction-amount ${t.type}">${t.type === "credit" ? '+' : '-'}$${Math.abs(t.amount).toFixed(2)}</div>
      </div>
    `).join("");
  }

  updateSummary(txns = []) {
    let balance = 0, income = 0, expenses = 0;
    txns.forEach(t => {
      if (t.type === "credit") { balance += t.amount; income += t.amount; }
      else { balance -= Math.abs(t.amount); expenses += Math.abs(t.amount); }
    });
    if (document.getElementById("currentBalance")) document.getElementById("currentBalance").textContent = `$${balance.toFixed(2)}`;
    if (document.getElementById("totalIncome")) document.getElementById("totalIncome").textContent = `$${income.toFixed(2)}`;
    if (document.getElementById("totalExpenses")) document.getElementById("totalExpenses").textContent = `$${expenses.toFixed(2)}`;
  }

  filterTransactions() {
    const filter = document.getElementById("transactionFilter").value;
    document.querySelectorAll(".transaction-item").forEach(it => {
      it.style.display = (filter === "all" || it.dataset.type === filter) ? "flex" : "none";
    });
  }

  logout() {
    localStorage.removeItem("banking_token");
    localStorage.removeItem("banking_user");
    this.token = null; this.user = null;
    window.location.href = "index.html";
  }
}

window.addEventListener("DOMContentLoaded", () => new BankingApp());
