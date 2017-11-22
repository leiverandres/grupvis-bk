import React, { Component } from 'react';
import { Card, Image } from 'semantic-ui-react';

const cardsArray = [
  {
    img: 'https://static.pexels.com/photos/672802/pexels-photo-672802.jpeg',
    header: 'Grupos mostrados por Gran Area de investigación',
    description: 'Descripción corta',
    linkPath: '/big-area-viz'
  },
  {
    img: 'https://static.pexels.com/photos/672802/pexels-photo-672802.jpeg',
    header: 'Grupos mostrados por Gran Area de investigación',
    description: 'Descripción corta',
    linkPath: '/big-area-viz'
  },
  {
    img: 'https://static.pexels.com/photos/672802/pexels-photo-672802.jpeg',
    header: 'Grupos mostrados por Gran Area de investigación',
    description: 'Descripción corta',
    linkPath: '/big-area-viz'
  },
  {
    img: 'https://static.pexels.com/photos/672802/pexels-photo-672802.jpeg',
    header: 'Grupos mostrados por Gran Area de investigación',
    description: 'Descripción corta',
    linkPath: '/big-area-viz'
  }
];

class VizList extends Component {
  state = {
    hoverdCard: null
  };

  handleMouseEnter = cardIdx => {
    this.setState({ hoverdCard: cardIdx });
  };

  handleMouseLeave = cardIdx => {
    this.setState({ hoverdCard: null });
  };
  render() {
    const { hoverdCard } = this.state;
    return (
      <div style={{ width: '80%', margin: '0 auto', paddingTop: '10%' }}>
        <Card.Group itemsPerRow="2" stackable>
          {cardsArray.map((card, idx) => {
            return (
              <Card
                key={idx}
                raised={hoverdCard === idx}
                onMouseEnter={() => this.handleMouseEnter(idx)}
                onMouseLeave={this.handleMouseLeave}
                href={card.linkPath}
              >
                <Image src={card.img} />
                <Card.Content>
                  <Card.Header>{card.header}</Card.Header>
                  <Card.Description>{card.description}</Card.Description>
                </Card.Content>
              </Card>
            );
          })}
        </Card.Group>
      </div>
    );
  }
}

export default VizList;
