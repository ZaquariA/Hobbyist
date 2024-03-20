import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, useHistory } from "react-router-dom";

function EditPost() {
  const { postId } = useParams();
  const history = useHistory();
  const [post, setPost] = useState({});
  const [image, setImage] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await axios.get(`/posts/${postId}`);
        setPost(response.data);
        setImage(response.data.image);
        setDescription(response.data.description);
      } catch (error) {
        console.error(error);
      }
    };

    fetchPost();
  }, [postId]);

  const handleImageChange = (event) => {
    setImage(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      await axios.patch(`/posts/${postId}`, {
        image,
        description,
      });
      history.push("/posts"); // Redirect to the posts page after updating
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Edit Post</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Image:
          <input type="text" value={image} onChange={handleImageChange} />
        </label>
        <br />
        <label>
          Description:
          <textarea
            value={description}
            onChange={handleDescriptionChange}
          ></textarea>
        </label>
        <br />
        <button type="submit">Update Post</button>
      </form>
    </div>
  );
}

export default EditPost;