import React, { Component } from 'react';
import { Grid } from 'semantic-ui-react';
import { Link } from 'react-router-dom';

import './VizList.css';

const cardsArray = [
  {
    img: '/preview_viz_1.png',
    header: 'Grupos de investigación por gran área de conocimiento',
    description: 'Descripción corta',
    linkPath: '/big-area-viz'
  },
  {
    img: 'https://static.pexels.com/photos/672802/pexels-photo-672802.jpeg',
    header: 'Grupos de investigación por gran área de conocimiento',
    description: 'Descripción corta',
    linkPath: '/big-area-viz'
  },
  {
    img: 'https://static.pexels.com/photos/672802/pexels-photo-672802.jpeg',
    header: 'Grupos de investigación por gran área de conocimiento',
    description: 'Descripción corta',
    linkPath: '/big-area-viz'
  },
  {
    img: 'https://static.pexels.com/photos/672802/pexels-photo-672802.jpeg',
    header: 'Grupos de investigación por gran área de conocimiento',
    description: 'Descripción corta',
    linkPath: '/big-area-viz'
  }
];

class VizList extends Component {
  render() {
    return (
      <div style={{ width: '80%', margin: '0 auto', paddingTop: '5%' }}>
        <Grid columns={3} centered stackable>
          {cardsArray.map((card, idx) => {
            return (
              <Grid.Column key={idx}>
                <Link to={card.linkPath}>
                  <div
                    className="gist gist-thumbnail"
                    style={{
                      backgroundImage: `url(${card.img})`
                    }}
                  >
                    <h3 className="gist-name">{card.header}</h3>
                  </div>
                </Link>
              </Grid.Column>
            );
          })}
        </Grid>
      </div>
    );
  }
}

export default VizList;
