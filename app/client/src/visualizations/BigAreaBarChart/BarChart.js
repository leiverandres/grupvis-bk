import React, { Component } from 'react';
import { scaleLinear, scaleBand, scaleOrdinal } from 'd3-scale';
import { max } from 'd3-array';
import { select } from 'd3-selection';
import { axisBottom, axisLeft, axisTop } from 'd3-axis';
import { stack, stackOffsetNone, stackOrderNone } from 'd3-shape';
import './BarChart.css';

const constants = {
  classificationLabels: ['A1', 'A', 'B', 'C', 'D', 'Reg'],
  faculties: [
    'Facultad de Ingenierías Eléctrica, Electrónica, Física y Ciencias de la Computación',
    'Facultad de Ingeniería Industrial',
    'Facultad de Ciencias Ambientales',
    'Facultad de Bellas Artes y Humanidades',
    'Facultad de Ciencias de la Salud',
    'Facultad de Ciencias  de la Educación',
    'Facultad de Ingeniería Mecánica',
    'Facultad de Ciencias  Básicas',
    'Facultad de Tecnología',
    'Vicerrectoría de Investigaciones innovación y Extensión'
  ],
  colors: [
    '#8dd3c7',
    '#ffffb3',
    '#bebada',
    '#fb8072',
    '#80b1d3',
    '#fdb462',
    '#b3de69',
    '#fccde5',
    '#d9d9d9',
    '#bc80bd',
    '#ccebc5',
    '#ffed6f'
  ]
};

export default class BarChart extends Component {
  componentDidMount() {
    this.renderBarChart();
  }

  componentDidUpdate() {
    this.renderBarChart();
  }

  renderBarChart = () => {
    const { dataArray, width, height } = this.props;
    const { faculties, classificationLabels, colors } = constants;
    const bigAreasLabels = dataArray.map(item => item.bigAreaName);

    // Fill missing faculties in each big Area
    dataArray.forEach((areaItem, idx) => {
      areaItem.classifications.forEach((classificationItem, jindex) => {
        faculties.forEach(fac => {
          if (!classificationItem[fac]) {
            dataArray[idx].classifications[jindex][fac] = 0;
          }
        });
      });
    });

    const margin = {
      top: 50,
      left: 50,
      bottom: 50,
      right: 20
    };
    const barMargin = 5;
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    const stackData = stack()
      .keys(faculties)
      .order(stackOrderNone)
      .offset(stackOffsetNone);

    const svg = select(this.nodeRef);

    svg
      .append('g')
      .attr('class', 'graph')
      .attr('transform', `translate(${margin.left}, ${margin.top})`);

    // Scales ================================================================
    const x0Scale = scaleBand()
      .range([0, chartWidth])
      .domain(bigAreasLabels);

    const x1Scale = scaleBand()
      .range([0, x0Scale.bandwidth()])
      .domain(classificationLabels);

    const yScale = scaleLinear()
      .range([chartHeight, 0])
      .domain([0, max(dataArray, d => max(d.classifications, dd => dd.total))]);

    const colorScale = scaleOrdinal(colors).domain(faculties);
    // Scales ================================================================

    // AXES ==============================================================
    svg
      .append('g')
      .attr('class', 'axis--x0')
      .attr('transform', `translate(${margin.left}, ${margin.top})`)
      .call(axisTop(x0Scale));

    svg
      .append('g')
      .attr('class', 'axis--y')
      .attr('transform', `translate(${margin.left}, ${margin.top})`)
      .call(axisLeft(yScale));
    // AXES ==============================================================

    // LABELS ============================================================
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
    // LABELS ============================================================

    // GROUPS ============================================================
    const group = svg
      .selectAll('.group-chart')
      .data(dataArray)
      .enter()
      .append('g')
      .attr('class', 'group-chart')
      .attr('transform', d => `translate(${x0Scale(d.bigAreaName)}, 0)`);
    // GROUPS ============================================================

    // STACKED BAR CHARTS ================================================

    group
      .selectAll('g')
      .data(d => stackData(d.classifications))
      .enter()
      .append('g')
      .attr('fill', d => colorScale(d.key))
      .selectAll('rect')
      .data(d => d)
      .enter()
      .append('rect')
      .attr('x', d => x1Scale(d.data.classification) + margin.left + barMargin)
      .attr('y', d => yScale(d[1]) + margin.top)
      .attr('height', d => yScale([d[0]]) - yScale(d[1]))
      .attr('width', d => x1Scale.bandwidth() - barMargin);

    group
      .append('g')
      .attr('class', 'axis--x1')
      .attr(
        'transform',
        `translate(${margin.left}, ${chartHeight + margin.top})`
      )
      .call(axisBottom(x1Scale));
    // STACKED BAR CHARTS ================================================
  };

  render() {
    const { width, height } = this.props;

    return (
      <div>
        <h3>Gran area</h3>
        <svg
          ref={svgNode => (this.nodeRef = svgNode)}
          width={width}
          height={height}
        />
      </div>
    );
  }
}
