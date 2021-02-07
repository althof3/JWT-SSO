import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [username, setusername] = useState("");
  const [logged_in, set_logged_in] = useState(false);


  let DJANGO_SSO_LOGIN_URL = "http://127.0.0.1:8000/sso/login/?next=/sso/halo";
  let LOGIN_CALLBACK = "http://127.0.0.1:8000/sso/halo/";
  

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
          setusername(json.data.name);
        });
    } 
  }, [logged_in]);
  
  useEffect(() => {
    window.addEventListener("message", receiveToken, false);
  }, []);

  const receiveToken = (event) => {
    window.removeEventListener('message', ()=>null, false);
    
    if (typeof(event.data) !== 'string') return;

    localStorage.setItem('token', event.data);
    set_logged_in(true)

  };

  const handle_logout = () => {
    localStorage.removeItem("token");
    setusername("");
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

      <h1>{username}</h1>
    </div>
  );
}

export default App;

