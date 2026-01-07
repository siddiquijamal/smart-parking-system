import { NavLink, useNavigate } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  // ✅ ADD THIS LINE
  const username = localStorage.getItem("username");

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username"); // ✅ cleanup
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="logo" onClick={() => navigate("/")}>
        🚗 <span>Smart Parking</span>
      </div>

      <div className="menu">
        <NavLink to="/" className="nav-link">
          Home
        </NavLink>

        <NavLink to="/reserve" className="nav-link">
          Reserve
        </NavLink>

        {token ? (
          <>
            {/* ✅ SHOW USERNAME */}
            <span style={{ color: "#fff", marginRight: "10px" }}>
              👤 {username}
            </span>

            <button onClick={logout} className="logout">
              Logout
            </button>
          </>
        ) : (
          <>
            <NavLink to="/login" className="nav-link">
              Login
            </NavLink>

            <NavLink to="/register" className="register">
              Register
            </NavLink>
          </>
        )}
      </div>
    </nav>
  );
}
