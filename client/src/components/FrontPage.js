import React from 'react';
import { Link } from 'react-router-dom';

function FrontPage() {
  return (
    <div>
      <h1>Welcome to The Hobbyist Hobbyists!</h1>
      <Link to="/login">Login</Link>
      <br />
      <Link to="/signup">Signup</Link>
    </div>
  );
}

export default FrontPage;