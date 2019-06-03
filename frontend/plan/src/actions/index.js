import fetch from "cross-fetch";

export const UPDATE_SEARCH = "UPDATE_SEARCH";

export const UPDATE_COURSE_INFO = "UPDATE_COURSE_INFO";
export const UPDATE_SECTIONS = "UPDATE_SECTIONS";
export const OPEN_SECTION_INFO = "OPEN_SECTION_INFO";
export const CHANGE_SCHEDULE = "CHANGE_SCHEDULE";
export const CREATE_SCHEDULE = "CREATE_SCHEDULE";


export const TOGGLE_SEARCH_FILTER = "TOGGLE_SEARCH_FILTER";
export const OPEN_MODAL = "OPEN_MODAL";
export const CLOSE_MODAL = "CLOSE_MODAL";
export const ACTION_BUTTON_PRESSED = "ACTION_BUTTON_PRESSED";

export const ADD_SCHED_ITEM = "ADD_SCHED_ITEM";
export const REMOVE_SCHED_ITEM = "REMOVE_SCHED_ITEM";
export const DELETE_SCHEDULE = "DELETE_SCHEDULE";
export const RENAME_SCHEDULE = "RENAME_SCHEDULE";
export const DUPLICATE_SCHEDULE = "DUPLICATE_SCHEDULE";
export const CLEAR_SCHEDULE = "CLEAR_SCHEDULE";

export const COURSE_SEARCH_ERROR = "COURSE_SEARCH_ERROR";
export const COURSE_SEARCH_LOADING = "COURSE_SEARCH_LOADING";
export const COURSE_SEARCH_SUCCESS = "COURSE_SEARCH_SUCCESS";
export const REQUEST_SEARCH = "REQUEST_SEARCH";

export const SECTION_INFO_SEARCH_ERROR = "SECTION_INFO_SEARCH_ERROR";
export const SECTION_INFO_SEARCH_LOADING = "SECTION_INFO_SEARCH_LOADING";
export const SECTION_INFO_SEARCH_SUCCESS = "SECTION_INFO_SEARCH_SUCCESS";
export const REQUEST_SECTION_INFO_SEARCH = "REQUEST_SECTION_INFO_SEARCH";


export const duplicateSchedule = scheduleName => (
    {
        type: DUPLICATE_SCHEDULE,
        scheduleName,
    }
);

export const deleteSchedule = () => (
    {
        type: DELETE_SCHEDULE,
    }
);

export const renameSchedule = scheduleName => (
    {
        type: RENAME_SCHEDULE,
        scheduleName,
    }
);

export const changeSchedule = scheduleId => (
    {
        type: CHANGE_SCHEDULE,
        scheduleId,
    }
);

export const addSchedItem = courseObj => (
    {
        type: ADD_SCHED_ITEM,
        courseObj,
    }
);

export const removeSchedItem = id => (
    {
        type: REMOVE_SCHED_ITEM,
        id,
    }
);

export const updateSearch = searchResults => (
    {
        type: UPDATE_SEARCH,
        searchResults,
    }
);

export const updateSections = sections => (
    {
        type: UPDATE_SECTIONS,
        sections,
    }
);

export const updateSectionInfo = sectionInfo => (
    {
        type: OPEN_SECTION_INFO,
        sectionInfo,
    }
);

export const updateCourseInfo = course => (
    {
        type: UPDATE_COURSE_INFO,
        course,
    }
);

export const createSchedule = scheduleName => (
    {
        type: CREATE_SCHEDULE,
        scheduleName,
    }
);

export const toggleSearchFilterShown = location => (
    {
        type: TOGGLE_SEARCH_FILTER,
        location,
    }
);


export const openModal = modalShown => (
    {
        type: OPEN_MODAL,
        modalShown,
    }
);


export const closeModal = () => (
    {
        type: CLOSE_MODAL,
    }
);

export const triggerModalAction = modalAction => (
    {
        type: ACTION_BUTTON_PRESSED,
        modalAction,
    }
);

export const clearSchedule = () => (
    {
        type: CLEAR_SCHEDULE,
    }
);

function buildCourseSearchUrl(searchData) {
    return `/courses/?search=${searchData.param}`;
}

function buildSectionInfoSearchUrl(searchData) {
    return `/courses/${searchData.param}`;
}


export function courseSearchError(error) {
    return {
        type: COURSE_SEARCH_ERROR,
        error,
    };
}

export function sectionInfoSearchError(error) {
    return {
        type: SECTION_INFO_SEARCH_ERROR,
        error,
    };
}

export function fetchCourseSearch(searchData) {
    return dispatch => (
        fetch(buildCourseSearchUrl(searchData)).then(
            response => response.json().then(
                json => dispatch(updateSearch(json)),
                error => dispatch(courseSearchError(error)),
            ),
            error => dispatch(courseSearchError(error)),
        )
    );
}

export function fetchCourseDetails(courseId) {
    return dispatch => (
        fetch(`/courses/${courseId}`)
            .then(res => res.json())
            .then(course => dispatch(updateCourseInfo(course)))
            .catch(error => dispatch(sectionInfoSearchError(error)))
    );
}

export function fetchSectionInfo(searchData) {
    return dispatch => (
        fetch(buildSectionInfoSearchUrl(searchData)).then(
            response => response.json().then(
                (json) => {
                    const info = {
                        id: json.id,
                        description: json.description,
                        crosslistings: json.crosslistings,
                    };
                    const { sections } = json;
                    dispatch(updateCourseInfo(sections, info));
                },
                error => dispatch(sectionInfoSearchError(error)),
            ),
            error => dispatch(sectionInfoSearchError(error)),
        )
    );
}

export function courseSearchLoading() {
    return {
        type: COURSE_SEARCH_LOADING,
    };
}

export function courseSearchSuccess(items) {
    return {
        type: COURSE_SEARCH_SUCCESS,
        items,
    };
}
