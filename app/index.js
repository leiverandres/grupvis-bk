const express = require("express");
const bodyParser = require("body-parser");
const { graphqlExpress, graphiqlExpress } = require("apollo-server-express");

const { schema } = require("./src/schema");

const PORT = 3000;

var app = express();

app.use(
  "/graphql",
  bodyParser.json(),
  graphqlExpress({
    schema
  })
);

app.use(
  "/graphiql",
  graphiqlExpress({
    endpointURL: "/graphql"
  })
);

app.listen(PORT, () => {
  console.info(`Running on port ${PORT}`);
});
