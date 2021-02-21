import React from "react";
import styled from "styled-components";
import { TopSection } from "./topSection";
import { Margin } from "../components/margin";
import { ServicesSection } from "./servicesSection";
import { Footer } from "../components/footer";

const PageContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
`;

export function Homepage(props) {
    return (
      <PageContainer>
        <TopSection />
        <ServicesSection />
        <Margin direction="vertical" margin="2em" />
        <Margin direction="vertical" margin="8em" />
        <Footer />
      </PageContainer>
    );
  }
  