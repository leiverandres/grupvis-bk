import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Label
} from 'recharts';
import { profilesMapping } from './reportMapping';

export default function MembersBarChart(props) {
  const data = props.membersData;

  return (
    <BarChart
      width={1000}
      height={400}
      data={data}
      margin={{ top: 5, right: 10, left: 20, bottom: 10 }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="abbreviation" type="category" tickLine={false}>
        <Label value="Tipo de integrante" offset={-5} position="insideBottom" />
      </XAxis>
      <YAxis allowDecimals={false}>
        <Label value="Cantidad" angle={-90} />
      </YAxis>
      <Tooltip labelFormatter={label => profilesMapping[label]} />
      <Bar dataKey="value" name="Cantidad de integrantes" fill="#009688" />
    </BarChart>
  );
}
