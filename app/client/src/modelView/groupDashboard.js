import React from 'react';
import {
  Grid,
  Image,
  Segment,
  List,
  Container,
  Divider
} from 'semantic-ui-react';
import { Query } from 'react-apollo';
import { gql } from 'apollo-boost';

import MembersBarChart from './membersBarChart';
import ProductsBarChart from './productsBarChart';
import ReportList from './reportList';
import im from '../parallel.png';

export default function GroupDashboard({ match }) {
  const groupDataQuery = gql`
    query GetGroup($groupCode: String!) {
      group(code: $groupCode) {
        groupName
        code
        bigKnowledgeArea
        knowledgeArea
        institution
        classification
        membersProfile {
          memberType
          abbreviation
          value
        }
        productsCount {
          approvedCount
          productType
          noApprovedCount
        }
        report {
          comparedClassification
          order
          diff
        }
      }
    }
  `;
  return (
    <Query query={groupDataQuery} variables={{ groupCode: match.params.code }}>
      {({ loading, error, data }) => {
        if (loading) return <h3>Loading ...</h3>;
        if (error) return `Error!: ${error}`;

        return <Dashboard data={data.group} />;
      }}
    </Query>
  );
}

function Dashboard(props) {
  let { data } = props;
  const BasicInfo = (
    <Container textAlign="left">
      <h3>Estado actual del grupo</h3>
      <List>
        <List.Item>
          <List.Header>Clasifición actual</List.Header>
          {data.classification}
        </List.Item>
        <List.Item>
          <List.Header>Gran area</List.Header>
          {data.bigKnowledgeArea}
        </List.Item>
        <List.Item>
          <List.Header>Area</List.Header>
          {data.knowledgeArea}
        </List.Item>
        <List.Item>
          <List.Header>Institución</List.Header>
          {data.institution}
        </List.Item>
      </List>
    </Container>
  );
  return (
    <Container fluid>
      <h1>{`${data.groupName} (${data.code})`}</h1>
      <Grid padded celled>
        <Grid.Row columns={2}>
          <Grid.Column width={9}>
            <Grid.Row>
              <Segment padded raised>
                <h2>Integrantes del grupo</h2>
                <MembersBarChart membersData={data.membersProfile} />
              </Segment>
            </Grid.Row>
            <br />
            <Grid.Row>
              <Segment textAlign="center" raised>
                <h3>Producción 2012 - 2018</h3>
                <ProductsBarChart productsCount={data.productsCount} />
              </Segment>
            </Grid.Row>
          </Grid.Column>

          <Grid.Column width={7}>
            <Segment padded raised>
              <h2>Reporte</h2>
              <Grid padded>
                <h3>Estado del grupo</h3>
                <Grid.Row textAlign="left" columns="equal">
                  <Grid.Column>
                    <List>
                      <List.Item>
                        <List.Header>Clasifición actual</List.Header>
                        {data.classification}
                      </List.Item>
                      <List.Item>
                        <List.Header>Gran area</List.Header>
                        {data.bigKnowledgeArea}
                      </List.Item>
                    </List>
                  </Grid.Column>

                  <Grid.Column>
                    <List>
                      <List.Item>
                        <List.Header>Area</List.Header>
                        {data.knowledgeArea}
                      </List.Item>
                      <List.Item>
                        <List.Header>Institución</List.Header>
                        {data.institution}
                      </List.Item>
                    </List>
                  </Grid.Column>
                </Grid.Row>

                <Divider />

                <Grid.Row>
                  <h3
                  >{`Diferencia de perfiles con respecto al grupo más cercano de la categoria ${
                    data.report.comparedClassification
                  }`}</h3>
                </Grid.Row>

                <Grid.Row>
                  <ReportList reportData={data.report} />
                </Grid.Row>
              </Grid>
            </Segment>
          </Grid.Column>
        </Grid.Row>

        <Grid.Row>
          <Grid.Column>
            <Segment raised>
              <Image centered src={im} size="huge" />
              <p>
                At vero eos et accusamus et iusto odio dignissimos ducimus qui
                blanditiis praesentium voluptatum deleniti atque corrupti quos
                dolores et quas molestias excepturi sint occaecati cupiditate
                non provident, similique sunt in culpa qui officia deserunt
                mollitia animi, id est laborum et dolorum fuga. Et harum quidem
                rerum facilis est et expedita distinctio. Nam libero tempore,
                cum soluta nobis est eligendi optio cumque nihil impedit quo
                minus id quod maxime placeat facere possimus, omnis voluptas
                assumenda est, omnis dolor repellendus.
              </p>
            </Segment>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </Container>
  );
}
