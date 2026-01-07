import { useState, useEffect } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Reserve() {
  const [slots, setSlots] = useState([]);
  const [vehicleNumber, setVehicleNumber] = useState("");
  const [slotId, setSlotId] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const token = localStorage.getItem("token"); // ✅ check login

  // Fetch available slots
  useEffect(() => {
    const fetchSlots = async () => {
      try {
        const res = await API.get("/slots/");
        const available = res.data.filter(
          (slot) => slot.status === "available"
        );
        setSlots(available);
        if (available.length > 0) setSlotId(available[0].id);
      } catch (err) {
        setError("Failed to fetch slots.");
      }
    };
    fetchSlots();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // ✅ LOGIN CHECK FIRST
    if (!token) {
      setError("Please login first to reserve a parking slot.");
      return;
    }

    if (!vehicleNumber || !slotId || !startTime || !endTime) {
      setError("Please fill all fields.");
      return;
    }

    try {
      const res = await API.post("/reserve/", {
        vehicle_number: vehicleNumber,
        slot_id: slotId,
        start_time: startTime,
        end_time: endTime,
      });

      alert("Reservation created successfully!");
      navigate(`/payment/${res.data.reservation.id}`);
    } catch (err) {
      setError("Reservation failed. Please try again.");
    }
  };

  return (
    <div
      style={{
        maxWidth: 500,
        margin: "50px auto",
        padding: 20,
        border: "1px solid #ddd",
        borderRadius: 8,
      }}
    >
      <h2>Reserve Parking Slot</h2>

      {/* ✅ Error message */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* ✅ LOGIN BUTTON WHEN NOT LOGGED IN */}

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 15 }}>
          <label>Vehicle Number:</label>
          <input
            type="text"
            value={vehicleNumber}
            onChange={(e) => setVehicleNumber(e.target.value)}
            style={{ width: "100%", padding: 8 }}
          />
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>Select Slot:</label>
          <select
            value={slotId}
            onChange={(e) => setSlotId(e.target.value)}
            style={{ width: "100%", padding: 8 }}
          >
            {slots.map((slot) => (
              <option key={slot.id} value={slot.id}>
                {slot.slot_number}
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>Start Time:</label>
          <input
            type="datetime-local"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            style={{ width: "100%", padding: 8 }}
          />
        </div>

        <div style={{ marginBottom: 15 }}>
          <label>End Time:</label>
          <input
            type="datetime-local"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
            style={{ width: "100%", padding: 8 }}
          />
        </div>

        <div style={{ display: "flex", gap: 10 }}>
  <button
    type="submit"
    style={{
      padding: "10px 20px",
      backgroundColor: "#4caf50",
      color: "#fff",
      border: "none",
      borderRadius: 4,
      cursor: "pointer",
    }}
  >
    Reserve
  </button>

  {!token && (
    <button
      type="button"
      onClick={() => navigate("/login")}
      style={{
        padding: "10px 20px",
        backgroundColor: "#1976d2",
        color: "#fff",
        border: "none",
        borderRadius: 4,
        cursor: "pointer",
      }}
    >
      Login
    </button>
  )}
</div>

      </form>
    </div>
  );
}
