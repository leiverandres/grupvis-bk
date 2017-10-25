const groups = [
  {
    code: "COL0009752",
    name: "soccer"
  },
  {
    code: "COL0009752",
    name: "baseball"
  }
];

const resolvers = {
  Query: {
    groups: () => {
      return groups;
    }
  }
};

module.exports = { resolvers };
