import React, { Component } from "react";
import { graphql, ApolloProvider } from "react-apollo";
import ApolloClient from "apollo-client";
import { HttpLink } from "apollo-link-http";
import { InMemoryCache } from "apollo-cache-inmemory";
import gql from "graphql-tag";

import logo from "./logo.svg";
import "./App.css";
import BarChart from "./components/BarChart";

const client = new ApolloClient({
  link: new HttpLink({ uri: "http://localhost:4000/graphql" }),
  cache: new InMemoryCache().restore(window.__APOLLO_STATE__ || {})
});

const groupsListQuery = gql`
  query GroupsListQuery {
    groups {
      code
      name
    }
  }
`;

const GroupsList = ({ data: { loading, error, groups } }) => {
  if (loading) {
    return <p>Loading ...</p>;
  }
  if (error) {
    return <p>{error.message}</p>;
  }
  return (
    <ul>
      {groups.map(gr => (
        <li key={gr.code}>
          {gr.code} - {gr.name}
        </li>
      ))}
    </ul>
  );
};

const GroupsListWithData = graphql(groupsListQuery)(GroupsList);

class App extends Component {
  render() {
    return (
      <ApolloProvider client={client}>
        <div className="App">
          <h2>Gran area</h2>
          <BarChart size={[500, 500]} width={500} height={500} />
        </div>
      </ApolloProvider>
    );
  }
}

export default App;
