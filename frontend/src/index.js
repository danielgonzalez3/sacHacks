import React from 'react';
import ReactDOM from 'react-dom';
import Login from './Login';
const domain = process.env.REACT_APP_AUTH0_DOMAIN;
const clientId = process.env.REACT_APP_AUTH0_CLIENT_ID;

ReactDOM.render(
      <Login />,  
    document.getElementById('root')
);

