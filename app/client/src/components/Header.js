import React, { Component } from 'react';
import { Container, Grid, Image } from 'semantic-ui-react';

// import background from '../../public/particles.png';
// import logoWithText from '../../public/logo_sirius_text.svg';
const background = '/particles.png';
const logoWithText = '/logo_sirius_text.svg';

const bannerStyle = {
  backgroundImage: `url(${background})`,
  width: '100%',
  height: '250px'
};

const containerStyle = { paddingTop: '100px' };

class Header extends Component {
  render() {
    return (
      <div style={bannerStyle}>
        <Container style={containerStyle}>
          <Grid>
            <Grid.Row>
              <Grid.Column mobile={16} tablet={16} computer={8}>
                <Image
                  src={logoWithText}
                  alt="Grupo de Investigación Sirius"
                  size="medium"
                />
              </Grid.Column>
            </Grid.Row>
          </Grid>
        </Container>
      </div>
    );
  }
}
export default Header;
