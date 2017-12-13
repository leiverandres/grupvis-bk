const { MongoClient } = require('mongodb');
const mongoURI = 'mongodb://localhost:27017/scienti-test';

const resolvers = {
  Query: {
    groups: async () => {
      try {
        const DB = await MongoClient.connect(mongoURI);
        const Groups = DB.collection('groups');
        const groups = await Groups.find({}).toArray();
        return groups;
      } catch (err) {
        console.error('Some error: ', err);
      }
    },
    group: async (root, args) => {
      try {
        const DB = await MongoClient.connect(mongoURI);
        const Groups = DB.collection('groups');
        const group = await Groups.findOne({ code: args.code });
        return group;
      } catch (err) {
        console.error('Some error: ', err);
      }
    },
    products: async () => {
      try {
        const DB = await MongoClient.connect(mongoURI);
        const Groups = DB.collection('groups');
        const groups = await Groups.find({}).toArray();
        let products = [];
        groups.forEach(group => {
          products = [...products, ...group.products];
        });
        return products;
      } catch (err) {
        console.error('Some error: ', err);
      }
    },
    product: async (root, args) => {
      try {
        const DB = await MongoClient.connect(mongoURI);
        const Groups = DB.collection('groups');
        const groups = await Groups.find({}).toArray();
        let products = [];
        groups.forEach(group => {
          const filteredProducts = group.products.filter(p => {
            return p.category === args.category;
          });
          products = [...products, ...filteredProducts];
        });
        return products;
      } catch (err) {
        console.error('Some error: ', err);
      }
    }
  }
};

module.exports = { resolvers };
