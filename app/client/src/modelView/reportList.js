import React, { Component } from 'react';
import {
  Header,
  Table,
  Button,
  Popup,
  List,
  Container
} from 'semantic-ui-react';
import { profilesMapping, productSubtypes } from './reportMapping';

class ReportList extends Component {
  state = {
    max: 12,
    compactView: true
  };

  handleSeeMoreClick = () => {
    this.setState({ compactView: false, max: 38 });
  };

  handleSeeLessClick = () => {
    this.setState({ compactView: true, max: 12 });
  };

  render() {
    const { max, compactView } = this.state;
    const { reportData } = this.props;
    const aggregatedList = reportData.diff
      .map((val, idx) => {
        return { name: reportData.order[idx], diffValue: val };
      })
      .sort((a, b) => {
        return b.diffValue - a.diffValue;
      });
    const reportList = aggregatedList
      .slice(0, max)
      .filter(item => item.diffValue > 0)
      .map((item, idx) => {
        const mappedProfileName = profilesMapping[item.name];
        const additionalList = productSubtypes[item.name];
        return (
          <Table.Row key={`report-row-${item.name}`}>
            {additionalList ? (
              <Popup
                trigger={
                  <Table.Cell>
                    <Header as="h4">
                      <Header.Content>{`${mappedProfileName} (${
                        item.name
                      })`}</Header.Content>
                    </Header>
                  </Table.Cell>
                }
                key={`report-row-${idx}`}
              >
                <Popup.Content>
                  <List bulleted>
                    {additionalList.map((additionalMsg, idx) => (
                      <List.Item key={`sub-msg-${item.name}-${idx}`}>
                        {additionalMsg}
                      </List.Item>
                    ))}
                  </List>
                </Popup.Content>
              </Popup>
            ) : (
              <Table.Cell>
                <Header as="h4">
                  <Header.Content>{`${mappedProfileName} (${
                    item.name
                  })`}</Header.Content>
                </Header>
              </Table.Cell>
            )}
            <Table.Cell>{item.diffValue.toFixed(3)}</Table.Cell>
          </Table.Row>
        );
      });
    return (
      <Container>
        <Table basic="very" celled>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>
                Nombre del perfil (abreviatura)
              </Table.HeaderCell>
              <Table.HeaderCell>Diferencia</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>{reportList}</Table.Body>
        </Table>
        {compactView ? (
          <Button onClick={this.handleSeeMoreClick} size="small">
            Ver mas
          </Button>
        ) : (
          <Button onClick={this.handleSeeLessClick} size="small">
            Ver menos
          </Button>
        )}
      </Container>
    );
  }
}

export default ReportList;
