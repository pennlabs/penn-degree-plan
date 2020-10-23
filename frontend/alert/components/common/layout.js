// import React from "react";
import styled from "styled-components";

export const Container = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
    background: rgb(251, 252, 255);
`;

export const Flex = styled.div`
    display: flex;
    margin: ${(props) => props.margin};
    padding: ${(props) => props.padding};
    text-align: ${(props) => (props.center ? "center" : null)};
    align-items: ${(props) => (props.valign ? "center" : null)};
    justify-content: ${(props) =>
        /* eslint-disable-next-line */
        props.halign ? "center" : props.spaceBetween ? "space-between" : null};
    flex-direction: ${(props) => (props.col ? "column" : "row")};
    flex-grow: ${(props) => props.grow || 0};
`;

export const Center = styled.div`
    text-align: center;
`;

export const GridItem = styled.div`
    display: flex;
    align-items: ${(props) => (props.valign ? "center" : null)};
    justify-content: ${(props) => (props.halign ? "center" : null)};
    grid-column: ${(props) => props.column};
    grid-row: ${(props) => props.row};
    background-color: ${(props) => (props.color ? props.color : "white")};
    border-bottom: ${(props) => (props.border ? "1px solid #ececec" : null)};
`;

export const RightItem = styled.div`
    height: 100%;
    display: flex;
    align-items: center;
    margin-left: auto;
`;