import React from 'react';
import {
  Grid,
  Segment,
  List,
  Container,
  Header,
  Loader
} from 'semantic-ui-react';
import { Query } from 'react-apollo';
import { gql } from 'apollo-boost';

import MembersBarChart from './membersBarChart';
import ProductsBarChart from './productsBarChart';
import ReportList from './reportList';
import ParallelCoordinates from './parallelCoordinatesChart';
import RequirementsModal from './requirementsModal';

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
          comparedValues
          order
          diff
        }
        profiles {
          abbreviation
          value
        }
      }
    }
  `;
  return (
    <Query query={groupDataQuery} variables={{ groupCode: match.params.code }}>
      {({ loading, error, data }) => {
        if (loading)
          return (
            <Container style={{ height: '100vh', position: 'relative' }}>
              <Loader size="massive" active>
                Cargando análisis
              </Loader>
            </Container>
          );
        if (error) return `Error!: ${error}`;
        return <Dashboard data={data.group} />;
      }}
    </Query>
  );
}

function Dashboard(props) {
  let { data } = props;

  const parallelData = data.profiles.map((val, idx) => {
    return {
      profileName: val['abbreviation'],
      value: val['value'],
      comparisonValue: data.report.comparedValues[idx].toFixed(3)
    };
  });

  const justA1Text = `En la gráfica anterior se observan dos curvas: la curva roja representa los valores de los perfiles para el grupo de investigación analizado  y la curva  verde representa el valor promedio de los perfiles dentro de la clasificación ${
    data.report.comparedClassification
  } en el área de ${data.bigKnowledgeArea}.
  `;
  const regularText = `En la gráfica anterior se observan cuatro curvas: la curva roja
  representa los valores de los perfiles para el grupo de
  investigación analizado. La curva verde y la amarilla representan el
  valor promedio de los perfiles dentro de la clasificación ${
    data.report.comparedClassification
  } y ${data.classification}
  respectivamente en el área de ${data.bigKnowledgeArea}. Finalmente la
  curva azul representa los valores en los perfiles para un
  grupo en la categoría ${
    data.report.comparedClassification
  } que sería el más cercano al que se
  presenta en este caso.`;

  return (
    <Container fluid>
      <Header style={{ fontSize: '2.5em' }}>{data.groupName}</Header>
      <Grid padded>
        <Grid.Row>
          <Grid.Column width={12}>
            <Segment raised>
              <h1>Comparación por perfiles</h1>
              <ParallelCoordinates
                classification={data.classification}
                knowledgeArea={data.bigKnowledgeArea}
                data={parallelData}
              />
              <br />
              <Container>
                {data.classification === 'A1' ? justA1Text : regularText}
              </Container>
            </Segment>
          </Grid.Column>
          <Grid.Column width={4}>
            <Segment>
              <h1>Estado del grupo</h1>
              <br />
              <List divided>
                <List.Item>
                  <List.Header as="h2">Código</List.Header>
                  <List.Description as="h3">{data.code}</List.Description>
                </List.Item>

                <br />
                <List.Item>
                  <List.Header as="h2">Clasifición actual</List.Header>
                  <List.Description as="h3">
                    {data.classification}
                  </List.Description>
                </List.Item>

                <br />
                <List.Item>
                  <List.Header as="h2">Gran area</List.Header>
                  <List.Description as="h3">
                    {data.bigKnowledgeArea}
                  </List.Description>
                </List.Item>

                <br />
                <List.Item>
                  <List.Header as="h2">Area</List.Header>
                  <List.Description as="h3">
                    {data.knowledgeArea}
                  </List.Description>
                </List.Item>

                <br />
                <List.Item>
                  <List.Header as="h2">Institución</List.Header>
                  <List.Description as="h3">
                    {data.institution}
                  </List.Description>
                </List.Item>

                <br />
                <List.Item>
                  <RequirementsModal
                    classification={data.classification}
                    targetClassification={data.report.comparedClassification}
                  />
                </List.Item>
              </List>
            </Segment>
          </Grid.Column>
        </Grid.Row>

        <Grid.Row columns={2}>
          <Grid.Column width={7}>
            <Segment padded raised>
              <h1
                style={{ marginBottom: '2em' }}
              >{`Diferencia de perfiles con respecto al ${
                data.classification === 'A1' ? 'promedio' : 'grupo más cercano'
              } de la categoria ${data.report.comparedClassification}`}</h1>
              <ReportList reportData={data.report} />
            </Segment>
          </Grid.Column>

          <Grid.Column width={9}>
            <Grid.Row>
              <Segment padded raised>
                <h1>Integrantes del grupo</h1>
                <MembersBarChart membersData={data.membersProfile} />
              </Segment>
            </Grid.Row>
            <br />
            <Grid.Row>
              <Segment textAlign="center" raised>
                <h1>Producción 2012 - 2018</h1>
                <ProductsBarChart productsCount={data.productsCount} />
              </Segment>
            </Grid.Row>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </Container>
  );
}
