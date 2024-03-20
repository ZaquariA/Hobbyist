import React, { useState } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";

function SubmitPost() {
  const [image, setImage] = useState("");
  const [description, setDescription] = useState("");
  const [comments, setComments] = useState("");
  const [submissionStatus, setSubmissionStatus] = useState(null);
  const history = useHistory();

  const handleImageChange = (event) => {
    setImage(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handleCommentsChange = (event) => {
    setComments(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
  
    if (!image || !description || !comments) {
      alert("Please fill in all required fields.");
      return;
    }
  
    try {
      const data = {
        image,
        description,
        comments,
      };
  
      const response = await axios.post("/posts", data);
  
      setImage("");
      setDescription("");
      setComments("");
      setSubmissionStatus("success");
  
    } catch (error) {
      console.error(error);
      setSubmissionStatus("error");
    }
  };

  const handleReturnHome = () => {
    history.push("/home");
  };

  return (
    <div>
      <h1>Post a post.</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Image:
          <input
            type="text"
            value={image}
            onChange={handleImageChange}
          />
        </label>
        <br />
        <label>
          Description:
          <textarea
            value={description}
            onChange={handleDescriptionChange}
          />
        </label>
        <br />
        <label>
          Comments:
          <textarea
            value={comments}
            onChange={handleCommentsChange}
          />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
      {submissionStatus === "success" && (
        <div>
          <p>Your post has been submitted!</p>
          <button onClick={handleReturnHome}>Return to Home</button>
        </div>
      )}
      {submissionStatus === "error" && (
        <p>There was an error submitting your post. Please try again.</p>
      )}
    </div>
  );
}

export default SubmitPost;