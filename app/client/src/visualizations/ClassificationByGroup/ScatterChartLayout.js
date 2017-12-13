import React, { Component } from 'react';
import { graphql } from 'react-apollo';
import gql from 'graphql-tag';
import Spinner from 'react-spinkit';
import { Header, Dropdown } from 'semantic-ui-react';

import Scatterplot from './Scatterplot';

const knowledgeAreaQuery = gql`
  query KnowledgeAreaQuery {
    groups {
      code
      name
      classification2015
      classification2017
    }
  }
`;

class BarChartLayout extends Component {
  state = {
    selected: {}
  };

  handleOptionChange = (ev, { value }) => {
    this.setState({ selected: value });
  };

  render() {
    const { data: { loading, groups } } = this.props;
    const { selected } = this.state;
    let options = [];
    let selectedData = {};
    if (!loading) {
      groups.forEach(element => {
        options.push({
          key: element.code,
          value: element.code,
          text: element.name
        });
      });
      if (selected) {
        selectedData = groups.find(item => selected === item.code);
      }
    }

    return (
      <div style={{ minHeight: '100vh', width: '80%', margin: '0 auto' }}>
        {loading ? (
          <Spinner name="cube-grid" style={styles.spinner} />
        ) : (
          <div>
            <Header size="huge">
              Comparación entre convocatorias 737 y 781 por grupo de
              investigación.
            </Header>
            <Dropdown
              placeholder="Seleccionar un grupo"
              search
              selection
              options={options}
              fluid
              onChange={this.handleOptionChange}
              loading={loading}
            />
            {selectedData && (
              <Scatterplot
                data={selectedData}
                width={1000}
                height={500}
                style={styles.chartContainer}
              />
            )}
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
