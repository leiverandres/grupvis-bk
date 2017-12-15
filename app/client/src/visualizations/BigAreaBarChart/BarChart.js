import React, { Component } from 'react';
import { scaleLinear, scaleBand, scaleOrdinal } from 'd3-scale';
import { max } from 'd3-array';
import { select, event } from 'd3-selection';
import { axisBottom, axisLeft, axisTop } from 'd3-axis';
import { stack, stackOffsetNone, stackOrderNone } from 'd3-shape';
import { transition } from 'd3-transition';
import { easeExpIn } from 'd3-ease';

import './BarChart.css';
import { faculties, colors } from './fixtures.json';

export default class BarChart extends Component {
  componentDidMount() {
    this.renderBarChart();
  }

  componentDidUpdate() {
    this.renderBarChart();
  }

  renderBarChart = () => {
    const { dataArray, width, height, classificationLabels } = this.props;
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
    const groupedChartPadding = 0.02;
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    const stackData = stack()
      .keys(faculties)
      .order(stackOrderNone)
      .offset(stackOffsetNone);

    const svg = select(this.nodeRef);

    svg
      .append('g')
      .attr('class', 'chart')
      .attr('transform', `translate(${margin.left}, ${margin.top})`);

    // Scales ================================================================
    const x0Scale = scaleBand()
      .range([0, chartWidth])
      .domain(bigAreasLabels)
      .padding(groupedChartPadding);

    const x1Scale = scaleBand()
      .range([0, x0Scale.bandwidth()])
      .domain(classificationLabels);

    const yScale = scaleLinear()
      .range([chartHeight, 0])
      .domain([0, max(dataArray, d => max(d.classifications, dd => dd.total))]);

    const colorScale = scaleOrdinal(colors).domain(faculties);
    // Scales ================================================================
    // TOOTIP ============================================================
    const tooltip = select('body')
      .append('div')
      .attr('class', 'tooltip')
      .style('display', 'none')
      .style('max-width', '300px')
      .style('height', 'auto')
      .style('color', '#fff')
      .style('text-align', 'center')
      .style('padding', '7px')
      .style('opacity', 0.9);

    // TOOTIP ============================================================
    // AXES ==============================================================
    svg
      .append('g')
      .attr('class', 'axis--x0')
      .attr('transform', `translate(${margin.left}, ${margin.top - 10})`)
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
    const t = transition()
      .duration(1700)
      .ease(easeExpIn);

    group
      .selectAll('g')
      .data(d => stackData(d.classifications))
      .enter()
      .append('g')
      .attr('fill', d => colorScale(d.key))
      .attr('class', d => d.key)
      .selectAll('rect')
      .data(d => {
        // Avoid losing faculty of every bar in the next step
        const faculty = d.key;
        const newData = d.map(di => {
          di.faculty = faculty;
          return di;
        });
        return newData;
      })
      .enter()
      .append('rect')
      .attr('x', d => x1Scale(d.data.classification) + margin.left + barMargin)
      .attr('width', d => x1Scale.bandwidth() - barMargin)
      .attr('height', 0) // setting 0 height for the transition
      .attr('y', yScale(0) + margin.top) // setting to the botton for the transition
      .on('mouseout', () => tooltip.style('display', 'none'))
      .on('mouseover', () => tooltip.style('display', 'inline-block'))
      .on('mousemove', function(d, i) {
        const quantity = d[1] - d[0];
        tooltip
          .style('left', `${event.pageX - margin.left}px`)
          .style('top', `${event.pageY - 150}px`)
          .style('display', 'inline-block').html(`<div>
                <P><strong>Facultad</strong>: ${d.faculty}</p>
                <p><strong>Categoria</strong>: ${d.data.classification}</p>
                <p>${quantity} ${quantity > 1 ? 'Grupos' : 'Grupo'}</p>
               </div>`);
      })
      .transition(t)
      .attr('y', d => yScale(d[1]) + margin.top)
      .attr('height', d => yScale([d[0]]) - yScale(d[1]));

    group
      .append('g')
      .attr('class', 'axis--x1')
      .attr(
        'transform',
        `translate(${margin.left}, ${chartHeight + margin.top})`
      )
      .call(axisBottom(x1Scale));
    // STACKED BAR CHARTS ================================================

    // LEGEND ============================================================
    const legendSquareSize = 19;
    const xLegendPos = width - legendSquareSize;
    const yLegendPos = margin.top + legendSquareSize;
    const legend = svg
      .append('g')
      .attr('font-family', 'sans-serif')
      .attr('font-size', 10)
      .attr('text-anchor', 'end')
      .selectAll('g')
      .data(faculties)
      .enter()
      .append('g')
      .attr('transform', (d, i) => `translate(0, ${i * legendSquareSize + 2})`);

    legend
      .append('rect')
      .attr('x', xLegendPos)
      .attr('y', yLegendPos) // it forms like a top padding
      .attr('width', legendSquareSize)
      .attr('height', legendSquareSize)
      .attr('fill', colorScale);

    legend
      .append('text')
      .attr('x', xLegendPos - legendSquareSize)
      .attr('y', yLegendPos + legendSquareSize / 2)
      .attr('dy', '0.32em')
      .text(d => d);
    // LEGEND ============================================================
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
