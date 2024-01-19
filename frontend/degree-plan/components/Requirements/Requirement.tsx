// interface IRequirement {
//     req: [ICourse]
// }
import Icon from '@mdi/react';
import { mdiArrowDown, mdiArrowUp, mdiEye, mdiLightSwitch, mdiLightbulb, mdiLightbulbOutline, mdiMagnify, mdiMenuDown, mdiMenuUp } from '@mdi/js';
import { titleStyle } from "@/pages/FourYearPlanPage";
import Course from "./Course";
import { useState } from 'react';
import RootQObj , { trimQuery } from './QObj';

/* Recursive component */
const Requirement = ({requirement, setSearchClosed, parent, handleSearch, setHighlightReqId, highlightReqId} : any) => {
    const [collapsed, setCollapsed] = useState(true);

    const handleShowSatisfyingCourses = () => {
        console.log(highlightReqId);
        if (highlightReqId === requirement.id) 
            setHighlightReqId(-1);
        else 
        setHighlightReqId(requirement.id);
    }

    return (
        <>
            {parent === requirement.parent && 
            (requirement.q || requirement.title) &&
            <div>
            
                    {requirement.q ? 
                    <label className="mb-2 col-12 justify-content-between d-flex" style={{
                        backgroundColor:'#EFEFEF', 
                        fontSize:'16px', 
                        padding:'2px', 
                        paddingLeft:'15px', 
                        borderRadius:'8px',
                    }}>
                        <div style={titleStyle}>
                            <RootQObj query={trimQuery(requirement.q)} reqId={requirement.id}/>
                        </div>
                        <div className='d-flex'>
                            <div onClick={handleShowSatisfyingCourses}>
                                <Icon path={mdiEye} size={1} color={highlightReqId === requirement.id ? 'yellow': '#575757'}/>
                            </div>
                            <div onClick={() => {setSearchClosed(false); handleSearch(requirement.id);}}>
                                <Icon path={mdiMagnify} size={1} color='#575757'/>
                            </div>
                        </div>
                    </label>
                    :
                    <label className="mb-2 col-12 justify-content-between d-flex" style={{
                        backgroundColor:'#EFEFEF', 
                        fontSize:'16px', 
                        padding:'2px', 
                        paddingLeft:'15px', 
                        borderRadius:'8px',
                    }}>
                        <div onClick={() => setCollapsed(!collapsed)} className='col-12 d-flex justify-content-between'>
                            <div style={titleStyle}>
                                {requirement.title}
                            </div>
                            <div>
                                {requirement.rules.length && 
                                    <Icon path={collapsed ? mdiMenuDown : mdiMenuUp} size={1} color='#575757'/>
                                }
                            </div>
                        </div>
                    </label>
                    }
                {!collapsed && <div className="ms-3">
                    {requirement.rules.map((rule: any, index: number) => 
                        <Requirement requirement={rule} setSearchClosed={setSearchClosed} parent={requirement.id} handleSearch={handleSearch} setHighlightReqId={setHighlightReqId} highlightReqId={highlightReqId}/>
                    )}
                </div>}
            </div>}
        </>
    )
}

export default Requirement;