import React, { useEffect, useState } from "react";
import axios from "axios";

function Post() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // Fetch the posts data
    const fetchPosts = async () => {
      try {
        const response = await axios.get("/posts");
        setPosts(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchPosts();
  }, []);

  return (
    <div>
      <h1>Posts</h1>
      {posts.map((post) => (
        <div key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.description}</p>
          <img src={post.image}></img>
        </div>
      ))}
    </div>
  );
}

export default Post;