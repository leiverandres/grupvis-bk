import React, { Component } from 'react';
import { Grid } from 'semantic-ui-react';
import { Link } from 'react-router-dom';

import './VizList.css';

const cardsArray = [
  {
    img: '/grupviz/preview_viz_1.png',
    header: 'Grupos de investigación por gran área de conocimiento.',
    description: 'Sin descripción',
    linkPath: '/grupviz/big-area-viz'
  },
  {
    img: '/grupviz/preview_viz_2.png',
    header:
      'Comparación entre convocatorias 737 y 781 por grupo de investigación.',
    description: 'Sin descripción',
    linkPath: '/grupviz/classification-group'
  },
  {
    img: '/preview_viz_3.png',
    header: 'Cantidad de grupos de investigación agrupados por clasificación',
    description: 'Sin descripción',
    linkPath: '/grupviz/aggregated-groups'
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
