import { createAccount, login, getLoginTemplate } from "../api.js";
import { loadLoggedView } from "./loggedView.js";

export async function loadNotLoggedView() {
  let $main = document.getElementById("main");
  let res = await getLoginTemplate();

  const content = await res.text();

  $main.innerHTML = content;

  const loginButton = document.getElementById("loginButton");
  const createAccountButton = document.getElementById("createAccountButton");

  loginButton.addEventListener("click", async () => {
    loginButton.disabled = true; // Disable button during request
    await handleLogin();
    loginButton.disabled = false; // Re-enable button
  });
  createAccountButton.addEventListener("click", async () => {
    createAccountButton.disabled = true; // Disable button during request
    await handleCreateAccount();
    createAccountButton.disabled = false; // Re-enable button
  });
}

async function handleLogin() {
  const emailInput = document.getElementById("emailInput");
  const passwordInput = document.getElementById("passwordInput");
  const email = emailInput.value;
  const password = passwordInput.value;
  try {
    const res = await login(email, password);
    const body = await res.json();
    if (body.access_token) {
      localStorage.setItem("access_token", body.access_token);
      loadLoggedView();
    } else {
      throw new Error("No access token received");
    }
  } catch (error) {
    console.error("Login failed:", error);
    alert("Login failed. Please check your credentials.");
  }
}

async function handleCreateAccount() {
  const emailInput = document.getElementById("emailInput");
  const passwordInput = document.getElementById("passwordInput");
  const email = emailInput.value;
  const password = passwordInput.value;
  try {
    const res = await createAccount(email, password);
    const body = await res.json();
    if (body.access_token) {
      localStorage.setItem("access_token", body.access_token);
      loadLoggedView();
    } else {
      throw new Error("No access token received");
    }
  } catch (error) {
    console.error("Account creation failed:", error);
    alert("Account creation failed. Please try again.");
  }
}
