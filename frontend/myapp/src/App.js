import React, { useState, useEffect } from "react";
// import Nav from "./components/Nav";
// import LoginForm from "./components/LoginForms";
// import SignupForm from "./components/SignupForm";
import "./App.css";

import {
  BrowserRouter as Router,
  Switch,
  Route,
  // Link,
  useParams,
  Redirect,
} from "react-router-dom";

function App () {

  const [username, setusername] = useState('');
  const [logged_in, set_logged_in] = useState(false)

  useEffect(() => {
    if (logged_in) {
      fetch("http://127.0.0.1:8000/sso/profile/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => res.json())
        .then((json) => {
          console.log(json);
          setusername(json.data.name)
        });
    }
  }, [logged_in])

  const handle_logout = () => {
    localStorage.removeItem("token");
    setusername('')
    set_logged_in(false)
  }

  // display_form = (form) => {
  //   this.setState({
  //     displayed_form: form,
  //   });
  // };

  const openwindow = () => {
    window.open("http://127.0.0.1:8000/sso/login", "_blank", "toolbar=no,scrollbars=yes,resizable=yes,width=500,height=800");
  }

  return (
    <Router>
      <div className="App">
        <ul>
          <li>
            <a
              onClick={handle_logout}
              href="http://127.0.0.1:8000/sso/logout"
            >
              Logout SSO
            </a>
          </li>
          <li>
            <button onClick={openwindow}>Login SSO</button>
          </li>
        </ul>

        <Switch>
          <Route path="/token/:jwt">
            <Users loged={set_logged_in} />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
        <h1>{username}</h1>
      </div>
    </Router>
  )
}


export default App;

function Home() {
  return <h2>Home</h2>;
}

function Users(props) {
  let { jwt } = useParams();
  localStorage.setItem("token", jwt);

  useEffect(() => {
    props.loged(true)
  }, [props]);

  return (
    <Redirect
      to='/dashboard'
    />
  );
}
