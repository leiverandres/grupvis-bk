const { MongoClient } = require('mongodb');

const resolvers = {
  Query: {
    groups: async () => {
      try {
        const DB = await MongoClient.connect(
          'mongodb://localhost/scienti-test'
        );
        const Groups = DB.collection('groups');
        const groups = await Groups.find({}).toArray();
        console.log('groups', groups);
        return groups;
      } catch (err) {
        console.error('Some error: ', err);
      }
    }
  }
};

module.exports = { resolvers };
