import React, { useState } from "react";
import PropTypes from "prop-types";
import { validateScheduleName } from "../schedule/schedule_name_validation";

const CreateScheduleModalInterior = ({ usedScheduleNames, createSchedule, close }) => {
    const [inputRef, setInputRef] = useState(null);
    const [userInput, setUserInput] = useState("");
    const {error, message: errorMessage} = validateScheduleName(userInput, usedScheduleNames);
    return <div>
        <input type={"text"} ref={ref => setInputRef(ref)}
               onChange={() => setUserInput(inputRef.value)}/>
        <p>{errorMessage}</p>
        <div role={"button"} onClick={() => {
            const scheduleName = inputRef.value;
            if (!error) {
                createSchedule(scheduleName);
                close();
            }
        }}>Create</div>
    </div>;
};

CreateScheduleModalInterior.propTypes = {
    usedScheduleNames: PropTypes.arrayOf(PropTypes.string).isRequired,
    createSchedule: PropTypes.func,
    close: PropTypes.func,
};

export default CreateScheduleModalInterior;
