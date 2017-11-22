import React, { Component } from 'react';
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-client';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { BrowserRouter, Route } from 'react-router-dom';

import './App.css';
import VizList from './components/VizList';
import BarChartLayout from './visualizations/BigAreaBarChart/BarChartLayout';

const client = new ApolloClient({
  link: new HttpLink({ uri: 'http://localhost:4000/graphql' }),
  cache: new InMemoryCache().restore(window.__APOLLO_STATE__ || {})
});

class App extends Component {
  render() {
    return (
      <ApolloProvider client={client}>
        <BrowserRouter>
          <div className="App">
            <Route exact path="/" component={VizList} />
            <Route
              path="/big-area-viz"
              render={() => (
                <BarChartLayout size={[500, 500]} width={500} height={500} />
              )}
            />
          </div>
        </BrowserRouter>
      </ApolloProvider>
    );
  }
}

export default App;
