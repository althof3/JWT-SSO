import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [logged_in, set_logged_in] = useState(false);
  const [user, setUser] = useState({});

  let DJANGO_SSO_LOGIN_URL = "http://127.0.0.1:8000/sso/login/?next=/sso/halo";
  let LOGIN_CALLBACK = "http://127.0.0.1:8000/sso/halo/";
  let SERVER = "http://127.0.0.1:8000";

  useEffect(() => {
    if (localStorage.getItem("token")) {
      fetch(`${SERVER}/sso/profile/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
        .then((res) => res.json())
        .then((json) => {
          setUser(json);
          set_logged_in(true)
        });
    } else {
      set_logged_in(false);
      setUser({})
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [logged_in]);

  useEffect(() => {
    window.addEventListener("message", receiveToken, false);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const receiveToken = (event) => {
    window.removeEventListener("message", () => null, false);

    if (event.origin !== `${SERVER}`) return;

    localStorage.setItem("token", event.data);
    set_logged_in(true);
  };

  const handle_logout = () => {
    localStorage.removeItem("token");
  };

  const handleLogin = () => {
    const loginWindow = window.open(
      DJANGO_SSO_LOGIN_URL,
      "_blank",
      "toolbar=no,scrollbars=yes,resizable=yes,width=500,height=800"
    );

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
          <a onClick={handle_logout} href={`${SERVER}/sso/logout`}>
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
