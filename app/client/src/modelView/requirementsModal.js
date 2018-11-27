import React from 'react';
import {
  Grid,
  List,
  Header,
  Modal,
  Button,
  Container
} from 'semantic-ui-react';

function Requirements({ classification }) {
  if (classification === 'A1') {
    return (
      <List bulleted>
        <List.Item>
          Tener un Indicador de Grupo que le permita estar en el Cuartil 1.
        </List.Item>
        <List.Item>
          Tener un indicador de Productos TOP que le permita estar en el Cuartil
          1.
        </List.Item>
        <List.Item>
          Tener un indicador de Productos Apropiación Social del Conocimiento
          mayor que Cero (0).
        </List.Item>
        <List.Item>
          Tener un indicador de Productos de actividades relacionadas con la
          Formación de Recurso Humano Tipo A mayor que Cero (0)*.
        </List.Item>
        <List.Item>
          Tener un (1) Investigador Sénior o Asociado como integrante del Grupo,
          que esté vinculado de manera contractual en una institución que haga
          parte del SNCTeI y que resida en Colombia.
        </List.Item>
        <List.Item>
          Tener un (1) indicador de Cohesión mayor que Cero (0).
        </List.Item>
        <List.Item>Tener al menos 5 años de existencia.</List.Item>
      </List>
    );
  } else if (classification === 'A') {
    return (
      <List bulleted>
        <List.Item>
          Tener un Indicador de Grupo que le permita estar en o por encima del
          Cuartil 2.
        </List.Item>
        <List.Item>
          Tener un indicador de Productos TOP o de Productos A mayor que Cero
          (0).
        </List.Item>
        <List.Item>
          Tener un indicador de Productos Apropiación Social del Conocimiento
          mayor que Cero (0).
        </List.Item>
        <List.Item>
          Tener un indicador de Productos de actividades relacionadas con la
          Formación de Recurso Humano - Tipo A mayor que Cero (0)*.
        </List.Item>
        <List.Item>
          Tener un (1) Investigador Sénior o Asociado como integrante del Grupo,
          que esté vinculado de manera contractual en una institución que haga
          parte del SNCTeI y que resida en Colombia.
        </List.Item>
        <List.Item>
          Tener un (1) indicador de Cohesión mayor que Cero.
        </List.Item>
        <List.Item>Tener al menos cinco (5) años de existencia.</List.Item>
      </List>
    );
  } else if (classification === 'B') {
    return (
      <List bulleted>
        <List.Item>
          Tener un Indicador de Grupo que le permita estar en o por encima del
          Cuartil 3.
        </List.Item>
        <List.Item>
          Tener un indicador de Productos TOP o de Productos A mayor que Cero
          (0).
        </List.Item>
        <List.Item>
          Tener un indicador de Productos Apropiación Social del Conocimiento
          mayor que Cero (0).
        </List.Item>
        <List.Item>
          Tener un indicador de Productos de actividades relacionadas con la
          Formación de Recurso Humano - Tipo A mayor que Cero (0) o tener un
          indicador de Productos de actividades relacionadas con la Formación de
          Recurso Humano - Tipo B que le permita estar en o por encima del
          Cuartil 2.
        </List.Item>
        <List.Item>
          Tener un (1) Investigador Sénior o Asociado o Junior o un Integrante
          Vinculado con Doctorado como integrante del Grupo, que esté vinculado
          de manera contractual en una institución que haga parte del SNCTeI y
          que resida en Colombia.
        </List.Item>
        <List.Item>
          Tener un (1) indicador de Cohesión mayor que Cero.
        </List.Item>
        <List.Item>Tener al menos tres (3) años de existencia.</List.Item>
      </List>
    );
  } else if (classification === 'C') {
    return (
      <List bulleted>
        <List.Item>Tener un Indicador de Grupo mayor que Cero (0).</List.Item>
        <List.Item>
          Tener un indicador de Productos TOP o de Productos A mayor que Cero
          (0).
        </List.Item>
        <List.Item>
          Tener un indicador de Productos Apropiación Social del Conocimiento
          mayor que Cero (0).
        </List.Item>
        <List.Item>
          Tener un indicador de Productos de actividades relacionadas con la
          Formación de Recurso Humano - Tipo A o Tipo B mayor que Cero (0).
        </List.Item>
        <List.Item>Tener al menos dos (2) años de existencia.</List.Item>
      </List>
    );
  }
}

export default function RequirementsModal(props) {
  return (
    <Modal trigger={<Button>Ver requerimientos de clasificación</Button>}>
      <Modal.Header>Requerimientos para clasificaciones</Modal.Header>
      <Modal.Content>
        <Modal.Description>
          <Grid columns="equal">
            {props.classification !== 'reconocido' && (
              <Grid.Column>
                <Container>
                  <Header>{`Clasificación ${props.classification}`}</Header>
                  <Requirements classification={props.classification} />
                </Container>
              </Grid.Column>
            )}
            {props.classification !== 'A1' && (
              <Grid.Column>
                <Container>
                  <Header>{`Clasificación ${
                    props.targetClassification
                  }`}</Header>
                  <Requirements classification={props.targetClassification} />
                </Container>
              </Grid.Column>
            )}
          </Grid>
        </Modal.Description>
      </Modal.Content>
    </Modal>
  );
}
