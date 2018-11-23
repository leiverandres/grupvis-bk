import React from 'react';
import { Loader, Container } from 'semantic-ui-react';
import { Query } from 'react-apollo';
import { gql } from 'apollo-boost';

import GroupsSearchBox from './GroupSearchBox';

const groupsUTPQuery = gql`
  query GetGroups($institution: String!) {
    groupsByInstitution(institution: $institution) {
      groupName
      code
    }
  }
`;

const variables = {
  institution: 'Universidad Tecnológica De Pereira - Utp'
};

export default function SearchBoxView() {
  return (
    <Query query={groupsUTPQuery} variables={variables}>
      {({ loading, error, data }) => {
        if (error) return `Error!: ${error}`;
        return (
          <Container style={{ height: '100vh', position: 'relative' }}>
            {loading ? (
              <Loader size="massive" active>
                Cargando
              </Loader>
            ) : (
              <GroupsSearchBox source={data.groupsByInstitution} />
            )}
          </Container>
        );
      }}
    </Query>
  );
}
