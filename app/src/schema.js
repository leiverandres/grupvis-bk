const { gql } = require('apollo-server-express');

const typeDefs = gql`
  type Member {
    name: String
    profileURL: String
    rol: String
    dedicatedHours: String
    startingDate: String
    endingDate: String
  }

  type Product {
    category: String
    type: String
    description: String
    isApproved: Boolean
    code: String
    title: String
    year: String
  }

  type Group {
    code: String!
    groupName: String!
    grouplacURL: String
    leader: String
    profilesURL: String
    classification: String
    classifiedOn: String
    foundationDate: String
    departament: String
    city: String
    certificationDate: String
    website: String
    email: String
    bigKnowledgeArea: String
    knowledgeArea: String
    nationalProgramOfScienceAndTechnology: String
    secondaryNationalProgramOfScienceAndTechnology: String
    institutions: [String]
    strategicPlan: String
    researchLines: [String]
    applicationFields: [String]
    members: [Member]
    products: [Product]
  }

  type Query {
    groups: [Group]
    group(code: String!): Group
    products: [Product]
    product(category: String): [Product]
  }
`;

module.exports = { typeDefs };
