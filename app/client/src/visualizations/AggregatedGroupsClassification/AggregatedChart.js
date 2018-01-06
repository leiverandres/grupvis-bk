import React, { Component } from 'react';
import { select } from 'd3-selection';
import { scaleLinear, scaleBand, scalePoint, scaleSequential } from 'd3-scale';
import { interpolateRdYlBu } from 'd3-scale-chromatic';
import { axisLeft, axisTop, axisBottom } from 'd3-axis';
import { area, line } from 'd3-shape';

export default class AggregatedChart extends Component {
  componentDidMount() {
    this.renderChart();
  }

  componentDidUpdate() {
    this.renderChart();
  }

  renderChart = () => {
    const { width, height } = this.props;
    const margin = { top: 40, right: 20, bottom: 20, left: 40 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    const svg = select(this.svgNode);

    // Scales ============================
    const yScale = scaleLinear()
      .domain([0, 36])
      .range([chartHeight, margin.top]);

    const classificationScale = scaleBand()
      .domain(['A1', 'A', 'B', 'C', 'D', 'Reconocido'])
      .range([margin.left, margin.left + chartWidth])
      .padding(0.35);

    const yearScale = scalePoint()
      .domain(['2015', '2017'])
      .range([0, classificationScale.bandwidth()]);

    const radius = scaleLinear()
      .domain([0, 36])
      .range([5, 15]);

    const color = scaleSequential(interpolateRdYlBu).domain([0, 36]);

    // Scales ============================
    const ticksPadding = 10;
    svg
      .append('g')
      .attr('transform', `translate(${margin.left + margin.right}, 0)`)
      .attr('font-weight', 'bold')
      .style('font-size', '1.2em')
      .call(
        axisLeft(yScale)
          .tickSize(0)
          .tickPadding(10)
      );

    svg
      .append('g')
      .attr('transform', `translate(${margin.left}, ${margin.top})`)
      .attr('font-weight', 'bold')
      .style('font-size', '1.2em')
      .call(
        axisTop(classificationScale)
          .tickSize(0)
          .tickPadding(10)
      );

    svg
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', margin.left / 2 - ticksPadding)
      .attr('x', -margin.top - chartHeight / 2)
      .attr('dy', '0.5em')
      .style('text-anchor', 'middle')
      .style('font-weight', 'bold')
      .text('Cantidad de Grupos');

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

    const pathFakeData = [
      [
        { year: '2015', cant: 5, classification: 'A1' },
        { year: '2017', cant: 6, classification: 'A1' }
      ],
      [
        { year: '2015', cant: 12, classification: 'A' },
        { year: '2017', cant: 16, classification: 'A' }
      ],
      [
        { year: '2015', cant: 23, classification: 'B' },
        { year: '2017', cant: 22, classification: 'B' }
      ],
      [
        { year: '2015', cant: 26, classification: 'C' },
        { year: '2017', cant: 34, classification: 'C' }
      ],
      // [
      //   { year: '2015', cant: 15, classification: 'D' },
      //   { year: '2017', cant: 0, classification: 'D' }
      // ],
      [
        { year: '2015', cant: 1, classification: 'Reconocido' },
        { year: '2017', cant: 8, classification: 'Reconocido' }
      ]
    ];

    const classificationChart = svg
      .selectAll('.classification-chart')
      .data(fakeData)
      .enter()
      .append('g')
      .attr('class', 'classification-chart')
      .attr('transform', d => {
        return `translate(${classificationScale(d.classification) +
          margin.left}, 0)`;
      });

    classificationChart
      .append('g')
      .attr('transform', `translate(0, ${chartHeight})`)
      .call(axisBottom(yearScale).tickSize(0))
      .style('stroke', '#9ea7aa')
      .select('path')
      .style('stroke', '#9ea7aa');

    const subchart = svg
      .selectAll('.classification-subchart')
      .data(fakeData)
      .enter()
      .append('g')
      .attr('class', 'classification-subchart');

    subchart
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
        d =>
          classificationScale(d.classification) +
          yearScale(d.year) +
          margin.left
      )
      .attr('cy', d => yScale(d.cant))
      .attr('fill', d => color(d.cant));

    // NUMBERS
    subchart
      .selectAll('.circle-values')
      .data(d => {
        const newData = d.counter.map(item => {
          const newItem = item;
          newItem.classification = d.classification;
          return newItem;
        });
        return newData;
      })
      .enter()
      .append('text')
      .attr('class', 'circle-values')
      .attr('x', d => {
        if (d.year === '2015') {
          return (
            classificationScale(d.classification) +
            yearScale(d.year) +
            margin.left -
            15
          );
        } else {
          return (
            classificationScale(d.classification) +
            yearScale(d.year) +
            margin.left
          );
        }
      })
      .attr('y', d => {
        if (d.year === '2015') {
          return yScale(d.cant) - 20;
        } else {
          return yScale(d.cant) + 30;
        }
      })
      .style('font-weight', 'bold')
      .text(d => (d.cant !== 0 ? d.cant : ''));

    // GRADIENTS FOR POINT JOINING LINES
    svg
      .selectAll('defs')
      .data(fakeData)
      .enter()
      .append('defs')
      .append('linearGradient')
      .attr('id', d => `pathGradient${d.classification}`)
      .selectAll('stop')
      .data(d => {
        const colorData = [
          { color: color(d.counter[0].cant), offset: '0%' },
          { color: color(d.counter[1].cant), offset: '100%' }
        ];
        return colorData;
      })
      .enter()
      .append('stop')
      .attr('offset', d => d.offset)
      .attr('stop-color', d => d.color);

    // DRAW JOINING LINES
    const joiningLine = area()
      .x(d => {
        return (
          classificationScale(d.classification) +
          yearScale(d.year) +
          margin.left +
          yearScale.padding()
        );
      })
      .y1(d => yScale(d.cant) + radius(d.cant))
      .y0(d => yScale(d.cant) - radius(d.cant));

    subchart
      .selectAll('path')
      .data(pathFakeData)
      .enter()
      .append('path')
      .attr('fill', d => `url(#pathGradient${d[0].classification})`)
      .datum(d => d)
      .attr('d', joiningLine);

    // SEPARATE CLASSIFICATION REGIONS
    let linesData = [];
    fakeData.forEach(elm => {
      linesData.push([
        [
          classificationScale(elm.classification) + classificationScale.step(),
          margin.top
        ],
        [
          classificationScale(elm.classification) + classificationScale.step(),
          chartHeight
        ]
      ]);
    });

    const lineGenerator = line();
    svg
      .selectAll('.divider-line')
      .data(linesData)
      .enter()
      .append('path')
      .attr('stroke', '#cfd8dc')
      .attr('d', lineGenerator);
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