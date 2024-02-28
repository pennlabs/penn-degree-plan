import React, { useState, useRef, useEffect } from "react";
import { useDrop } from "react-dnd";
import { ItemTypes } from "../dnd/constants";
import CoursesPlanned from "./CoursesPlanned";
import Stats from "./Stats";
import styled from '@emotion/styled';
import { Course, DegreePlan, DnDFulfillment, Fulfillment } from "@/types";
import { postFetcher, useSWRCrud } from "@/hooks/swrcrud";
import { useSWRConfig } from "swr";
import { TrashIcon } from "../Requirements/ReqPanel";


const translateSemester = (semester: Course["semester"]) => {
    const year = semester.slice(0, 4);
    const term = semester.slice(4);
    return `${term === "A" ? "Spring" : term === "B" ? "Summer" : "Fall"} ${year}`
}

export const SemesterCard = styled.div<{$isDroppable:boolean, $isOver: boolean}>`
    background: #FFFFFF;
    box-shadow: 0px 0px 4px 2px ${props => props.$isOver ? 'var(--selected-color);' : props.$isDroppable ? 'var(--primary-color-dark);' : 'rgba(0, 0, 0, 0.05);'}
    border-radius: 10px;
    border-width: 0px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    flex: 1 1 15rem;
`;

const SemesterHeader = styled.div`
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
`

const SemesterLabel = styled.div`
    font-weight: 500;
`;

const SemesterContent = styled.div`
    margin-top: .5rem;
    display: flex;
    flex-direction: row;
    gap: 1rem;
`;

const FlexStats = styled(Stats)`
    flex-basis: 7rem;
    flex-grow: .1;
`;

const FlexCoursesPlanned = styled(CoursesPlanned)`
    flex-grow: 1;
`;

const CreditsLabel = styled.div`
    font-size: 1.2rem;
    font-weight: 500;
    margin-top: 1rem;
    margin-left: auto;
    margin-right: 0;
`;

interface SemesterProps {
    showStats: boolean;
    semester: string;
    fulfillments: Fulfillment[]; // fulfillments of this semester
    activeDegreeplanId: DegreePlan["id"] | undefined;
    className: string;
    editMode: boolean;
    setModalKey: (arg0: string) => void;
    setModalObject: (obj: any) => void;
    removeSemester: (sem: string) => void;
}

const FlexSemester = ({ showStats, semester, fulfillments, activeDegreeplanId, editMode, setModalKey, setModalObject, removeSemester} : SemesterProps) => {
    const credits = fulfillments.reduce((acc, curr) => acc + (curr.course?.credits || 1), 0)

    // the fulfillments api uses the POST method for updates (it creates if it doesn't exist, and updates if it does)
    const { createOrUpdate } = useSWRCrud<Fulfillment>(`/api/degree/degreeplans/${activeDegreeplanId}/fulfillments`, { idKey: "full_code" });

    const [{ isOver, canDrop }, drop] = useDrop<DnDFulfillment, never, { isOver: boolean, canDrop: boolean }>(() => ({
        accept: ItemTypes.COURSE,
        drop: (fulfillment: DnDFulfillment) => {
            console.log(semester, fulfillment)
            createOrUpdate({ semester, rules: fulfillment.rules }, fulfillment.full_code);
        },
        collect: monitor => ({
          isOver: !!monitor.isOver(),
          canDrop: !!monitor.canDrop()
        }),
    }), [createOrUpdate, semester]);

    const handleRemoveCourse = (full_code: Course["full_code"]) => {
        createOrUpdate({ semester: null }, full_code);
        /** API: add to dock */
        // setDockedCourses((dockedCourses:string[]) => [...dockedCourses, full_code]);
    }

    const removeSemesterHelper = () => {
        removeSemester(semester);
        console.log('fulfillments', fulfillments);
        for (var i = 0; i < fulfillments.length; i++) {
            console.log(fulfillments[i].full_code)
            createOrUpdate({ semester: null }, fulfillments[i].full_code);
        }
    }

    const handleRemoveSemester = () => {
        setModalKey('semester-remove');
        setModalObject({helper: removeSemesterHelper});
    }

    return (
        <SemesterCard $showStats={showStats} $isDroppable={canDrop} $isOver={isOver} ref={drop} >
            <SemesterHeader>
                <SemesterLabel>
                    {translateSemester(semester)}
                </SemesterLabel>
                {!!editMode &&         
                <TrashIcon role="button" onClick={handleRemoveSemester}>
                    <i className="fa fa-trash fa-md"/>
                </TrashIcon>}
            </SemesterHeader>
            <SemesterContent> 
                <FlexCoursesPlanned 
                    semester={semester} 
                    fulfillments={fulfillments} 
                    removeCourse={handleRemoveCourse}/>
                {!!showStats && <FlexStats fulfillments={fulfillments}/>}
            </SemesterContent>
            <CreditsLabel>
                {credits} CUs
            </CreditsLabel>
        </SemesterCard>
    )
}

export default FlexSemester;