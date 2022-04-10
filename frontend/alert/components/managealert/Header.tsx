import React from "react";
import styled from "styled-components";
import {
    GridItem,
    Flex,
    RightItem,
} from "pcx-shared-components/src/common/layout";
import { Img } from "../common/common";
import { AlertAction } from "../../types";
import { maxWidth, PHONE } from "../../constants";
import DropdownTool from "./DropdownTool";

const Grid = styled.div<{ selected: boolean }>`
    display: grid;
    grid-template-columns: ${({ selected }) =>
        selected ? "1fr 10.5fr" : "1fr 1fr 3fr 1fr 1fr 1fr 2.5fr 1fr"};
    grid-template-rows: 1.5rem;

    ${maxWidth(PHONE)} {
        grid-template-columns: 0fr 0fr 2.5fr 2fr 0.5fr 3.5fr 0fr 1fr;
        & > div:nth-child(0) {
            display: none;
        }
        & > div:nth-child(8n + 1) {
            display: none;
        }
        & > div:nth-child(8n + 2) {
            display: none;
        }
        & > div:nth-child(8n + 7) {
            display: none;
        }
    }
`;

const HeaderText = styled.p`
    font-size: 0.7rem;
    font-weight: bold;
    color: ${(props) => (props.color ? props.color : "#9ea0a7")};
    text-align: center;
`;

const HeaderAction = styled(HeaderText)`
    margin-right: 1rem;
    cursor: pointer;
    color: #489be8;
`;

const HeaderButtonsFlex = styled(Flex)`
    & > * {
        display: block;
        margin-right: 0.4rem;
    }
`;

const HeaderContainer = styled.div`
    display: flex;
    align-items: center;

    ${maxWidth(PHONE)} {
        display: flex;
        align-items: center;
    }
`;

const Separator = styled.div`
    margin: 0rem 1rem 0rem 1rem;
`;

interface HeaderProps {
    selected: number;
    batchActionHandler: (action: AlertAction) => void;
    batchSelectHandler: (select: boolean) => void;
    setBatchSelected: (select: boolean) => void;
    batchSelected: boolean;
}
// Component for table header in alert management
// Renders column titles or "x selected" depending
// on if alerts are selected
const Header = ({
    selected,
    batchActionHandler,
    batchSelectHandler,
    batchSelected,
    setBatchSelected,
}: HeaderProps) => {
    const headings = [
        "LAST NOTIFIED",
        "COURSE ID",
        "STATUS",
        "",
        "SUBSCRIPTION",
        "NOTIFY WHEN CLOSED",
        ""
    ];

    return (
        <Grid selected={selected !== 0}>
            <GridItem column={1} row={1} color="#f8f8f8" halign valign border>
                <input
                    type="checkbox"
                    checked={batchSelected}
                    onChange={() => {
                        batchSelectHandler(batchSelected);
                        setBatchSelected(!batchSelected);
                    }}
                />
            </GridItem>
            {selected === 0 &&
                headings.map((heading, i) => (
                    <GridItem
                        // eslint-disable-next-line
                        key={`header${i}`}
                        column={i + 2}
                        row={1}
                        color="#f8f8f8"
                        valign
                        halign
                        border
                    >
                        <HeaderText>{heading}</HeaderText>
                    </GridItem>
                ))}
            {selected !== 0 && (
                <>
                    <GridItem column={2} row={1} color="#f8f8f8" valign>
                        <HeaderContainer>
                            <HeaderText color="#489be8">{`${selected} SELECTED`}</HeaderText>
                            <Separator style={{ color: "#878787" }}>
                                |
                            </Separator>
                            <DropdownTool
                                actionsText={[
                                    "Alerts",
                                    "Toggle On",
                                    "Toggle Off",
                                ]}
                                functions={[
                                    () =>
                                        batchActionHandler(AlertAction.ONALERT),
                                    () =>
                                        batchActionHandler(
                                            AlertAction.OFFALERT
                                        ),
                                ]}
                                width={"5"}
                            />

                            <DropdownTool
                                actionsText={[
                                    "Notify when Closed",
                                    "Toggle On",
                                    "Toggle Off",
                                ]}
                                functions={[
                                    () =>
                                        batchActionHandler(
                                            AlertAction.ONCLOSED
                                        ),
                                    () =>
                                        batchActionHandler(
                                            AlertAction.OFFCLOSED
                                        ),
                                ]}
                                width={"8"}
                            />
                            <HeaderButtonsFlex valign>
                                <Img
                                    src="/svg/trash.svg"
                                    width="0.5rem"
                                    height="0.5rem"
                                />
                                <HeaderAction
                                    onClick={() =>
                                        batchActionHandler(AlertAction.DELETE)
                                    }
                                >
                                    DELETE
                                </HeaderAction>
                            </HeaderButtonsFlex>
                        </HeaderContainer>
                    </GridItem>
                </>
            )}
        </Grid>
    );
};

export default Header;
