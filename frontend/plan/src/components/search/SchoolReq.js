import React, { useState } from "react";
import PropTypes from "prop-types";

export function SchoolReq({ filterInfo, schoolReq }) {
    const schools = ["College", "Engineering", "Nursing", "Wharton"];
    const [selSchool, setSelSchool] = useState("College");

    const schoolCode = new Map();
    schoolCode.set("College", "SAS");
    schoolCode.set("Engineering", "SEAS");
    schoolCode.set("Wharton", "WH");
    schoolCode.set("Nursing", "NURS");

    const schoolHandleChange = (event) => {
        setSelSchool(event.target.value);
    };

    return (
        <div className="columns contained" id="schoolreq">
            <div className="column is-one-quarter">
                <p><strong>School</strong></p>
                <ul className="field">
                    {schools.map(school => (
                        <li>
                            <input
                                className="is-checkradio is-small"
                                id={school}
                                type="radio"
                                value={school}
                                checked={selSchool === school}
                                onChange={schoolHandleChange}
                            />
                            { /* eslint-disable-next-line jsx-a11y/label-has-for */ }
                            <label htmlFor={school}>{school}</label>
                        </li>
                    ))}
                </ul>
            </div>
            <div className="is-divider-vertical" />
            <div className="column">
                <p><strong>{`${selSchool} Requirements`}</strong></p>
                <ul className="field">
                    {schoolReq[schoolCode.get(selSchool)].map(req => (
                        <li>
                            <input
                                className="is-checkradio is-small"
                                id={req.id}
                                type="checkbox"
                                value={req.id}
                                checked={filterInfo[req.id] === 1}
                                onChange={() => {

                                }}
                            />
                            { /* eslint-disable-next-line jsx-a11y/label-has-for */ }
                            <label htmlFor={req.id}>{req.name}</label>
                        </li>
                    ))
                    }
                </ul>
            </div>
        </div>
    )
}