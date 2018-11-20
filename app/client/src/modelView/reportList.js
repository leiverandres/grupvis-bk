import React, { Component } from 'react';
import {
  Header,
  Table,
  Button,
  Popup,
  List,
  Container
} from 'semantic-ui-react';
import {
  profilesMapping,
  membersProfile,
  colaborationProfile,
  productSubtypes
} from './reportMapping';

function buildMessage(abbreviatedProfile) {
  const mappedProfileName = profilesMapping[abbreviatedProfile];
  if (membersProfile.includes(abbreviatedProfile)) {
    return `Incrementar la cantidad de miembros tipo ${mappedProfileName}`;
  } else if (colaborationProfile.includes(abbreviatedProfile)) {
    return `Aumentar el ${mappedProfileName}`;
  } else {
    return `Aumentar la producción de ${mappedProfileName}`;
  }
}

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
    const reportList = aggregatedList.slice(0, max).map((item, idx) => {
      const mappedProfileName = profilesMapping[item.name];
      if (item.diffValue !== 0) {
        const ROW = (
          <Table.Row key={idx}>
            <Table.Cell>
              <Header as="h4">
                <Header.Content>{mappedProfileName}</Header.Content>
              </Header>
            </Table.Cell>
            <Table.Cell>{item.diffValue.toFixed(3)}</Table.Cell>
          </Table.Row>
        );
        const additionalList = productSubtypes[item.name];
        if (additionalList) {
          return (
            <Popup trigger={ROW}>
              <Popup.Content>
                <List bulleted>
                  {additionalList.map(additionalMsg => (
                    <List.Item>{additionalMsg}</List.Item>
                  ))}
                </List>
              </Popup.Content>
            </Popup>
          );
        } else {
          return ROW;
        }
      }
    });
    return (
      <Container>
        <Table basic="very" celled>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Perfiles</Table.HeaderCell>
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
