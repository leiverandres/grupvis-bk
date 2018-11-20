import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

export default function ProductsBarChart(props) {
  console.log(props.productsCount);
  const data = props.productsCount.filter(
    elem => elem.approvedCount !== 0 || elem.noApprovedCount !== 0
  );
  return (
    <BarChart
      width={1000}
      height={400}
      data={data}
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      style={{ margin: 'auto' }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="productType" tick={false} type="category" />
      <YAxis domain={['dataMin', 'dataMax']} />
      <Tooltip />
      <Legend />
      <Bar
        dataKey="approvedCount"
        fill="rgba(55, 83, 109, 0.9)"
        name="Aprobados"
      />
      <Bar
        dataKey="noApprovedCount"
        fill="rgba(26, 118, 255, 0.9)"
        name="Sin aprobar"
      />
    </BarChart>
  );
}
