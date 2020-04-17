import React from "react";
import styled from "styled-components";
import PropTypes from "prop-types";
import XBell from "../../assets/bell-off.svg";
import Trash from "../../assets/trash.svg";
import ABell from "../../assets/abell.svg";
import {
    GridItem, Flex, RightItem, Img
} from "./ManageAlertStyledComponents";

const HeaderText = styled.p`
    font-size: 0.7rem;
    font-weight: bold;
    color: ${props => (props.color ? props.color : "#9ea0a7")};
`;

const HeaderAction = styled(HeaderText)`
    margin-right: 1rem;
    cursor: pointer;
`;

const HeaderButtonsFlex = styled(Flex)`
    & > * {
        display: block;
        margin-right: 0.4rem;
    }
`;

const HeaderRightItem = styled(RightItem)`
    margin-right: 0.5rem;
`;

const Header = ({ selected }) => {
    const headings = ["LAST NOTIFIED", "COURSE ID", "STATUS", "REPEAT", "ACTIONS"];

    return (
        <>
            <GridItem column="1" row="1" color="#f8f8f8" halign valign>
                <input type="checkbox" />
            </GridItem>
            {!selected
             && headings.map((heading, i) => (
                 // eslint-disable-next-line
                 <GridItem key={`header${i}`} column={(i + 2).toString()} row="1" color="#f8f8f8" valign>
                     <HeaderText>{heading}</HeaderText>
                 </GridItem>
             ))}

            {selected
             && (
                 <>
                     <GridItem column="2" row="1" color="#f8f8f8" valign>
                         <HeaderText color="#489be8">{`${selected} SELECTED`}</HeaderText>
                     </GridItem>
                     <GridItem column="3/7" row="1" color="#f8f8f8" valign>
                         <HeaderRightItem>
                             <HeaderButtonsFlex valign>
                                 <Img src={ABell} width="0.5rem" height="0.5rem" />
                                 <HeaderAction>RESUBSCRIBE</HeaderAction>
                             </HeaderButtonsFlex>
                             <HeaderButtonsFlex valign>
                                 <Img src={XBell} width="0.5rem" height="0.5rem" />
                                 <HeaderAction>CANCEL</HeaderAction>
                             </HeaderButtonsFlex>
                             <HeaderButtonsFlex valign>
                                 <Img src={Trash} width="0.5rem" height="0.5rem" />
                                 <HeaderAction>DELETE</HeaderAction>
                             </HeaderButtonsFlex>
                         </HeaderRightItem>
                     </GridItem>
                 </>
             )}
        </>
    );
};

Header.propTypes = { selected: PropTypes.number };

export default Header;
