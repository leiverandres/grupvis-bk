const { makeExecutableSchema } = require('graphql-tools');
const { resolvers } = require('./resolvers');

const typeDefs = `
type Member {
  name: String,
  profileURL: String,
  rol: String,
  dedicatedHours: String,
  startingDate: String,
  endingDate: String
}

type Product {
  category: String,
  type: String,
  description: String,
  isApproved: Boolean
}

type Group {
  code: String!,
  name: String!,
  grouplacURL: String,
  website: String,
  email: String,
  city: String,
  leader: String,
  classificationDate: String,
  foundationDate: String,
  departament: String,
  city: String,
  certificationDate: String,
  classification2015: String,
  classification2017: String,
  bigKnowledgeArea: String,
  knowledgeArea: String,
  nationalProgramOfScienceAndTechnology: String,
  secondaryNationalProgramOfScienceAndTechnology: String,
  strategicPlan: String,
  institutions: [String],
  researchLines: [String],
  applicationFields: [String],
  members: [Member],
  products: [Product],
  faculty: String,
  dependency: String
}

type Query {
  groups: [Group]
  group(code: String!): Group
}
`;

const schema = makeExecutableSchema({ typeDefs, resolvers });

module.exports = { schema };
