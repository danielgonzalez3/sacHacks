import React from "react";
import auth from "./auth";

export const LoginButton = props => {
  return (
    <div>
      <button
        block size="lg" 
        type="submit" 
        onClick={() => {
          auth.login(() => {
            props.history.push("/app");
          });
        }}
      >
        Login
      </button>
    </div>
  );
};