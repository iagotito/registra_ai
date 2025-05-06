import { getUserData } from "../api.js";
import { loadLoggedView } from "./loggedView.js";
import { loadNotLoggedView } from "./notLoggedView.js";

export async function loadHomeView() {
  const token = localStorage.getItem("access_token");

  const headers = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  let res = await getUserData(token);

  if (res.ok) {
    loadLoggedView();
  } else {
    loadNotLoggedView();
  }
}
