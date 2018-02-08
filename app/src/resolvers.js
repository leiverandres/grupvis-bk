const { MongoClient } = require('mongodb');

const ENV = process.env.NODE_ENV || 'development';
const mongoHost = ENV === 'production' ? 'mongo' : 'localhost';
const mongoDBName = ENV === 'production' ? 'scienti' : 'scienti-test';
const mongoURI = `mongodb://${mongoHost}:27017/${mongoDBName}`;
console.log(`Connecting to ${mongoURI}`);

const resolvers = {
  Query: {
    groups: async () => {
      try {
        const DB = await MongoClient.connect(mongoURI);
        const Groups = DB.collection('groups');
        const groups = await Groups.find({}).toArray();
        return groups;
      } catch (err) {
        console.error('Error getting groups: ', err);
      }
    },
    group: async (root, args) => {
      try {
        const DB = await MongoClient.connect(mongoURI);
        const Groups = DB.collection('groups');
        const group = await Groups.findOne({ code: args.code });
        return group;
      } catch (err) {
        console.error(`Error getting group with code ${args.code}: `, err);
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
        console.error('Error getting products: ', err);
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
        console.error('Error getting single product type from groups: ', err);
      }
    }
  }
};

module.exports = { resolvers };
