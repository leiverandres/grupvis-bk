import React, { Component } from 'react';
import { graphql } from 'react-apollo';
import gql from 'graphql-tag';
import Spinner from 'react-spinkit';
import { Header } from 'semantic-ui-react';

import BarChart from './BarChart';
import './BarChart.css';

const knowledgeAreaQuery = gql`
  query KnowledgeAreaQuery {
    groups {
      code
      name
      bigKnowledgeArea
      knowledgeArea
      classification2015
      classification2017
      faculty
      dependency
    }
  }
`;

/**
 * Take care with this function it's a little complicated
 * TODO: explain this
 * @param {Array} groups
 * @param {String} year
 */
function summarizeClassifications(groups, year) {
  const countByBigArea = {};
  groups.forEach(groupObj => {
    const { bigKnowledgeArea, faculty, name } = groupObj;
    let classification = '';
    if (year === '2017') {
      // TODO: handle in a better way reconocido.
      classification =
        groupObj.classification2017 === 'Reconocido'
          ? 'Reg'
          : groupObj.classification2017 || 'Reg';
    } else {
      classification = groupObj.classification2015 || 'Reg';
    }
    if (countByBigArea[bigKnowledgeArea]) {
      // already exist an big area object
      if (countByBigArea[bigKnowledgeArea][classification]) {
        // already exist an counter of area inside this big area
        if (countByBigArea[bigKnowledgeArea][classification][faculty]) {
          countByBigArea[bigKnowledgeArea][classification][faculty].push(name);
        } else {
          countByBigArea[bigKnowledgeArea][classification][faculty] = [name];
        }
      } else {
        // no couter of area inside big area object
        countByBigArea[bigKnowledgeArea][classification] = {
          [faculty]: [name]
        };
      }
    } else {
      // no big area object found
      countByBigArea[bigKnowledgeArea] = {
        [classification]: {
          [faculty]: [name]
        }
      };
    }
  });

  const dataCount = Object.entries(countByBigArea).map(item => {
    return {
      bigAreaName: item[0],
      classifications: Object.entries(item[1]).map(subitem => {
        const counter = {};
        let total = 0;
        Object.entries(subitem[1]).forEach(entry => {
          counter[entry[0]] = entry[1].length;
          total += entry[1].length;
        });
        return {
          classification: subitem[0],
          total: total,
          ...counter
        };
      })
    };
  });
  return dataCount;
}

class BarChartLayout extends Component {
  render() {
    const { data: { loading, groups } } = this.props;

    let dataCount2015 = [];
    let dataCount2017 = [];
    if (!loading) {
      dataCount2015 = summarizeClassifications(groups, '2015');
      dataCount2017 = summarizeClassifications(groups, '2017');
    }

    return (
      <div>
        {loading ? (
          <Spinner name="cube-grid" style={styles.spinner} />
        ) : (
          <div>
            <Header size="huge">
              Grupos de investigación por gran area
              <Header.Subheader>Clasificación 2015 vs 2017</Header.Subheader>
            </Header>

            <BarChart
              dataArray={dataCount2015}
              size={[500, 500]}
              width={1200}
              height={500}
              style={styles.chartContainer}
            />
            <BarChart
              dataArray={dataCount2017}
              size={[500, 500]}
              width={1200}
              height={500}
            />
          </div>
        )}
      </div>
    );
  }
}

const styles = {
  spinner: {
    height: '4em',
    width: '4em',
    position: 'absolute',
    top: '50%',
    left: '50%',
    margin: '-2em 0 0 -2em'
  },
  chartContainer: {
    marginBottom: '50px'
  }
};

const BarChartWithData = graphql(knowledgeAreaQuery)(BarChartLayout);
export default BarChartWithData;
