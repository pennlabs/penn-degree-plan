import React, { useState } from "react";
import { useOnClickOutside } from "./useOnClickOutside";
import PropTypes from "prop-types";

export function DropdownButton({ title, children }) {
    const [isActive, setIsActive] = useState(false);

    const toggleButton = () => {
        if (isActive) {
            setIsActive(false);
        } else {
            setIsActive(true);
        }
    };

    const ref = useOnClickOutside(toggleButton, !isActive);

    return (
        <div
            className={`dropdown ${isActive ? "is-active" : ""}`}
            ref={ref}
        >
            <div className="dropdown-trigger">
                <button
                    className="button is-rounded"
                    aria-haspopup="true"
                    aria-controls="dropdown-menu"
                    onClick={toggleButton}
                    type="button"
                >
                    <span>
                        {title}
                    </span>
                </button>
            </div>
            <div className="dropdown-menu" id="dropdown-menu" role="menu">
                <div className="dropdown-content">
                    {/* This injects the setIsActive method to allow children */}
                    {/* to change state of dropdown  */}
                    {React.Children.map(children, c => (
                        React.cloneElement(c, {
                            setIsActive,
                        })
                    ))}
                </div>
            </div>
        </div>
    )
}