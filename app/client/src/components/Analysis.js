import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { serverURL } from '../config.json';

class Analysis extends Component {
  state = {
    comp_html: ''
  };
  componentDidMount() {
    console.log('downloading html');
    window
      .fetch(`${serverURL}/download/analysis-file`)
      .then(res => res.text())
      .then(text => {
        console.log('res', text);
        this.setState({ comp_html: text });
      })
      .catch(err => console.log('Error:', err));
  }
  render() {
    return (
      <div>
        <Link
          to="http://localhost:5000/grupviz/download/analysis-file"
          target="_self"
        >
          click me
        </Link>
        <div dangerouslySetInnerHTML={{ __html: this.state.comp_html }} />
      </div>
    );
  }
}

export default Analysis;
