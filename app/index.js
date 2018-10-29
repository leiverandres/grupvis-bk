const express = require('express');
const { ApolloServer } = require('apollo-server-express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const morgan = require('morgan');
const compression = require('compression');

const { schemak, typeDefs } = require('./src/schema');
const { resolvers } = require('./src/resolvers');

const PORT = process.env.PORT || 5000;
const server = new ApolloServer({ typeDefs, resolvers });
const app = express();

app.use(morgan('tiny'));
app.use(compression());
app.use(cors());
app.use('/grupviz', express.static(path.resolve(__dirname, 'client', 'build')));
app.use('/grupviz', express.static(path.resolve(__dirname, 'files')));

app.get('/grupviz/download-report', (req, res) => {
  res.sendFile(
    path.resolve(__dirname, 'files', 'general_report.csv'),
    'reporte_general.csv'
  );
});

app.get('/grupviz/download-products', (req, res) => {
  res.sendFile(
    path.resolve(__dirname, 'files', 'products_report.csv'),
    'reporte_productos.csv'
  );
});

app.get('/grupviz/analysis-file', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'files', 'Comparación_737_781.html'));
});

app.get('/grupviz/*', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'client', 'build', 'index.html'));
});

server.applyMiddleware({ app });
app.listen(PORT, () => {
  console.info(`Running on port ${PORT}`);
  console.log(server.graphqlPath);
});
