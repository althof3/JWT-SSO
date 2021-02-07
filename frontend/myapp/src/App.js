import React, { useState, useEffect } from "react";
import "./App.css";

function App() {

  const [logged_in, set_logged_in] = useState(false);
  const [user, setUser] = useState({})


  let DJANGO_SSO_LOGIN_URL = "http://127.0.0.1:8000/sso/login/?next=/sso/halo";
  let LOGIN_CALLBACK = "http://127.0.0.1:8000/sso/halo/";
  

  useEffect(() => {
    if (localStorage.getItem("token")) {
      fetch("http://127.0.0.1:8000/sso/profile/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => res.json())
        .then((json) => {
          setUser(json)
        });
    } 
  }, [logged_in]);
  
  useEffect(() => {
    window.addEventListener("message", receiveToken, false);
  }, []);

  const receiveToken = (event) => {
    window.removeEventListener('message', ()=>null, false);
    
    if (event.origin !== 'http://127.0.0.1:8000') return;

    localStorage.setItem('token', event.data);
    set_logged_in(true)

  };

  const handle_logout = () => {
    localStorage.removeItem("token");
    setUser({});
    set_logged_in(false);
  };

  const handleLogin = () => {
    const loginWindow = window.open(DJANGO_SSO_LOGIN_URL, "_blank", "toolbar=no,scrollbars=yes,resizable=yes,width=500,height=800");

    const getUserDataInterval = setInterval(() => {
      if (loginWindow.closed) {
        clearInterval(getUserDataInterval);
      }
      loginWindow.postMessage("ALTOP", LOGIN_CALLBACK);
    }, 1000);
  };

  return (
    <div className="App">
      <ul>
        <li>
          <a onClick={handle_logout} href="http://127.0.0.1:8000/sso/logout">
            Logout SSO
          </a>
        </li>
        <li>
          <button onClick={handleLogin}>Login SSO</button>
        </li>
      </ul>

      <h1>{user.name}</h1>
      <h4>{user.role}</h4>
    </div>
  );
}

export default App;

