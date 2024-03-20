import React from "react"
import { Link } from "react-router-dom";

function Home() {
    return (
        <div>
            <h1>This is the home page!</h1>
            <Link to="/submit-post">Submit a post</Link>
        </div>
    )
}

export default Home