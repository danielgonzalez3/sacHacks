import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Top from './topSection';
import { HomeLayout } from "./homePage";
import { ProtectedRoute } from "./protectedRoute";
import { TopSection } from "./topSection";

import { BrowserRouter, Route, Switch } from "react-router-dom";

import "./index.css";

/*
function App() {
  return (
    <div className="App">
      <Switch>
        <Route exact path="/" component={Login} />
        <ProtectedRoute exact path="/app" component={HomeLayout} />
        <Route path="*" component={() => "404 NOT FOUND"} />
      </Switch>
    </div>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
  rootElement
);
*/



ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);


