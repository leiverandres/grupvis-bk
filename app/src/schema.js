const {
  makeExecutableSchema,
  addMockFunctionsToSchema
} = require("graphql-tools");
const { resolvers } = require("./resolvers");

const typeDefs = `
type Group {
    code: ID!,
    name: String!
}

type Query {
  groups: [Group]
}
`;

const schema = makeExecutableSchema({ typeDefs, resolvers });

module.exports = { schema };
