import React, { useState } from 'react';
import RuleLeaf, { SkeletonRuleLeaf } from './QObject';
import { Course, Fulfillment, Rule as RuleComponent } from '@/types';
import styled from '@emotion/styled';
import { Icon } from '../common/bulma_derived_components';
import { useSWRCrud } from '@/hooks/swrcrud';
import { useDrop } from 'react-dnd';
import { ItemTypes } from '../dnd/constants';
import { DarkBlueBackgroundSkeleton } from '../FourYearPlan/PlanPanel';

const RuleTitleWrapper = styled.div`
    background-color: var(--primary-color-light);
    position: relative;
    border-radius: var(--req-item-radius);
`

const ProgressBar = styled.div<{$progress: number}>`
    width: ${props => props.$progress * 100}%;
    height: 100%;
    position: absolute;
    background-color: var(--primary-color-dark);
    border-top-left-radius: .3rem;
    border-bottom-left-radius: .3rem;
`

const RuleTitle = styled.div<{$progress: number}>`
  position: relative;
  font-size: 1rem;
  font-weight: 500;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  color: #575757;
  padding: 0.25rem .5rem;
  margin: 0.5rem 0;
`

const RuleLeafWrapper = styled.div<{$isDroppable:boolean, $isOver: boolean}>`
  margin: .5rem;
  margin-left: 0;
  display: flex;
  justify-content: space-between;
  gap: .5rem;
  align-items: center;
  box-shadow: ${props => props.$isOver ? '0px 0px 4px 2px var(--selected-color);' : props.$isDroppable ? '0px 0px 4px 2px var(--primary-color-dark);' : 'rgba(0, 0, 0, 0.05);'}
`

const CusCourses = styled.div`
  font-weight: 500;
  font-size: .9rem;
  white-space: nowrap;
`

const Row = styled.div`
  display: flex;
  gap: .5rem;
`

interface RuleProps {
    rule: RuleComponent;
    rulesToFulfillments: { [ruleId: string]: Fulfillment[] };
    activeDegreePlanId: number;
}


/**
 * Skeleton of a rule, which excepts children that are skeleton rules. If the skeleton has children, then
 * it is treated as a rule header; otherwise it is treated as a rule leaf.
 */
export const SkeletonRule: React.FC<React.PropsWithChildren> = ({ children }) => (
  <>
    {!children ?
      <RuleLeafWrapper $isDroppable={false} $isOver={false}>
          <SkeletonRuleLeaf />
          <div>
            <CusCourses>
              <Row>
                <DarkBlueBackgroundSkeleton width="1em" />
                <span>/</span>
                <DarkBlueBackgroundSkeleton width="2em" />
              </Row>
            </CusCourses>
          </div>
      </RuleLeafWrapper>
      :
      <RuleTitleWrapper>
        <ProgressBar $progress={0}></ProgressBar>
        <RuleTitle $progress={0}>
          <Row>
            <DarkBlueBackgroundSkeleton width="10em" />
            <DarkBlueBackgroundSkeleton width="7em" />
          </Row>
            <Icon>
              <i className="fas fa-chevron-down" />
            </Icon>
        </RuleTitle>
      </RuleTitleWrapper>
      }
    <div className="ms-3">
      {children}
    </div>
  </>
)

/**
 * Recursive component to represent a rule.
 * @returns 
 */
const RuleComponent = ({ activeDegreePlanId, rule, rulesToFulfillments} : RuleProps) => {
    const [collapsed, setCollapsed] = useState(false);
  
    // this is only used when we have a rule leaf
    // TODO: this logic should be moved to the rule leaf
    const fulfillmentsForRule: Fulfillment[] = rulesToFulfillments[rule.id] || [];
    const cus = fulfillmentsForRule.reduce((acc, f) => acc + (f.course?.credits || 1), 0); // default to 1 cu 
    const num = fulfillmentsForRule.length;
    const satisfied = (rule.credits ? cus >= rule.credits : true) && (rule.num ? num >= rule.num : true);

    // the fulfillments api uses the POST method for updates (it creates if it doesn't exist, and updates if it does)
    const { createOrUpdate } = useSWRCrud<Fulfillment>(`/api/degree/degreeplans/${activeDegreePlanId}/fulfillments`, { idKey: "full_code" });

    const [{ isOver, canDrop }, drop] = useDrop(() => ({
        accept: ItemTypes.COURSE,
        drop: (course: Course) => {
            console.log("DROPPED", course.full_code, 'from', course.semester);
            if (!!course.semester) {
              createOrUpdate({ semester: course.semester, rules: [rule.id] }, course.full_code);
            }
        },
        canDrop: () => {return !satisfied && !!rule.q},  // has to be a rule leaf and unsatisfied to drop
        collect: monitor => ({
          isOver: !!monitor.isOver() && !satisfied,
          canDrop: !!monitor.canDrop()
        }),
    }), [createOrUpdate]);

    const getProgress = () => {
      let satisfied = 0, total = 0;
      for (let i = 0; i < rule.rules.length; i++) {
        const childRuleFulfillments = rulesToFulfillments[rule.rules[i].id];
        satisfied += childRuleFulfillments ? childRuleFulfillments.length : 0;
        total += rule.rules[i].num ? rule.rules[i].num : rule.rules[i].credits;
      }
      if (!satisfied && !total) return [];
      return [satisfied, total];

    }

    return (
      <>
        {rule.q ? 
          <RuleLeafWrapper $isDroppable={canDrop} $isOver={isOver} ref={drop}>
              <RuleLeaf q_json={rule.q_json} rule={rule} fulfillmentsForRule={fulfillmentsForRule} satisfied={satisfied} />
              <div>
                {rule.credits && <CusCourses>{cus} / {rule.credits} cus</CusCourses>}
                {" "}
                {rule.num && <CusCourses>{num} / {rule.num}</CusCourses>}
              </div>
          </RuleLeafWrapper>
          :
          <RuleTitleWrapper onClick={() => setCollapsed(!collapsed)}>
            <ProgressBar $progress={getProgress()[0] / getProgress()[1]}></ProgressBar>
            <RuleTitle>
              <div>
                {rule.title}
                {!!getProgress().length && <span>{` (${getProgress()[0]} / ${getProgress()[1]})`}</span>}
              </div>
                {rule.rules.length && 
                    <Icon>
                      <i className={`fas fa-chevron-${collapsed ? "up" : "down"}`}></i>
                    </Icon>
                }
            </RuleTitle>
          </RuleTitleWrapper>
          }
        {!collapsed && <div className="ms-3">
            {rule.rules.map((rule: any, index: number) => <div>
                <RuleComponent 
                  key={rule.id} 
                  rule={rule} 
                  rulesToFulfillments={rulesToFulfillments} 
                  />
                </div>
            )}
          </div>
          }
      </>
    )
}

export default RuleComponent;