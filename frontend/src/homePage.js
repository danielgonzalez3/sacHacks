import React from "react";
import auth from "./auth";

export const HomeLayout = props => {
  return (
    <div>
      <h1>Home Layout</h1>
      <button
        onClick={() => {
          auth.logout(() => {
            props.history.push("/");
          });
        }}
      >
        Logout
      </button>
    </div>
  );
};
