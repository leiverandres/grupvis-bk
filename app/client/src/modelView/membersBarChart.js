import React from 'react';
import { Group } from '@vx/group';
import { Bar } from '@vx/shape';
import { scaleLinear, scaleBand } from '@vx/scale';
import { AxisLeft, AxisBottom } from '@vx/axis';
import { LinearGradient } from '@vx/gradient';

const width = 700;
const height = 500;
const margin = {
  top: 60,
  bottom: 20,
  left: 20,
  right: 20
};

const xMax = width - margin.left - margin.right;
const yMax = height - margin.top - margin.bottom;

const x = d => d.abbreviation;
const y = d => Number(d.value);

export default function MembersBarChart(props) {
  const data = props.membersData;
  const xScale = scaleBand({
    rangeRound: [margin.left, xMax],
    domain: data.map(x),
    padding: 0.4
  });

  const yScale = scaleLinear({
    rangeRound: [yMax, margin.top],
    domain: [0, Math.max(...data.map(y))]
  });

  const compose = (scale, accessor) => data => scale(accessor(data));
  const xPoint = compose(
    xScale,
    x
  );
  const yPoint = compose(
    yScale,
    y
  );
  return (
    <svg width={width} height={height}>
      <LinearGradient from="#fbc2eb" to="#a6c1ee" id="gradient" />
      <Group>
        <AxisBottom
          scale={xScale}
          top={yMax}
          left={margin.left}
          label={'Tipo de perfil del integrante'}
          stroke={'#1b1a1e'}
          tickTextFill={'#1b1a1e'}
        />
        <AxisLeft
          scale={yScale}
          top={0}
          left={margin.left + margin.right}
          label={'Cantidad'}
          stroke={'#1b1a1e'}
          tickTextFill={'#1b1a1e'}
        />
        {data.map((d, i) => {
          const barHeight = yMax - yPoint(d);
          return (
            <Group key={`bar-${i}`}>
              <Bar
                x={xPoint(d) + margin.left}
                y={yMax - barHeight}
                height={barHeight}
                width={xScale.bandwidth()}
                fill="rgba(64, 138, 140, 0.9)"
              />
            </Group>
          );
        })}
      </Group>
    </svg>
  );
}
