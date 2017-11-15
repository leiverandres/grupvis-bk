import React, { Component } from "react";
import { graphql } from "react-apollo";
import gql from "graphql-tag";

import BarChart from "./BarChart";
import "./BarChart.css";

const knowledgeAreaQuery = gql`
  query KnowledgeAreaQuery {
    groups {
      code
      name
      bigKnowledgeArea
      knowledgeArea
      classification
      faculty
      dependency
    }
  }
`;

class BarChartLayout extends Component {
  render() {
    const { data: { loading, groups } } = this.props;
    console.log(this.props);
    let dataCount = {};
    if (!loading) {
      const countByBigArea = {};
      groups.forEach(groupObj => {
        const { bigKnowledgeArea, faculty, name } = groupObj;
        let classification = groupObj.classification || "Reg";
        if (countByBigArea[bigKnowledgeArea]) {
          // already exist an big area object
          if (countByBigArea[bigKnowledgeArea][classification]) {
            // already exist an counter of area inside this big area
            if (countByBigArea[bigKnowledgeArea][classification][faculty]) {
              countByBigArea[bigKnowledgeArea][classification][faculty].push(
                name
              );
            } else {
              countByBigArea[bigKnowledgeArea][classification][faculty] = [
                name
              ];
            }
          } else {
            // no couter of area inside big area object
            countByBigArea[bigKnowledgeArea][classification] = {
              [faculty]: [name]
            };
          }
        } else {
          // no big area object found
          countByBigArea[bigKnowledgeArea] = {
            [classification]: {
              [faculty]: [name]
            }
          };
        }
      });

      dataCount = Object.entries(countByBigArea).map(item => {
        return {
          bigAreaName: item[0],
          classifications: Object.entries(item[1]).map(subitem => {
            const counter = {};
            Object.entries(subitem[1]).forEach(entry => {
              counter[entry[0]] = entry[1].length;
            });
            return {
              classification: subitem[0],
              ...counter
            };
          })
        };
      });
    }
    return (
      <div>
        {loading ? (
          <h1>Loading...</h1>
        ) : (
          <div>
            <BarChart
              dataObj={dataCount[4]}
              size={[500, 500]}
              width={700}
              height={600}
            />
          </div>
        )}
      </div>
    );
  }
}

const BarChartWithData = graphql(knowledgeAreaQuery)(BarChartLayout);
export default BarChartWithData;
