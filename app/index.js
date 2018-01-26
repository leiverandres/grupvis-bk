const { graphqlExpress, graphiqlExpress } = require('apollo-server-express');
const bodyParser = require('body-parser');
const cors = require('cors');
const express = require('express');
const path = require('path');
const morgan = require('morgan');
const compression = require('compression');

const { schema } = require('./src/schema');

const PORT = process.env.PORT || 4000;
const app = express();

app.use(morgan('tiny'));
app.use(compression());
app.use(cors());
app.use('/grupviz', express.static(path.resolve(__dirname, 'client', 'build')));

app.use(
  '/grupviz/graphql',
  bodyParser.json(),
  graphqlExpress({
    schema
  })
);

app.use(
  '/grupviz/graphiql',
  graphiqlExpress({
    endpointURL: '/graphql'
  })
);

app.get('/grupviz/download-report', (req, res) => {
  const filePath = './files/general_report.csv';
  res.download(filePath, 'reporte_general.csv');
});

app.get('/grupviz/download-products', (req, res) => {
  const filePath = './files/products_report.csv';
  res.download(filePath, 'reporte_productos.csv');
});

app.get('/grupviz/analysis', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'files', 'Comparación_737_781.html'));
});

app.get('/grupviz/*', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'client', 'build', 'index.html'));
});

app.listen(PORT, () => {
  console.info(`Running on port ${PORT}`);
});
