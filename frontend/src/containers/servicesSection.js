import React from "react";
import { Element } from "react-scroll";
import styled from "styled-components";
import { Margin } from "../components/margin";
import { OurSerivce } from "../components/ourService";
import { SectionTitle } from "../components/sectionTitle";

// INSTEAD OF Service1Img ADD THE GRAPHS/METRICS
import Service1Img from "../images/proof_of_concept_pj.png";
import Service2Img from "../images/mobile_phone.png";
import Service3Img from "../images/bug_fixed.png";

const ServicesContainer = styled(Element)`
  width: 100%;
  min-height: 1100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0;
`;

export function ServicesSection(props) {
  return (
    <ServicesContainer name="servicesSection">
      <SectionTitle>Bridge the Education Gap</SectionTitle>
      <Margin direction="vertical" margin="3em" />
      <OurSerivce
        title="Proof of Concept:"
        description="Jensen is a versatile app built to support educators by 
        providing a suite of tools that can be used to bring the classroom 
        to the student. Jensen is driven to make virtual learning work for students."
        imgUrl={Service1Img}
      />
      <OurSerivce
        title="Mobile optimized"
        description="We build and deliver fully integrated webapps
          with customized control panels that fit your 
          compnay needs"
        imgUrl={Service2Img}
        isReversed
      />
      <OurSerivce
        title="Quality is our priority"
        description="We have teams of professional developers, designers
        and managers that ensures delivering the best 
        software quality for your company"
        imgUrl={Service3Img}
      />
    </ServicesContainer>
  );
}
