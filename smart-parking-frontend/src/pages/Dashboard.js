import { useEffect, useState } from "react";
import API from "../api/api";
import SlotList from "../components/SlotList";

export default function Dashboard() {
  const [counts, setCounts] = useState({
  total: 0,
  available: 0,
  reserved: 0,
  occupied: 0,
});



  const [slots, setSlots] = useState([]);

  useEffect(() => {
    API.get("dashboard/")
      .then(res => {
        console.log("Dashboard API:", res.data);
        setCounts(res.data);
      })
      .catch(err => console.error(err));

    API.get("slots/")
      .then(res => {
        console.log("Slots API:", res.data);
        setSlots(res.data);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={styles.page}>
      <h1 style={styles.heading}>📊 Smart Parking Dashboard</h1>

      {/* Stats Cards */}
      <div style={styles.cards}>
        <Card title="Total Slots" value={counts.total} color="#6366f1" />
        <Card title="Available" value={counts.available} color="#22c55e" />
        <Card title="Reserved" value={counts.reserved} color="#f59e0b" />
        <Card title="Occupied" value={counts.occupied} color="#ef4444" />

      </div>

      {/* Slot List */}
      <div style={styles.slotSection}>
        <h2 style={styles.sectionTitle}>🚗 Parking Slots</h2>

        {slots.length > 0 ? (
          <SlotList slots={slots} />
        ) : (
          <p style={{ color: "#6b7280" }}>No slots available</p>
        )}
      </div>
    </div>
  );
}



const Card = ({ title, value, color }) => (
  <div style={{ ...styles.card, borderLeft: `6px solid ${color}` }}>
    <p style={styles.cardTitle}>{title}</p>
    <h2 style={{ ...styles.cardValue, color }}>{value}</h2>
  </div>
);

const styles = {
  page: {
    padding: "40px",
    background: "#f4f6fb",
    minHeight: "calc(100vh - 140px)"
  },

  heading: {
    fontSize: "28px",
    fontWeight: "700",
    marginBottom: "30px",
    color: "#1f2937"
  },

  cards: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "20px",
    marginBottom: "40px"
  },

  card: {
    background: "#ffffff",
    padding: "22px",
    borderRadius: "16px",
    boxShadow: "0 12px 30px rgba(0,0,0,0.08)",
    transition: "transform 0.3s ease",
    cursor: "pointer"
  },

  cardTitle: {
    fontSize: "14px",
    color: "#6b7280",
    marginBottom: "6px"
  },

  cardValue: {
    fontSize: "32px",
    fontWeight: "700"
  },

  slotSection: {
    background: "#ffffff",
    padding: "25px",
    borderRadius: "16px",
    boxShadow: "0 12px 30px rgba(0,0,0,0.08)"
  },

  sectionTitle: {
    marginBottom: "15px",
    fontSize: "22px",
    fontWeight: "600",
    color: "#374151"
  }
};
