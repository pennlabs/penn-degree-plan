import { useDrag } from "react-dnd";
import { ItemTypes } from "../dnd/constants";
import { GrayIcon } from '../common/bulma_derived_components';
import styled from '@emotion/styled';
import { Course, DnDCourse, DockedCourse, Fulfillment } from "@/types";
import { Draggable } from "../common/DnD";
import CourseComponent, { PlannedCourseContainer } from "../Course/Course";
import { CourseXButton } from "../Course/Course";
import { useSWRCrud } from "@/hooks/swrcrud";

interface CourseInDockProps {
    course: DnDCourse;
    isDisabled: boolean;
    className?: string;
    onClick?: () => void;
  }

const CourseInDock = (props : CourseInDockProps) => {
    const { course } = props;

    const { remove } = useSWRCrud<DockedCourse>(`/api/degree/docked`, { idKey: 'full_code' });
    const handleRemoveCourse = (full_code: string) => {
      remove(full_code);
    }

    const [{ isDragging }, drag] = useDrag<DnDCourse, never, { isDragging: boolean }>(() => ({
      type: ItemTypes.COURSE_IN_DOCK,
      item: course,
      collect: (monitor) => ({
        isDragging: !!monitor.isDragging()
      })
    }), [course])
  
    return (
      <CourseComponent dragRef={drag} isDragging={isDragging} removeCourse={handleRemoveCourse} isUsed {...props} />
    )
  }
  
  
  export default CourseInDock;