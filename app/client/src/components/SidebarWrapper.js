import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Sidebar, Menu, Icon } from 'semantic-ui-react';

import { serverURL } from '../config.json';

class SidebarWrapper extends Component {
  render() {
    const { visible } = this.props;
    return (
      <Sidebar.Pushable style={{ minHeight: '100vh' }}>
        <Sidebar
          as={Menu}
          animation="push"
          width="thin"
          visible={visible}
          icon="labeled"
          vertical
          inverted
        >
          <Menu.Item name="home" as={Link} to="/grupviz">
            <Icon name="grid layout" />
            Inicio
          </Menu.Item>
          <Menu.Item name="reports" as={Link} to="/grupviz/groups-table">
            <Icon name="table" />
            Reportes
          </Menu.Item>
          <Menu.Item name="analysis" href={`${serverURL}/analysis-file`}>
            <Icon name="cubes" />
            Analisis
          </Menu.Item>
          <Menu.Item name="gamepad">
            <Menu.Header>Enlaces de interes</Menu.Header>
            <Menu.Menu>
              <Menu.Item href="http://sirius.utp.edu.co/" target="_blank">
                Grupo de investigación Sirius
              </Menu.Item>
              <Menu.Item
                href="http://www.utp.edu.co/vicerrectoria/investigaciones/"
                target="_blank"
              >
                Vicerrectoría de Investigaciones, Innovación y Extensión
              </Menu.Item>
            </Menu.Menu>
          </Menu.Item>
        </Sidebar>
        <Sidebar.Pusher>{this.props.children}</Sidebar.Pusher>
      </Sidebar.Pushable>
    );
  }
}

export default SidebarWrapper;
