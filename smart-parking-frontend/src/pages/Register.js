import { useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";
import "./Login.css"; // reuse same modern style

export default function Register() {
  const [data, setData] = useState({
    username: "",
    password: "",
    email: "",
  });

  const navigate = useNavigate();

  const submit = async () => {
    try {
      await API.post("auth/register/", data);
      alert("Registration successful!");
      navigate("/login");
    } catch (err) {
      alert("Registration failed");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Create Account 🚀</h2>
        <p className="subtitle">Join Smart Parking System</p>

        <input
          placeholder="Username"
          onChange={(e) =>
            setData({ ...data, username: e.target.value })
          }
        />

        <input
          type="email"
          placeholder="Email"
          onChange={(e) =>
            setData({ ...data, email: e.target.value })
          }
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) =>
            setData({ ...data, password: e.target.value })
          }
        />

        <button onClick={submit}>Register</button>

        <p className="footer-text">
          Already have an account?{" "}
          <span onClick={() => navigate("/login")}>Login</span>
        </p>
      </div>
    </div>
  );
}
