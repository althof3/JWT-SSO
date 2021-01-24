import React, { Component } from "react";
// import Nav from "./components/Nav";
// import LoginForm from "./components/LoginForms";
// import SignupForm from "./components/SignupForm";
import "./App.css";

import { 
  BrowserRouter as Router, 
  Switch, 
  Route, 
  // Link,
  useParams
} from "react-router-dom";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      displayed_form: "",
      logged_in: localStorage.getItem("token") ? true : false,
      username: "",
    };
  }

  componentDidMount() {
    if (this.state.logged_in) {
      fetch("http://127.0.0.1:8000/sso/profile/?format=json", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => res.json())
        .then((json) => {
          console.log(json);
          this.setState({ username: json.data.name });
        });
    }
  }

  handle_login = (e, data) => {
    e.preventDefault();
    fetch("http://localhost:8000/token-auth/", {
      // mode: 'no-cors',
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((json) => {
        localStorage.setItem("token", json.token);
        this.setState({
          logged_in: true,
          displayed_form: "",
          username: json.user.username,
        });
        console.log(this.state);
      });
  };

  handle_signup = (e, data) => {
    e.preventDefault();
    fetch("http://localhost:8000/core/users/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((json) => {
        localStorage.setItem("token", json.token);
        this.setState({
          logged_in: true,
          displayed_form: "",
          username: json.username,
        });
      });
  };

  handle_logout = () => {
    localStorage.removeItem("token");
    this.setState({ logged_in: false, username: "" });
  };

  display_form = (form) => {
    this.setState({
      displayed_form: form,
    });
  };

  // haha = () => {
  //   fetch("http://localhost:8000/sso/profile/", {
  //     headers: {
  //       Authorization: `JWT ${localStorage.getItem("token")}`,
  //     },
  //   })
  //     .then((res) => res.json())
  //     .then((json) => {
  //       console.log(json);
  //       // this.setState({ username: json.username });
  //     });
  // };

  render() {
    // let form;
    // switch (this.state.displayed_form) {
    //   case "login":
    //     form = <LoginForm handle_login={this.handle_login} />;
    //     break;
    //   case "signup":
    //     form = <SignupForm handle_signup={this.handle_signup} />;
    //     break;
    //   default:
    //     form = null;
    // }

    // this.haha();

    return (
      <Router>
        <div className="App">
          {/* <Nav
            logged_in={this.state.logged_in}
            display_form={this.display_form}
            handle_logout={this.handle_logout}
          /> */}
          {/* {form} */}
          {/* {this.haha} */}

          <ul>
            
            
               <li>
                  <a onClick={this.handle_logout} href="http://127.0.0.1:8000/sso/logout">Logout SSO</a>
                </li>
               <li>
                  <a href="http://127.0.0.1:8000/sso/login">Login SSO</a>
                </li>
            
            
          </ul>
          

          <Switch>
            <Route path="/token/:jwt">
              <Users />
            </Route>
            <Route path="/">
              <Home />
            </Route>
          </Switch>
          <h1>{this.state.username}</h1>
        </div>
      </Router>
    );
  }
}

export default App;


function Home() {
  return <h2>Home</h2>;
}


function Users() {

  let {jwt} = useParams()
  localStorage.setItem("token", jwt);

  return <h3>
          {`Hello`}
          {localStorage.getItem('token')}
        </h3>;
}