import React, { Component } from 'react';
import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import ReactTable from 'react-table';
import Spinner from 'react-spinkit';
import 'react-table/react-table.css';

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
      <div>
        <h1>Grupos de investigación UTP</h1>
        <div>
          {loading ? (
            <Spinner />
          ) : (
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
              pivotBy={['code']}
              nextText="Siguiente"
              previousText="Anterior"
              pageText="Página"
              rowsText="Filas"
              ofText="De"
            />
          )}
        </div>
      </div>
    );
  }
}

const GroupsTableWithData = graphql(groupsQuery)(GroupsTableLayout);
export default GroupsTableWithData;
