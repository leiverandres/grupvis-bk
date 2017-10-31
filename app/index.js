const { graphqlExpress, graphiqlExpress } = require('apollo-server-express');
const bodyParser = require('body-parser');
const cors = require('cors');
const express = require('express');

const { schema } = require('./src/schema');

const PORT = 4000;
const app = express();

app.use(cors());

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

app.listen(PORT, () => {
  console.info(`Running on port ${PORT}`);
});
