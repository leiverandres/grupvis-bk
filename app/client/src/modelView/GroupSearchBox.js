import Fuse from 'fuse.js';
import React, { Component } from 'react';
import { Search, Container, Label } from 'semantic-ui-react';
import { Redirect } from 'react-router-dom';

const initialState = {
  results: [],
  value: '',
  selection: ''
};

function GroupRowResult({ groupName, code }) {
  return (
    <Label color="blue">
      {groupName}
      <Label.Detail>{code}</Label.Detail>
    </Label>
  );
}

export default class GroupsSearchBox extends Component {
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
      keys: ['groupName', 'code']
    };
    this.fuse = new Fuse(this.props.source, options);
  }

  componentWillMount() {
    this.resetComponent();
  }

  resetComponent = () => this.setState(initialState);

  handleResultSelect = (e, { result }) =>
    this.setState({ value: result.groupName, selection: result.code });

  handleSearchChange = (e, { value }) => {
    const results = this.fuse.search(value);
    this.setState({ value, results });
  };

  render() {
    const { value, results, selection } = this.state;
    if (selection !== '') {
      return <Redirect to={`/grupviz/dashboard/${selection}`} />;
    }
    return (
      <Container style={{ position: 'relative', top: '20%' }}>
        <h1 style={{ fontSize: '3em' }}>
          Buscar grupo por código o por nombre
        </h1>
        <Search
          fluid
          onResultSelect={this.handleResultSelect}
          onSearchChange={this.handleSearchChange}
          resultRenderer={GroupRowResult}
          results={results}
          value={value}
        />
      </Container>
    );
  }
}
