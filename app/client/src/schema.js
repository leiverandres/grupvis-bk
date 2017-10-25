export const typeDefs = `
  type Group {
    code: ID!,
    name: String!
  }

  type Query {
    groups: [Group]
  }

`;
