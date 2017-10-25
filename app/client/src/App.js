import React, { Component } from "react";
import { makeExecutableSchema, addMockFunctionsToSchema } from "graphql-tools";
import { mockNetworkInterfaceWithSchema } from "apollo-test-utils";
import { gql, graphql, ApolloProvider } from "react-apollo";
import { ApolloClient } from "apollo-client";

import { typeDefs } from "./schema";
import logo from "./logo.svg";
import "./App.css";

const schema = makeExecutableSchema({ typeDefs });
addMockFunctionsToSchema({ schema });

const mockNetworkInterface = mockNetworkInterfaceWithSchema({ schema });
const client = new ApolloClient({
  networkInterface: mockNetworkInterface
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
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <h1 className="App-title">Welcome to Colciencias viz app</h1>
          </header>
          <GroupsListWithData />
        </div>
      </ApolloProvider>
    );
  }
}

export default App;
