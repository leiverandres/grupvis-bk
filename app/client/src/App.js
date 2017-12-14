import React, { Component } from 'react';
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-client';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { BrowserRouter, Route } from 'react-router-dom';

import './App.css';
import Header from './components/Header';
import SidebarWrapper from './components/SidebarWrapper';
import VizList from './components/VizList';
import UnderConstruction from './components/UnderConstruction';
import BarChartLayout from './visualizations/BigAreaBarChart/BarChartLayout';
import ScatterChartLayout from './visualizations/ClassificationByGroup/ScatterChartLayout';
import GroupsTable from './groupsTable/groupsTableLayout';
import { serverURL } from './config.json';

const client = new ApolloClient({
  link: new HttpLink({ uri: `${serverURL}/graphql` }),
  cache: new InMemoryCache().restore(window.__APOLLO_STATE__ || {})
});

class App extends Component {
  state = { visible: false };

  toggleVisibility = () => {
    this.setState({ visible: !this.state.visible });
  };

  render() {
    const { visible } = this.state;

    return (
      <ApolloProvider client={client}>
        <BrowserRouter>
          <SidebarWrapper visible={visible}>
            <div className="App">
              <Header handleToggleVisibility={this.toggleVisibility} />
              <Route exact path="/" component={VizList} />
              <Route
                exact
                path="/under-construction"
                component={UnderConstruction}
              />
              <Route
                path="/big-area-viz"
                render={() => (
                  <BarChartLayout size={[500, 500]} width={500} height={500} />
                )}
              />
              <Route
                exact
                path="/classification-group"
                component={ScatterChartLayout}
              />
              <Route path="/groups-table" component={GroupsTable} />
            </div>
          </SidebarWrapper>
        </BrowserRouter>
      </ApolloProvider>
    );
  }
}

export default App;
