import React, { Component } from 'react';
import { graphql } from 'react-apollo';
import gql from 'graphql-tag';
import { scaleLinear, scaleBand } from 'd3-scale';
import { max } from 'd3-array';
import { select } from 'd3-selection';
import { axisBottom, axisLeft } from 'd3-axis';
import './BarChart.css';

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
        const { bigKnowledgeArea, faculty, classification, name } = groupObj;
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
            return {
              clasification: subitem[0],
              countByClassification: Object.entries(
                subitem[1]
              ).map(classEntry => {
                return {
                  faculty: classEntry[0],
                  groups: classEntry[1],
                  total: classEntry[1].length
                };
              })
            };
          })
        };
      });
    }
    console.log(dataCount);
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
              width={500}
              height={400}
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
    const { dataObj, width, height } = this.props;
    const clasifications = Object.keys(dataObj);
    const counts = Object.values(dataObj);
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
      .append('g')
      .attr('class', 'graph')
      .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const xScale = scaleBand()
      .range([0, chartWidth])
      .domain(clasifications);

    const yScale = scaleLinear()
      .range([chartHeight, 0])
      .domain([0, max(counts)]);

    svg
      .append('g')
      .attr('class', 'axis--x')
      .attr(
        'transform',
        `translate(${margin.left}, ${chartHeight + margin.top})`
      )
      .call(axisBottom(xScale));

    svg
      .append('text')
      .attr('x', chartWidth / 2)
      .attr('y', chartHeight + 3 * margin.top)
      .attr('text-achor', 'middle')
      .attr('fill', 'initial')
      .text('Clasificación');

    svg
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', margin.left / 4)
      .attr('x', -chartHeight / 2 + margin.top)
      .attr('dy', '0.5em')
      .attr('class', 'label')
      .text('Cantidad de grupos');

    svg
      .append('g')
      .attr('class', 'axis--y')
      .attr('transform', `translate(${margin.left}, ${margin.top})`)
      .call(axisLeft(yScale).ticks(10));

    svg
      .select('.graph')
      .selectAll('.bar')
      .data(counts)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', (d, i) => xScale(clasifications[i]) + barMargin)
      .attr('y', d => yScale(d))
      .attr('width', xScale.bandwidth() - barMargin)
      .attr('height', d => chartHeight - yScale(d));
  };

  render() {
    const { width, height } = this.props;

    return (
      <div>
        <svg
          ref={svgNode => (this.nodeRef = svgNode)}
          width={width}
          height={height}
          style={{ border: 'solid 3px black' }}
        />
      </div>
    );
  }
}

const BarChartWithData = graphql(knowledgeAreaQuery)(BarChartLayout);
export default BarChartWithData;
