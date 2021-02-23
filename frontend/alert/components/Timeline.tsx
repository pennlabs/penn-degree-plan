import React, {useEffect} from 'react';
import styled from "styled-components";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTimes, faCircle } from '@fortawesome/free-solid-svg-icons'


const AlertHistoryContainer = styled.div`
  position: absolute;
  right: 0px;
  top: 0;
  width: 14vw;
  min-width: 200px;
  height: 100vh;
  padding: 32px 32px;
  box-shadow: 0px 4px 18px rgba(0, 0, 0, 0.08);;
  background: white;
  transition: 0.5s all;
  z-index: 100;
`

const CloseButton = styled.button`
  outline: none;
  border: none;
  background: none;
  position: absolute;
  right: 23px;
  top: 25px;
  font-size: 20px;
  color: rgba(157,157,157,1);
  i {
    color: #9d9d9d;
    transition: 0.2s;
    :hover{
      color: #5a5a5a;
    }
  }
`

const CourseInfoContainer = styled.div`
  display: flex;
  justify-content: left;
  align-items: center;
  flex-direction: row;
  margin-top: 6px;
  margin-bottom: 30px;
`

const AlertTitle = styled.h3`
  font-size: 22px;
  color: rgba(40,40,40,1);
  margin-bottom: 0px;
  padding-bottom: 0px;
  margin-top: 16px;
`

const CourseSubHeading = styled.h5`
  font-size: 15px;
  color: rgba(40,40,40,1);
  margin-bottom: 0px;
  margin-top: 0px;
  margin-right: 10px;
  font-weight: normal;
`

const StatusLabel = styled.div`
  height: 23px;
  border-radius: 3px;
  font-weight: 600;
  color: #e8746a;
  background: #f9dcda;
  font-size: 12px;
  text-align: center;
  line-height: 24px;
  padding: 0px 5px;
`

const TimelineContainer = styled.div`
  display: flex;
  justify-content: flex-start;
  align-items: center;
  overflow-y: scroll;
  height: calc(100vh - 150px);
  flex-direction: column;

  &::-webkit-scrollbar { 
    display: none; 
  } 
`

type CircleProps = {
  open: boolean;
}

const Circle = styled.div<CircleProps>`
  height: 14px;
  width: 14px;
  border: 1px solid ${({open}) => open ? "#78D381" : "#cbd5dd"};
  border-radius: 50%;
  color: ${({open}) => open ? "#78D381" : "#cbd5dd"};
  font-size: 10px;
  text-align: center;
  vertical-align: middle;
  line-height: 14px;
`

type SegmentProps = {
  open: boolean
  length: number;
}

const Segment = styled.div<SegmentProps>`
  background-color: ${({open}) => open ? "#78D381" : "#cbd5dd"};
  height: ${({length}) => length}px;
  width: 3px;
`


// const Center = styled.div`
//   display: flex;
//   align-items: center;
//   flex-direction: column;
// `


// const Segment = styled.div`
//   width: 2px;
//   height: ${props=>props.height + 5}px;
//   background: ${props=>props.type=="opened" ? "#78d381" : "#cbd5dd"};
// `
// const MyCircle = styled.div`
//   color: ${props=>props.type=="opened" ? "#78d381" : "#cbd5dd"};
// `

// const TimeStyle = styled.div`
//   position: absolute;
//   top: ${props => props.offset}px;
//   right: 50px;
// `

// const DateStyle = styled.div`
//   position: absolute;
//   top: ${props => props.offset}px;
//   left: 10px;
// `

// const CourseIndicator = ({time, type, offset}) => {
//   let convertedTime = convertTime(time);
//   return <TimeStyle offset={offset}>{convertedTime[1]}</TimeStyle>
// }

// const FlexRow = styled.div`
//   display: flex;
//   flex-direction: row;
//   position: relative;
// `

// const LeftRight = styled.div`
//   display: flex;
//   flex-direction: row;
//   justify-content: space-between;
//   align-items: center;
// `

// function convertTime(timeString){
//   const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
//   let d = new Date(timeString);
//   return [d.toLocaleDateString('en-US', {month:"numeric", day: "numeric"}), d.toLocaleTimeString('en-US', { hour12: true,
//                                              hour: "numeric",
//                                              minute: "numeric"}).toLowerCase()]
// }

// function absoluteTime(timeString){
//   let d = new Date(timeString);
//   return d.getTime();
// }

// function dateDivs(data, yoff){
//   var i;
//   let divs = [];
//   for (i=1; i<data.length; i++){
//     if(convertTime(data[i][0]["created_at"])[0]!==convertTime(data[i-1][0]["created_at"])[0]){
//       divs.push(<DateStyle offset={yoff[i]}>{convertTime(data[i][0]["created_at"])[0]}</DateStyle>);
//     }
//   }
//   console.log("date divs length is " + divs.length);
//   return divs;
// }

interface TimelineProps {
  courseCode: string;
}

// setTimeline
const Timeline = ({
  courseCode}: TimelineProps) => {

  let [data, setData] = React.useState(null);
  let [segLengths, setSegLengths] = React.useState(null);
  let [yOffsets, setYOffsets] = React.useState(null);
  let [loaded, setLoaded] = React.useState(false);
  let [displayedCode, setDisplayedCode] = React.useState(null);

  // useEffect(()=>{

  //     if (courseCode == null){
  //       return;
  //     }

  //     setLoaded(false);

  //     fetch(`https://penncourseplan.com/api/alert/statusupdate/${courseCode}`).then(res=>res.json()).then(result=>{
  //       console.log(result)
  //       result.sort((a,b)=>(a.created_at > b.created_at) ? 1 : -1);
  //       let simplifiedData = result.reduce((ans, item, index) => { // preprocessing hte data
  //         if(index==0){
  //           return ans;
  //         }
  //         if(item["old_status"] == result[index-1]["old_status"]){
  //           return ans;
  //         }
  //         if(item["old_status"] == "C" && item["new_status"] == "O"){
  //           ans.push([item, "opened"]);
  //         }
  //         if(item["old_status"] == "O" && item["new_status"] == "C"){
  //           ans.push([item, "closed"]);
  //         }
  //         return ans;
  //       }, []).reverse()
  //       setData(simplifiedData);
  //       var i;
  //       let segmentLengths = [];
  //       for (i = 1; i < simplifiedData.length; i++){
  //         segmentLengths.push(Math.round(20+5*Math.pow(1 + absoluteTime(result[i]["created_at"]) - absoluteTime(result[i-1]["created_at"]), 0.2)));
  //       }
  //       let yPositions = [];
  //       yPositions[0] = 0;
  //       for (i = 1; i < segmentLengths.length + 1; i++){
  //         yPositions[i] = Math.round(yPositions[i-1] + segmentLengths[i-1]);
  //       }
  //       console.log(simplifiedData);
  //       console.log(segmentLengths);
  //       console.log(yPositions);
  //       setSegLengths(segmentLengths);
  //       setYOffsets(yPositions);
  //       setLoaded(true);
  //       setDisplayedCode(courseCode);
  //     })
  //   }
  // , [courseCode]);

  // offScreen={courseCode==null || loaded==false}
  
  return (
  
    <AlertHistoryContainer>

            <AlertTitle>Alert History</AlertTitle>
            {/* onClick={()=>setTimeline(null)} */}
            <CloseButton><FontAwesomeIcon icon={faTimes}/></CloseButton>

            <CourseInfoContainer>
              <CourseSubHeading>PSYC-001-001</CourseSubHeading>
              <StatusLabel>Closed</StatusLabel>
            </CourseInfoContainer>

            <TimelineContainer>
              <Segment open={true} length={30}/>
              <Circle open={true}><FontAwesomeIcon icon={faCircle}/></Circle>
              <Segment open={false} length={150}/>
              <Circle open={false}><FontAwesomeIcon icon={faCircle}/></Circle>
              <Segment open={true} length={50}/>
              <Circle open={true}><FontAwesomeIcon icon={faCircle}/></Circle>
            </TimelineContainer>



            {/* <MyButton onClick={()=>setTimeline(null)}><i className="fas fa-times"></i></MyButton>
            <AlertTitle>Alert History</AlertTitle>
            <LeftRight>
                <Subheading>{displayedCode}</Subheading>
                {loaded && data[0]["new_status"] === "O" ? <OpenBadge>Open</OpenBadge> : <ClosedBadge>Closed</ClosedBadge>}
            </LeftRight>
            <ScrollContainer>
              { data && yOffsets ?
                      <FlexRow>
                        <div style={{width:"100px"}}>
                            {dateDivs(data, yOffsets)}
                        </div>
                        <Center>
                          {data.map((item, index) =>
                                <>
                                <Segment height={index === 0 ? segLengths[index] - 5 : segLengths[index] - 23} type = {item[1]} />
                                <MyCircle type = {item[1]}><i className="fas fa-dot-circle"></i></MyCircle>
                                </>
                                                  )}
                        </Center>
                        <div>
                            {data.map((item, index) => index !=0 && <TimeStyle offset={yOffsets[index]}>{convertTime(item[0]["created_at"])[1]}</TimeStyle>
                        )}
                        </div>
                      </FlexRow>
                              : "loading course data"

              }
            </ScrollContainer> */}

    </AlertHistoryContainer>
  );
}

export default Timeline;
