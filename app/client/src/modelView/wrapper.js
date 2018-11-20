import Fuse from 'fuse.js';
import React, { Component } from 'react';
import { Search, Grid, Label } from 'semantic-ui-react';
import { Query } from 'react-apollo';
import { gql } from 'apollo-boost';
import { Redirect } from 'react-router-dom';

const resultRenderer = ({ code }) => {
  return (
    <div key={code}>
      <Label content={code} color="blue" />
    </div>
  );
};

const initialState = {
  isLoading: false,
  results: [],
  value: '',
  selection: ''
};

class GroupsSearchBar extends Component {
  state = initialState;

  constructor(props) {
    super(props);
    var options = {
      shouldSort: true,
      findAllMatches: true,
      threshold: 0.6,
      location: 0,
      distance: 100,
      maxPatternLength: 32,
      minMatchCharLength: 1,
      keys: ['title', 'code']
    };
    this.fuse = new Fuse(this.props.source, options);
  }

  componentWillMount() {
    this.resetComponent();
  }

  resetComponent = () => this.setState(initialState);

  handleResultSelect = (e, { result }) =>
    this.setState({ value: result.title, selection: result.code });

  handleSearchChange = (e, { value }) => {
    const results = this.fuse.search(value);
    this.setState({ value, results });
  };

  render() {
    const { isLoading, value, results, selection } = this.state;
    console.log(results);
    if (selection !== '') {
      return <Redirect to={`/grupviz/dashboard/${selection}`} />;
    }
    return (
      <Grid style={{ height: '100vh' }}>
        <Grid.Column>
          <h1>Titulo de la APP</h1>
          <Search
            loading={isLoading}
            onResultSelect={this.handleResultSelect}
            onSearchChange={this.handleSearchChange}
            // resultRenderer={resultRenderer}
            results={results}
            value={value}
          />
        </Grid.Column>
      </Grid>
    );
  }
}

export default function SearchView() {
  const groupsQuery = gql`
    query GetGroups($institution: String!) {
      groupsByInstitution(institution: $institution) {
        title: groupName
        code
      }
    }
  `;
  const variables = {
    institution: 'Universidad Tecnológica De Pereira - Utp'
  };
  return (
    <Query query={groupsQuery} variables={variables}>
      {({ loading, error, data }) => {
        if (loading) return loading;
        if (error) return `Error!: ${error}`;
        return <GroupsSearchBar source={data.groupsByInstitution} />;
      }}
    </Query>
  );
}
