import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import API from "../api/api";

export default function Payment() {
  const { reservation_id } = useParams();
  const navigate = useNavigate();
  const [reservation, setReservation] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load Razorpay script dynamically
  const loadRazorpayScript = () => {
    return new Promise((resolve) => {
      if (window.Razorpay) return resolve(true);
      const script = document.createElement("script");
      script.src = "https://checkout.razorpay.com/v1/checkout.js";
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };

  // Check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("You must be logged in to make a payment!");
      navigate("/login");
    }
  }, [navigate]);

  // Fetch reservation details
  useEffect(() => {
    const fetchReservation = async () => {
      try {
        const res = await API.get(`reservations/${reservation_id}/`);
        setReservation(res.data);
      } catch (err) {
        console.error("Error fetching reservation:", err);
        alert(
          err.response?.data?.error ||
            "Failed to fetch reservation details. Are you logged in?"
        );
        navigate("/"); // Go back home if failed
      } finally {
        setLoading(false);
      }
    };
    fetchReservation();
  }, [reservation_id, navigate]);

  // Pay Now
  const payNow = async () => {
    if (!reservation) return;

    const scriptLoaded = await loadRazorpayScript();
    if (!scriptLoaded) {
      alert("Failed to load Razorpay payment script. Please try again.");
      return;
    }

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("You must be logged in to pay!");
        navigate("/login");
        return;
      }

      // Create order on backend
      const orderRes = await API.post("payment/create-order/", {
        reservation_id: reservation.id,
      });

      const order_id = orderRes.data?.order_id;
      const amount = orderRes.data?.amount;
      const key = orderRes.data?.key;

      if (!order_id || !amount || !key) {
        console.error("Invalid response from backend:", orderRes.data);
        alert("Failed to create payment order. Please try again.");
        return;
      }

      const options = {
        key: key,
        amount: amount,
        currency: "INR",
        name: "Smart Parking",
        description: `Payment for Reservation #${reservation.id}`,
        order_id: order_id,
        handler: async function (response) {
          try {
            await API.post("payment/verify/", {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
            });

            alert("Payment successful!");
            navigate("/");
          } catch (err) {
            console.error("Verification error:", err.response?.data);
            alert(
              err.response?.data?.error ||
                "Payment verification failed. Contact support."
            );
          }
        },
        theme: { color: "#0b79d0" },
      };

      // ✅ Open Razorpay payment
      const rzp = new window.Razorpay(options);
      rzp.open();
    } catch (err) {
      console.error("Create order error:", err.response || err);
      alert(
        err.response?.data?.error ||
          "Payment failed. Make sure you are logged in and try again."
      );
    }
  };

  if (loading) return <p>Loading reservation details...</p>;
  if (!reservation) return <p>Reservation not found.</p>;

  return (
  <div
    style={{
      padding: 20,
      maxWidth: 500,
      margin: "50px auto",
      border: "1px solid #ddd",
      borderRadius: 8,
      background: "#fff",
    }}
  >
    <h2>💳 Payment Details</h2>

    <div style={{ marginBottom: 10 }}>
      <strong>Reservation ID:</strong> {reservation.id}
    </div>

    <div style={{ marginBottom: 10 }}>
      <strong>Vehicle Number:</strong> {reservation.vehicle_number}
    </div>

    <div style={{ marginBottom: 10 }}>
      <strong>Slot Number:</strong>{" "}
      {reservation.slot?.slot_number || reservation.slot_number}
    </div>

    <div style={{ marginBottom: 10 }}>
      <strong>Start Time:</strong>{" "}
      {new Date(reservation.start_time).toLocaleString()}
    </div>

    <div style={{ marginBottom: 10 }}>
      <strong>End Time:</strong>{" "}
      {new Date(reservation.end_time).toLocaleString()}
    </div>

    <div style={{ marginBottom: 15 }}>
      <strong>Amount:</strong> ₹{reservation.amount}
    </div>

    <button
      onClick={payNow}
      style={{
        width: "100%",
        padding: "12px",
        backgroundColor: "#4caf50",
        color: "#fff",
        border: "none",
        borderRadius: 4,
        cursor: "pointer",
        fontSize: 16,
      }}
    >
      Pay Now
    </button>
  </div>
);

}
