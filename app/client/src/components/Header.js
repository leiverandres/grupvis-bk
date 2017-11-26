import React, { Component } from 'react';
import { Container, Grid, Image, Icon } from 'semantic-ui-react';

// import background from '../../public/particles.png';
// import logoWithText from '../../public/logo_sirius_text.svg';
const background = '/particles.png';
const logoWithText = '/logo_sirius_text.svg';

const bannerStyle = {
  backgroundImage: `url(${background})`,
  width: '100%',
  height: '25%',
  marginBottom: '5%'
};

const containerStyle = { paddingTop: '2em', width: '100%' };

class Header extends Component {
  render() {
    const { handleToggleVisibility } = this.props;
    return (
      <div style={bannerStyle}>
        <Container style={containerStyle}>
          <Grid>
            <Grid.Column width={1}>
              <Icon
                name="bars"
                onClick={handleToggleVisibility}
                size="large"
                color="grey"
                style={{ marginLeft: '25px', left: '25px' }}
              />
            </Grid.Column>
            <Grid.Column mobile={16} tablet={16} computer={8}>
              <Image
                src={logoWithText}
                alt="Grupo de Investigación Sirius"
                size="medium"
              />
            </Grid.Column>
          </Grid>
        </Container>
      </div>
    );
  }
}
export default Header;
