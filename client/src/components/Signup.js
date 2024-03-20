import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";

function Signup() {
  const history = useHistory();
  const [username, setUsername] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [image, setImage] = useState(null);
  const [bio, setBio] = useState("");

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleImageChange = (event) => {
    setImage(event.target.files[0]);
  };

  const handleBioChange = (event) => {
    setBio(event.target.value);
  };

  const handleSignupSubmit = async (event) => {
    event.preventDefault();
  
    try {
      const data = {
        username,
        name,
        email,
        password,
        image: image ? image.name : null,
        bio,
      };
  
      const response = await axios.post("/signup", data);
    
      setUsername("");
      setName("");
      setEmail("");
      setPassword("");
      setImage(null);
      setBio("");
  
      history.push("/home");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      <form onSubmit={handleSignupSubmit}>
        <label>
          Username:
          <input
            type="text"
            value={username}
            onChange={handleUsernameChange}
            maxLength={16}
          />
        </label>
        <br />
        <label>
          Name:
          <input 
            type="text" 
            value={name} 
            onChange={handleNameChange} 
            maxLength={16}
        />
        </label>
        <br />
        <label>
          Email:
          <input type="email" value={email} onChange={handleEmailChange} />
        </label>
        <br />
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={handlePasswordChange}
          />
        </label>
        <br />
        <label>
          Image:
          <input type="file" onChange={handleImageChange} />
        </label>
        <br />
        <label>
          Tell us about yourself!
          <textarea value={bio} onChange={handleBioChange} />
        </label>
        <br />
        <button type="submit">Signup</button>
      </form>
    </div>
  );
}

export default Signup;