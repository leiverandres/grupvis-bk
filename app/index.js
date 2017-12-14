const { graphqlExpress, graphiqlExpress } = require('apollo-server-express');
const bodyParser = require('body-parser');
const cors = require('cors');
const express = require('express');
const path = require('path');
const morgan = require('morgan');

const { schema } = require('./src/schema');

const PORT = 4000;
const app = express();

app.use(morgan('tiny'));
app.use(cors());
app.use(express.static(path.resolve(__dirname, 'client', 'build')));

app.use(
  '/graphql',
  bodyParser.json(),
  graphqlExpress({
    schema
  })
);

app.use(
  '/graphiql',
  graphiqlExpress({
    endpointURL: '/graphql'
  })
);

app.get('/download-report', (req, res) => {
  const filePath = './files/cleaned_up.csv';
  res.download(filePath, 'report.csv');
});

app.get('/*', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'client', 'build', 'index.html'));
});

app.listen(PORT, () => {
  console.info(`Running on port ${PORT}`);
});
