import React, { useState, useEffect } from "react";
import axios from "axios";

function Hobby() {
  const [hobbies, setHobbies] = useState([]);

  useEffect(() => {
    const fetchHobbies = async () => {
      try {
        const response = await axios.get("/hobbies");
        setHobbies(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchHobbies();
  }, []);

  return (
    <div>
      <h1>Hobbies</h1>
      {hobbies.map((hobby) => (
        <div key={hobby.id}>
          <h2>{hobby.name}</h2>
          <p>{hobby.description}</p>
          <img src={hobby.image}></img>
        </div>
      ))}
    </div>
  );
}

export default Hobby;