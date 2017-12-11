import React, { Component } from "react";
import { Header, Icon } from "semantic-ui-react";

class UnderConstruction extends Component {
  render() {
    return (
      <Header as="h1" icon>
        <Icon name="setting" />
        Estamos trabajando en ello
        <Header.Subheader>
          Esta página no esta disponible aún. Pedimos perdon por las molestias.
        </Header.Subheader>
      </Header>
    );
  }
}

export default UnderConstruction;
