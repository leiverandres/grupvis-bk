import React, { Component } from 'react';
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-client';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { BrowserRouter, Route, Link } from 'react-router-dom';
import { Sidebar, Menu, Icon } from 'semantic-ui-react';

import './App.css';
import Header from './components/Header';
import SidebarWrapper from './components/SidebarWrapper';
import VizList from './components/VizList';
import BarChartLayout from './visualizations/BigAreaBarChart/BarChartLayout';

const client = new ApolloClient({
  link: new HttpLink({ uri: 'http://localhost:4000/graphql' }),
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
            <div className="App" style={{ heigth: '100%' }}>
              <Header handleToggleVisibility={this.toggleVisibility} />
              <Route exact path="/" component={VizList} />
              <Route
                path="/big-area-viz"
                render={() => (
                  <BarChartLayout size={[500, 500]} width={500} height={500} />
                )}
              />
            </div>
          </SidebarWrapper>
        </BrowserRouter>
      </ApolloProvider>
    );
  }
}

export default App;
