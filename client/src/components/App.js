import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Login from "./Login";
import Signup from "./Signup";
import Home from "./Home";
import FrontPage from "./FrontPage";
import Hobby from "./Hobbies";
import Post from "./Posts";
import SubmitPost from "./SubmitPost";
import EditPost from "./EditPost";

function App() {
  return (
    <Router>
      <div>
        <Switch>
          <Route exact path="/" component={FrontPage} />
          <Route exact path="/login" component={Login} />
          <Route exact path="/signup" component={Signup} />
          <Route exact path="/home" component={Home} />
          <Route exact path="/hobbies" component={Hobby} />
          <Route exact path="/posts" component={Post} />
          <Route exact path="/submit-post" component={SubmitPost} />
          <Route exact path="/edit-post/:postId" component={EditPost} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;