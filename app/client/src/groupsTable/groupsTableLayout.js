import React, { Component } from 'react';
import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import ReactTable from 'react-table';
import Spinner from 'react-spinkit';
import { Button, Icon, Grid, Header } from 'semantic-ui-react';
import 'react-table/react-table.css';

import { serverURL } from '../config.json';

const groupsQuery = gql`
  query GroupsInfo {
    groups {
      code
      name
      faculty
      dependency
      classification2017
      classification2015
      leader
      knowledgeArea
    }
  }
`;

class GroupsTableLayout extends Component {
  render() {
    const { data: { loading, groups } } = this.props;
    return (
      <Grid>
        <Grid.Row centered>
          <Header style={{ fontSize: '3em' }}>
            Grupos de investigación UTP
          </Header>
        </Grid.Row>
        <Grid.Row style={{ justifyContent: 'right', marginRight: '2%' }}>
          <Button.Group>
            <Button
              labelPosition="left"
              icon
              href={`${serverURL}/download-report`}
            >
              <Icon name="download" />
              Descargar información general
            </Button>
            <Button.Or text="o" />
            <Button href={`${serverURL}/download-products`}>
              Descargar productos de los grupos
            </Button>
          </Button.Group>
        </Grid.Row>
        <Grid.Row>
          {loading ? (
            <Spinner />
          ) : (
            <Grid.Column width={16}>
              <ReactTable
                data={groups}
                columns={[
                  { Header: 'Código', accessor: 'code' },
                  { Header: 'Nombre', accessor: 'name' },
                  { Header: 'Líder', accessor: 'leader' },
                  { Header: 'Area de conocimiento', accessor: 'knowledgeArea' },
                  { Header: 'Facultad', accessor: 'faculty' },
                  { Header: 'Departamento', accessor: 'dependency' },
                  {
                    Header: 'Clasificación (737)',
                    accessor: 'classification2015'
                  }
                ]}
                nextText="Siguiente"
                previousText="Anterior"
                pageText="Página"
                rowsText="Filas"
                ofText="De"
              />
            </Grid.Column>
          )}
        </Grid.Row>
      </Grid>
    );
  }
}

const GroupsTableWithData = graphql(groupsQuery)(GroupsTableLayout);
export default GroupsTableWithData;
