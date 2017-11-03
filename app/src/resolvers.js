const { MongoClient } = require("mongodb");
const mongoURI = "mongodb://localhost/scienti-test";

const resolvers = {
  Query: {
    groups: async () => {
      try {
        const DB = await MongoClient.connect(mongoURI);
        const Groups = DB.collection("groups");
        const groups = await Groups.find({}).toArray();
        return groups;
      } catch (err) {
        console.error("Some error: ", err);
      }
    },
    group: async (root, args) => {
      try {
        const DB = await MongoClient.connect(mongoURI);
        const Groups = DB.collection("groups");
        const group = await Groups.findOne({ code: args.code });
        return group;
      } catch (err) {
        console.error("Some error: ", err);
      }
    }
  }
};

module.exports = { resolvers };
