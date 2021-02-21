import React from "react";
import styled, { css } from "styled-components";

import JensenLogo from "../images/logo.png";
import { theme } from "../theme";

const LogoContainer = styled.div`
  display: flex;
  flex-direction: ${({ inline }) => (inline ? "row" : "column")};
  align-items: center;
`;

const LogoImg = styled.img`
  width: 8em;
  height: 6.5em;

  ${({ inline }) =>
    inline &&
    css`
      width: 30px;
      height: 27px;
      margin-right: 6px;
    `};

  ${({ small }) =>
    small &&
    css`
      width: 6em;
      height: 5em;
    `};
`;

const LogoText = styled.div`
  margin-top: ${({ inline }) => (inline ? 0 : "6px")};
  font-size: ${({ inline, small }) =>
    inline ? "18px" : small ? "23px" : "40px"};
  color: ${({ inline }) => (inline ? "#fff" : theme.primary)};
  font-weight: 900;
`;

export function Logo(props) {
  const { inline, small } = props;

  return (
    <LogoContainer inline={inline} small={small}>
      <LogoImg src={JensenLogo} inline={inline} small={small} />
      <LogoText inline={inline} small={small}>
        Jensen
      </LogoText>
    </LogoContainer>
  );
}
