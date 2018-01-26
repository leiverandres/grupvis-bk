import React, { Component } from 'react';
import { graphql } from 'react-apollo';
import gql from 'graphql-tag';
import Spinner from 'react-spinkit';
import { Header, List } from 'semantic-ui-react';

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

  let dataCount = [];
  groups.forEach(groupObj => {
    const { bigKnowledgeArea, faculty, name } = groupObj;
    let classification = '';
    if (year === '2017') {
      classification = groupObj.classification2017
        ? groupObj.classification2017 === 'reconocido'
          ? 'SC'
          : groupObj.classification2017
        : 'NP';
    } else {
      classification =
        groupObj.classification2015 === 'reconocido'
          ? 'Rec'
          : groupObj.classification2015 || 'SC';
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

  dataCount = Object.entries(countByBigArea).map(item => {
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
      <div style={{ minHeight: '100vh' }}>
        {loading ? (
          <Spinner name="cube-grid" style={styles.spinner} />
        ) : (
          <div>
            <Header style={{ fontSize: '3em' }}>
              Grupos de investigación por gran area
              <Header.Subheader>Clasificación 2015 vs 2017</Header.Subheader>
            </Header>
            <div style={{ marginLeft: '5%', textAlign: 'left', width: '50%' }}>
              <Header size="medium">Convenciones de siglas</Header>
              <List>
                <List.Item>
                  <List.Header>Reg</List.Header>
                  Grupos registrados en Colciencias, pero sin clasificación para
                  la convocatoria 737.
                </List.Item>
                <List.Item>
                  <List.Header>SC</List.Header>
                  Grupos reconocidos, pero sin clasificación.
                </List.Item>
                <List.Item>
                  <List.Header>NP</List.Header>
                  Grupos que no participaron en la convocatoria 781.
                </List.Item>
              </List>
            </div>
            <div style={{ marginTop: '4em' }}>
              <Header size="huge">Convocatoria 737 (2015)</Header>
              <BarChart
                dataArray={dataCount2015}
                classificationLabels={['A1', 'A', 'B', 'C', 'D', 'SC', 'Rec']}
                size={[500, 500]}
                width={1200}
                height={500}
                style={styles.chartContainer}
              />
              <Header size="huge">Convocatoria 781 (2017)</Header>
              <BarChart
                dataArray={dataCount2017}
                classificationLabels={['A1', 'A', 'B', 'C', 'SC', 'NP']}
                size={[500, 500]}
                width={1200}
                height={500}
              />
            </div>
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
