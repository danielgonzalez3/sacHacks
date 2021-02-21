import React from "react";
import { Button } from "./button";
import { Logo } from "./logo";
import { Margin } from "./margin";
import "./navBar.css";
import styled from "styled-components";

export function Navbar(props){
    return(
        <div className = "navBarContainer"> 
            <div> 
                <Logo inline />
            </div>
            <div className = "buttonContainer">
                <Button small> Get Started </Button>
                <Margin direction="horizontal" margin="8px" />
                <Button small className = "styledButton">Button</Button>
            </div>
        </div>
    );
}