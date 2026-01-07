import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Reserve from "./pages/Reserve";
import Navbar from "./components/Navbar";
import Payment from "./pages/Payment";
import Footer from "./pages/Footer";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/reserve" element={<Reserve />} />
        <Route path="/payment/:reservation_id" element={<Payment />} />
      </Routes>
      <Footer/>
    </BrowserRouter>
  );
}

export default App;
