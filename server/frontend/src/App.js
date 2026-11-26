import Register from "./components/Register/Register";
import LoginPanel from "./components/Login/Login"
import Dealers from "./components/Dealers/Dealers";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}
export default App;
