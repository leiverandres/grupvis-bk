import React, { Component } from 'react';
import { select } from 'd3-selection';
import { scaleBand, scalePoint, scaleOrdinal } from 'd3-scale';
import { area } from 'd3-shape';

import { circleColors } from './fixtures.json';

export default class BarChart extends Component {
  componentDidMount() {
    this.renderBarChart();
  }

  componentDidUpdate() {
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
    const classifications = ['A1', 'A', 'B', 'C', 'D', 'reconocido', 'SC'];
    const margin = {
      top: 30,
      right: 20,
      bottom: 30,
      left: 40
    };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    const svg = select(this.nodeRef);

    svg.style('background', '#f5f5f5');

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

    const color = scaleOrdinal(circleColors).domain(['2015', '2017']);

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

    svg
      .selectAll('.classification-text')
      .data(dataArray)
      .enter()
      .append('text')
      .attr('class', 'classification-text')
      .attr('x', d => xScale(d.year) + xScale.padding())
      .attr(
        'y',
        d =>
          yScale(d.classification) +
          yScale.bandwidth() -
          radius(d.classification) -
          20
      )
      .text(d => d.classification);

    svg
      .selectAll('.year-text')
      .data(dataArray)
      .enter()
      .append('text')
      .attr('class', 'year-text')
      .attr('font-weight', 'bold')
      .attr('x', d => xScale(d.year) + xScale.padding())
      .attr(
        'y',
        d =>
          yScale(d.classification) +
          yScale.bandwidth() +
          radius(d.classification) +
          20
      )
      .text(d => d.year);

    const joiningLine = area()
      .x(d => {
        return xScale(d.year) + xScale.padding();
      })
      .y1(
        d =>
          yScale(d.classification) +
          yScale.bandwidth() +
          radius(d.classification)
      )
      .y0(
        d =>
          yScale(d.classification) +
          yScale.bandwidth() -
          radius(d.classification)
      );

    const svgDefs = svg.append('defs');
    svgDefs
      .append('linearGradient')
      .attr('id', 'pathGradient')
      .selectAll('stop')
      .data([
        { color: circleColors[0], offset: '0%' },
        { color: circleColors[1], offset: '100%' }
      ])
      .enter()
      .append('stop')
      .attr('offset', d => d.offset)
      .attr('stop-color', d => d.color);

    svg
      .append('path')
      .datum(dataArray)
      .attr('fill', `url(#pathGradient)`)
      .attr('d', joiningLine);
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
