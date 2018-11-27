import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Label
} from 'recharts';
import { Query } from 'react-apollo';
import { gql } from 'apollo-boost';

import { profilesMapping } from './reportMapping';

const ParallelCoordinates = ({
  data,
  classification,
  targetClassification
}) => {
  return (
    <LineChart
      width={1300}
      height={500}
      data={data}
      margin={{ top: 5, right: 30, left: 20, bottom: 20 }}
    >
      <XAxis
        dataKey="profileName"
        tick={{ angle: -35, textAnchor: 'end' }}
        interval={0}
      >
        <Label value="Nombre del perfil" offset={-20} position="insideBottom" />
      </XAxis>
      <YAxis />
      <CartesianGrid strokeDasharray="3 3" />
      <Tooltip labelFormatter={label => profilesMapping[label]} />
      <Legend verticalAlign="top" align="right" />
      <Line
        style={{ strokeWidth: 2 }}
        type="monotoneX"
        name="Valor grupo analizado"
        dataKey="value"
        stroke="#f44336"
        activeDot={{ r: 9 }}
      />
      <Line
        type="monotoneX"
        name="Valor grupo comparado"
        dataKey="comparisonValue"
        stroke="#2196f3"
      />
      <Line
        type="monotoneX"
        name={`Promedio para ${classification}`}
        dataKey="meanValue"
        stroke="#ff9800"
      />
      <Line
        type="monotoneX"
        name={`Promedio para ${targetClassification}`}
        dataKey="comparisonMeanValue"
        stroke="#4caf50"
      />
    </LineChart>
  );
};

function getTargetClassification(classification) {
  switch (classification) {
    case 'A1':
    case 'A':
      return 'A1';
    case 'B':
      return 'A';
    case 'C':
      return 'B';
    case 'reconocido':
      return 'C';
    default:
      return classification;
  }
}

export default function ParallelCoordinatesQuery(props) {
  const { classification, knowledgeArea, data } = props;
  const previousData = data;
  const targetClassification = getTargetClassification(classification);
  const vars = {
    classification,
    knowledgeArea,
    targetClassification
  };
  const query = gql`
    query GetSummaries(
      $classification: String!
      $targetClassification: String!
      $knowledgeArea: String!
    ) {
      groupSummary: profileSummary(
        classification: $classification
        knowledgeArea: $knowledgeArea
      ) {
        meanValues
      }
      compSummary: profileSummary(
        classification: $targetClassification
        knowledgeArea: $knowledgeArea
      ) {
        meanValues
      }
    }
  `;
  return (
    <Query query={query} variables={vars}>
      {({ loading, error, data }) => {
        if (loading) return <h3>Loading ...</h3>;
        if (error) return `Error!: ${error}`;
        const { groupSummary, compSummary } = data;
        const mergedData = previousData.map((val, idx) => {
          val['meanValue'] = groupSummary.meanValues[idx].toFixed(3);
          val['comparisonMeanValue'] = compSummary.meanValues[idx].toFixed(3);
          return val;
        });
        return (
          <ParallelCoordinates
            data={mergedData}
            classification={classification}
            targetClassification={targetClassification}
          />
        );
      }}
    </Query>
  );
}
