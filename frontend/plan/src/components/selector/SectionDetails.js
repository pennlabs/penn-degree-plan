import React from "react";
import PropTypes from "prop-types";

import "bulma-popover/css/bulma-popver.min.css";

import { getTimeString } from "../../meetUtil";

const getSectionId = id => (tokens => tokens[tokens.length - 1])(id.split("-"));

const getClassCode = id => (tokens => tokens.slice(0, tokens.length - 1).join("-"))(id.split("-"));

export default function SectionDetails({ section, isOpen }) {
    const { id, instructors, meetings } = section;
    return (
        <li style={{ display: isOpen ? "block" : "none" }}>
            <div style={{ margin: ".5em .5em .5em 3.25em", maxHeight: "40%", fontSize: ".75em", display: "block" }}>
                <h3 className="title is-6 section-details-title">
                    <b>{`${getSectionId(id)}`}</b>
                    &nbsp;&nbsp;
                    <p>
                        {instructors.map((elem, ind) => <>
                            {ind !== 0 ? <br /> : null}
                            {ind !== instructors.length - 1 ? `${elem},` : elem}
                        </>)}
                    </p>
                </h3>
                <span className="popover is-popover-right">
                    <span className="popover-trigger">
                        <a
                            href={`https://penncoursereview.com/course/${getClassCode(id)}`}
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            <img className="pcr-svg" src="https://danxtao.com/assets/pcr.svg" />
                        </a>
                    </span>
                    <span className="popover-content">
                        View course on Penn Course Review
                    </span>
                </span>
                <br />
                <i className="far fa-clock grey-text" />
                &nbsp;
                {getTimeString(meetings)}
                &nbsp;&nbsp;
                <i className="fas fa-map-marker-alt grey-text" />
                &nbsp;
                {meetings.map(m => m.room).join(", ")}
            </div>
        </li>
    );
}

SectionDetails.propTypes = {
    // eslint-disable-next-line
    section: PropTypes.object.isRequired,
    isOpen: PropTypes.bool.isRequired,
};
