import React, { Component } from 'react';
import { select } from 'd3-selection';
import { scaleLinear, scaleBand, scalePoint } from 'd3-scale';
import { axisLeft, axisTop, axisBottom } from 'd3-axis';

export default class AggregatedChart extends Component {
  componentDidMount() {
    this.renderChart();
  }

  componentDidUpdate() {
    this.renderChart();
  }

  renderChart = () => {
    const { width, height } = this.props;
    const margin = { top: 20, right: 20, bottom: 20, left: 40 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    const svg = select(this.svgNode);

    // Scales ============================
    const yScale = scaleLinear()
      .domain([0, 36])
      .range([chartHeight, 0]);

    const classificationScale = scaleBand()
      .domain(['A1', 'A', 'B', 'C', 'D', 'Reconocido'])
      .range([0, chartWidth])
      .padding(0.2);

    const yearScale = scalePoint()
      .domain(['2015', '2017'])
      .range([0, classificationScale.bandwidth()]);

    const radius = scaleLinear()
      .domain([0, 36])
      .range([5, 15]);

    // Scales ============================

    svg
      .append('g')
      .attr('transform', `translate(${(margin.left, margin.top)})`)
      .call(axisLeft(yScale));

    svg
      .append('g')
      .attr('transform', `translate(${margin.left}, ${margin.top})`)
      .call(axisTop(classificationScale));

    const fakeData = [
      {
        classification: 'A1',
        counter: [{ year: '2015', cant: 5 }, { year: '2017', cant: 6 }]
      },
      {
        classification: 'A',
        counter: [{ year: '2015', cant: 12 }, { year: '2017', cant: 16 }]
      },
      {
        classification: 'B',
        counter: [{ year: '2015', cant: 23 }, { year: '2017', cant: 22 }]
      },
      {
        classification: 'C',
        counter: [{ year: '2015', cant: 26 }, { year: '2017', cant: 34 }]
      },
      {
        classification: 'D',
        counter: [{ year: '2015', cant: 15 }, { year: '2017', cant: 0 }]
      },
      {
        classification: 'Reconocido',
        counter: [{ year: '2015', cant: 1 }, { year: '2017', cant: 8 }]
      }
    ];

    const classificationChart = svg
      .selectAll('.classification-chart')
      .data(fakeData)
      .enter()
      .append('g')
      .attr('class', 'classification-chart')
      .attr('transform', d => {
        return `translate(${classificationScale(d.classification)}, 0)`;
      });

    classificationChart
      .append('g')
      .attr('transform', `translate(0, ${chartHeight})`)
      .call(axisBottom(yearScale));

    svg
      .selectAll('.classification-subchart')
      .data(fakeData)
      .enter()
      .append('g')
      .attr('class', 'classification-subchart')
      .selectAll('circle')
      .data(d => {
        const newData = d.counter.map(item => {
          const newItem = item;
          newItem.classification = d.classification;
          return newItem;
        });
        return newData;
      })
      .enter()
      .append('circle')
      .attr('class', '.circle')
      .attr('r', d => {
        return d.cant !== 0 ? radius(d.cant) : 0;
      })
      .attr(
        'cx',
        d => classificationScale(d.classification) + yearScale(d.year)
      )
      .attr('cy', d => yScale(d.cant))
      .attr('fill', 'black');
  };
  render() {
    const { width, height } = this.props;
    return (
      <div className="chart-container">
        <svg ref={ref => (this.svgNode = ref)} width={width} height={height} />
      </div>
    );
  }
}
