import React, { Component } from 'react';
import { graphql } from 'react-apollo';
import gql from 'graphql-tag';

import AggregatedChart from './AggregatedChart';

const groupsQuery = gql`
  query GroupsClassification {
    groups {
      classification2015
      classification2017
      name
    }
  }
`;

class ChartLayout extends Component {
  render() {
    const { data: { loading, groups } } = this.props;
    let counter = {};
    if (!loading) {
      const initialObj = {
        A1: [{ year: '2015', count: 0 }, { year: '2017', count: 0 }],
        A: [{ year: '2015', count: 0 }, { year: '2017', count: 0 }],
        B: [{ year: '2015', count: 0 }, { year: '2017', count: 0 }],
        C: [{ year: '2015', count: 0 }, { year: '2017', count: 0 }],
        D: [{ year: '2015', count: 0 }, { year: '2017', count: 0 }],
        Reconocido: [{ year: '2015', count: 0 }, { year: '2017', count: 0 }]
      };
      counter = groups.reduce((acum, cur) => {
        if (cur.classification2015) {
          acum[cur.classification2015][0].count += 1;
        }
        if (cur.classification2017) {
          acum[cur.classification2017][1].count += 1;
        }
        return acum;
      }, initialObj);
    }
    return (
      <div>
        <h1> Evolución entre 2015 y 2017</h1>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <AggregatedChart width={1200} height={600} />
        )}
      </div>
    );
  }
}

const ChartLayoutWithData = graphql(groupsQuery)(ChartLayout);
export default ChartLayoutWithData;
