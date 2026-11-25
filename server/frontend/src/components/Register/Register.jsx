import React, { useState } from "react";
import "./Register.css";
import user_icon from "../assets/person.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";
import close_icon from "../assets/close.png";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);

  const register = async (e) => {
    e.preventDefault();
    setError("");
    setPending(true);
    try {
      const res = await fetch(window.location.origin + "/djangoapp/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userName, password, firstName, lastName, email }),
      });
      const json = await res.json();
      if (res.ok && json.status === "Authenticated") {
        sessionStorage.setItem("username", json.userName);
        window.location.href = window.location.origin;
      } else {
        setError(json.error === "Already Registered"
          ? "The user with same username is already registered"
          : json.error || "Registration failed. Please try again.");
      }
    } catch {
      setError("Unable to connect. Please try again.");
    } finally {
      setPending(false);
    }
  };

  return (
    <div className="register_container" style={{width: "50%", maxWidth: "620px", borderRadius: "12px", padding: "20px", boxSizing: "border-box"}}>
      <div className="header" style={{display: "flex", flexDirection: "row", justifyContent: "space-between", alignItems: "center"}}>
        <span className="text" style={{fontSize: "0.7em"}}>SignUp</span>
        <a href="/" aria-label="Close registration"><img style={{width:"1cm"}} src={close_icon} alt="Close"/></a>
      </div>
      <form onSubmit={register}>
        <div className="inputs">
          <div className="input"><img src={user_icon} className="img_icon" alt=""/><input required aria-label="Username" autoComplete="username" type="text" name="username" placeholder="Username" className="input_field" value={userName} onChange={e => setUserName(e.target.value)}/></div>
          <div className="input"><img src={user_icon} className="img_icon" alt=""/><input required aria-label="First Name" autoComplete="given-name" type="text" name="first_name" placeholder="First Name" className="input_field" value={firstName} onChange={e => setFirstName(e.target.value)}/></div>
          <div className="input"><img src={user_icon} className="img_icon" alt=""/><input required aria-label="Last Name" autoComplete="family-name" type="text" name="last_name" placeholder="Last Name" className="input_field" value={lastName} onChange={e => setLastName(e.target.value)}/></div>
          <div className="input"><img src={email_icon} className="img_icon" alt=""/><input required aria-label="Email" autoComplete="email" type="email" name="email" placeholder="Email" className="input_field" value={email} onChange={e => setEmail(e.target.value)}/></div>
          <div className="input"><img src={password_icon} className="img_icon" alt=""/><input required aria-label="Password" autoComplete="new-password" name="psw" type="password" placeholder="Password" className="input_field" minLength={8} value={password} onChange={e => setPassword(e.target.value)}/></div>
        </div>
        {error && <p role="alert" style={{background: "white", color: "#9b1c1c", padding: "10px", borderRadius: "6px"}}>{error}</p>}
        <div className="submit_panel"><input className="submit" type="submit" disabled={pending} value={pending ? "Registering..." : "Register"}/></div>
        <p style={{textAlign: "center"}}>Already registered? <a href="/login/">Login</a></p>
      </form>
    </div>
  );
};

export default Register;
