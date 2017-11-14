import React, { Component } from "react";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
import { scaleLinear, scaleBand } from "d3-scale";
import { max } from "d3-array";
import { select } from "d3-selection";
import { axisBottom, axisLeft } from "d3-axis";
import { stack, stackOffsetNone, stackOrderNone } from "d3-shape";
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
            <h3>{`Gran area: ${dataCount[0].bigAreaName}`}</h3>
            <BarChart
              dataObj={dataCount[0]}
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

class BarChart extends Component {
  componentDidMount() {
    this.createBarChart();
  }

  componentDidUpdate() {
    this.createBarChart();
  }

  createBarChart = () => {
    const { dataObj: { classifications }, width, height } = this.props;

    const faculties = Array.from(
      classifications.reduce((acumSet, curItem) => {
        Object.keys(curItem)
          .filter(key => key !== "classification")
          .forEach(item => {
            acumSet.add(item);
          });
        return acumSet;
      }, new Set())
    );
    const stackData = stack()
      .keys(faculties)
      .order(stackOrderNone)
      .offset(stackOffsetNone);
    const series = stackData(classifications);
    console.log(series);
    const margin = {
      top: 20,
      left: 50,
      bottom: 50,
      right: 20
    };
    const barMargin = 10;
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    const svg = select(this.nodeRef);

    svg
      .append("g")
      .attr("class", "graph")
      .attr("transform", `translate(${margin.left}, ${margin.top})`);

    const xScale = scaleBand()
      .range([0, chartWidth])
      .domain(classifications.map(c => c.clasification));

    const yScale = scaleLinear()
      .range([chartHeight, 0])
      .domain([0, 20]);

    // AXES
    svg
      .append("g")
      .attr("class", "axis--x")
      .attr(
        "transform",
        `translate(${margin.left}, ${chartHeight + margin.top})`
      )
      .call(axisBottom(xScale));

    svg
      .append("g")
      .attr("class", "axis--y")
      .attr("transform", `translate(${margin.left}, ${margin.top})`)
      .call(axisLeft(yScale).ticks(10));

    // LABELS
    svg
      .append("text")
      .attr("x", chartWidth / 2)
      .attr("y", chartHeight + 3 * margin.top)
      .attr("text-achor", "middle")
      .attr("fill", "initial")
      .text("Clasificación");

    svg
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", margin.left / 4)
      .attr("x", -chartHeight / 2 + margin.top)
      .attr("dy", "0.5em")
      .attr("class", "label")
      .text("Cantidad de grupos");

    // BARS
    svg
      .select(".graph")
      .selectAll(".bar")
      .data(classifications, d => false)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .attr("x", (d, i) => xScale(classifications[i]) + barMargin)
      .attr("y", d => yScale(d))
      .attr("width", xScale.bandwidth() - barMargin)
      .attr("height", d => chartHeight - yScale(d));
  };

  render() {
    const { width, height } = this.props;

    return (
      <div>
        <svg
          ref={svgNode => (this.nodeRef = svgNode)}
          width={width}
          height={height}
          style={{ border: "solid 3px black" }}
        />
      </div>
    );
  }
}

const BarChartWithData = graphql(knowledgeAreaQuery)(BarChartLayout);
export default BarChartWithData;
