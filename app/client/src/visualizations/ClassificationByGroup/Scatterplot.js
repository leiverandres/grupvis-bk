import React, { Component } from 'react';
import { select } from 'd3-selection';
import { scaleBand, scalePoint, scaleOrdinal } from 'd3-scale';
import { axisBottom, axisLeft } from 'd3-axis';

export default class BarChart extends Component {
  componentDidMount() {
    this.renderBarChart();
  }

  componentDidUpdate() {
    console.log('update');
    const svg = select(this.nodeRef);
    svg.selectAll('*').remove();
    this.renderBarChart();
  }

  renderBarChart = () => {
    const { data } = this.props;

    let dataArray = [
      {
        name: data.name,
        year: '2015',
        classification: data.classification2015 || 'SC'
      },
      {
        name: data.name,
        year: '2017',
        classification: data.classification2017 || 'SC'
      }
    ];
    const { width, height } = this.props;
    const classifications = ['A1', 'A', 'B', 'C', 'D', 'SC', 'Reconocido'];
    const margin = {
      top: 30,
      right: 20,
      bottom: 30,
      left: 40
    };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    const svg = select(this.nodeRef);

    // SCALES =================================================
    const xScale = scalePoint()
      .domain(['2015', '2017'])
      .range([margin.left, chartWidth + margin.left])
      .padding(15);

    const yScale = scaleBand()
      .domain(classifications)
      .range([margin.top, margin.top + chartHeight]);

    const radius = scaleBand()
      .domain(classifications)
      .range([60, 5]);

    const color = scaleOrdinal(['#4dd0e1', '#81c784']).domain(['2015', '2017']);
    svg
      .append('g')
      .attr('class', 'axis--x')
      .attr('transform', `translate(0, ${margin.top + chartHeight})`)
      .call(axisBottom(xScale));

    svg
      .append('g')
      .attr('class', 'axis--y')
      .attr('transform', `translate(${margin.left}, ${margin.top})`)
      .call(axisLeft(yScale));

    svg
      .selectAll('.circle')
      .data(dataArray)
      .enter()
      .append('circle')
      .attr('class', '.circle')
      .attr('r', d => radius(d.classification))
      .attr('cx', d => xScale(d.year) + xScale.padding())
      .attr('cy', d => yScale(d.classification) + yScale.bandwidth())
      .attr('fill', d => color(d.year));
  };

  render() {
    const { width, height, style } = this.props;

    return (
      <div className="chart-container" style={style}>
        <svg
          ref={svgNode => (this.nodeRef = svgNode)}
          width={width}
          height={height}
        />
      </div>
    );
  }
}
