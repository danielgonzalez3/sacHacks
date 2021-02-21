import React, { useState } from "react";
import { Element, scroller } from "react-scroll";
import { Button } from "../components/button";
import "./topSection.css";
import { Navbar } from "../components/navBar";
import { Margin } from "../components/margin";
import { Logo } from "../components/logo";
import { DownArrow } from "../components/downArrow";

export function TopSection(props) {
    const scrollToNextSection = () => {
        scroller.scrollTo("servicesSection", { smooth: true, duration: 1500 });
    };

    return(
        <Element name="topSection">
            <div className = "topImageContainer" >
                <div className = "imageFilter"> 
                    <Navbar />
                    <Margin direction="vertical" margin="8em" />
                    <Logo />
                    <Margin direction="vertical" margin="4em" />
                    <h1 className = "bigText"> Project Jensen </h1>
                    <h1 className = "bigText"> the future of teaching software </h1>
                    <Margin direction="vertical" margin="4em" />
                    <Button>Better Teaching now.</Button>
                    <div className = "downArrowContainer" onClick={scrollToNextSection}>
                        <DownArrow/>
                    </div>
                </div>
            </div>
        </Element>
        
    );
}