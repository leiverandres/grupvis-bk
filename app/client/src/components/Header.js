import React, { Component } from 'react';
import { Container, Grid, Image, Icon } from 'semantic-ui-react';

const background = '/particles.png';
const logoWithText = '/logo_sirius_text.svg';
const utpLogo = 'UTP-logo.svg';

const bannerStyle = {
  backgroundImage: `url(${background})`,
  width: '100%',
  height: '20%',
  marginBottom: '5%'
};

const containerStyle = { paddingTop: '2em', width: '100%' };

class Header extends Component {
  render() {
    const { handleToggleVisibility } = this.props;
    return (
      <div style={bannerStyle}>
        <Container style={containerStyle}>
          <Grid columns={3}>
            <Grid.Row>
              <Grid.Column width={2} textAlign="left">
                <Icon
                  name="bars"
                  onClick={handleToggleVisibility}
                  size="large"
                  color="grey"
                  style={{
                    marginLeft: '25px',
                    left: '25px',
                    cursor: 'pointer'
                  }}
                />
              </Grid.Column>
              <Grid.Column width={7}>
                <Image
                  src={logoWithText}
                  alt="Logo Grupo de Investigación Sirius"
                  size="medium"
                  href="/"
                  centered
                />
              </Grid.Column>
              <Grid.Column width={7}>
                <Image src={utpLogo} alt="Logo UTP" size="small" centered />
              </Grid.Column>
            </Grid.Row>
          </Grid>
        </Container>
      </div>
    );
  }
}
export default Header;
