import { useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";
import "./Login.css";

export default function Login() {
  const [data, setData] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const submit = async () => {
  try {
    const res = await API.post("auth/login/", data);

    localStorage.setItem("token", res.data.token);

    // ✅ ADD THIS LINE (important)
    localStorage.setItem("username", data.username);

    navigate("/");
  } catch (err) {
    alert("Invalid credentials");
  }
};


  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Welcome Back 👋</h2>
        <p className="subtitle">Login to your Smart Parking account</p>

        <input
          type="text"
          placeholder="Username"
          onChange={(e) =>
            setData({ ...data, username: e.target.value })
          }
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) =>
            setData({ ...data, password: e.target.value })
          }
        />

        <button onClick={submit}>Login</button>

        <p className="footer-text">
          Don’t have an account? 
          <span onClick={() => navigate("/register")}>Sign up</span>
        </p>
      </div>
    </div>
  );
}
