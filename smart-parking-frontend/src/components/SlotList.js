import { useNavigate } from "react-router-dom";
import "./SlotList.css";

export default function SlotList({ slots }) {
  const group = (status) => slots.filter((s) => s.status === status);

  return (
    <div className="slot-container">
      <SlotSection title="Available Slots" status="available" slots={group("available")} />
      <SlotSection title="Reserved Slots" status="reserved" slots={group("reserved")} />
      <SlotSection title="Occupied Slots" status="occupied" slots={group("occupied")} />
    </div>
  );
}

const SlotSection = ({ title, slots, status }) => (
  <div className="slot-section">
    <h3>{title}</h3>
    <div className="slot-grid">
      {slots.length ? (
        slots.map((s) => <Slot key={s.id} slot={s} />)
      ) : (
        <p className="empty-text">No slots</p>
      )}
    </div>
  </div>
);

const Slot = ({ slot }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    if (slot.status === "available") {
      navigate("/reserve", { state: { slot } });
    }
  };

  return (
    <div
      className={`slot-card ${slot.status}`}
      onClick={handleClick}
      style={{
        cursor: slot.status === "available" ? "pointer" : "not-allowed",
        opacity: slot.status === "available" ? 1 : 0.6,
      }}
    >
      <h4>Slot {slot.slot_number}</h4>
      <span className="badge">{slot.status}</span>
    </div>
  );
};
