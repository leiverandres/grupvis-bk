import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Label
} from 'recharts';

export default function ProductsBarChart(props) {
  const data = props.productsCount.filter(
    elem => elem.approvedCount !== 0 || elem.noApprovedCount !== 0
  );
  return (
    <BarChart
      width={1000}
      height={700}
      data={data}
      margin={{ top: 5, right: 10, left: 30, bottom: 280 }}
      style={{ margin: 'auto' }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis
        dataKey="productType"
        type="category"
        interval={0}
        tick={{ angle: -50, textAnchor: 'end' }}
        reversed
      />
      <YAxis domain={['dataMin', 'dataMax']}>
        <Label value="Cantidad" angle={-90} />
      </YAxis>
      <Tooltip />
      <Legend verticalAlign="top" align="right" />
      <Bar dataKey="approvedCount" fill="#6ec6ff" name="Aprobados" />
      <Bar dataKey="noApprovedCount" fill="#ff7961" name="Sin aprobar" />
    </BarChart>
  );
}
