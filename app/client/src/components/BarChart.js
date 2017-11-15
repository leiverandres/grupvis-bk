import React, { Component } from "react";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
import {
  scaleLinear,
  scaleBand,
  scaleOrdinal,
  schemeCategory10
} from "d3-scale";
import { max } from "d3-array";
import { select } from "d3-selection";
import { axisBottom, axisLeft } from "d3-axis";
import { stack, stackOffsetNone, stackOrderNone } from "d3-shape";
import "./BarChart.css";

export default class BarChart extends Component {
  componentDidMount() {
    this.createBarChart();
  }

  componentDidUpdate() {
    this.createBarChart(schemeCategory10);
  }

  createBarChart = () => {
    const { dataObj: { classifications }, width, height } = this.props;
    const classificationLabels = classifications.map(c => c.classification);

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
      .domain(classificationLabels);

    const yScale = scaleLinear()
      .range([chartHeight, 0])
      .domain([0, 20]);

    // Color
    const zScale = scaleOrdinal(schemeCategory10);

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
    const layer = svg
      .selectAll(".stack")
      .data(series)
      .enter()
      .append("g")
      .attr("class", "stack");

    layer
      .selectAll("rect")
      .data(d => d)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .style("fill", (d, i) => {
        console.log(i, zScale(i));
        return zScale(i);
      })
      .attr(
        "x",
        (d, i) => xScale(classificationLabels[i]) + margin.left + barMargin
      )
      .attr("y", d => yScale(d[0] + d[1]) + margin.top)
      .attr("height", d => {
        const height = yScale(d[0]) - yScale(d[0] + d[1]) || 0;
        console.log("height for", d, height);
        console.log("y0", d[0], yScale(d[0]));
        console.log("y", d[1], yScale(d[1]));
        console.log("sub", d[0] + d[1]);
        return height;
      })
      .attr("width", d => xScale.bandwidth() - barMargin);
  };

  render() {
    const { width, height, dataObj: { bigAreaName } } = this.props;

    return (
      <div>
        <h3>{`Gran area: ${bigAreaName}`}</h3>
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
