const { MongoClient } = require('mongodb');

const ENV = process.env.NODE_ENV || 'development';
const mongoHost = ENV === 'production' ? 'mongo' : 'localhost';
const mongoDBName = ENV === 'production' ? 'col-scienti' : 'col-scienti-dev';
const mongoURI = `mongodb://${mongoHost}:27017`;
// const mongoURI = `mongodb://${mongoHost}:27017/${mongoDBName}`;
console.log(`MongoDB uri: ${mongoURI}`);

const resolvers = {
  Report: {
    comparedClassification: parent => {
      return parent['targetClassification'];
    },
    comparedKnowledgeArea: parent => {
      return parent['bigKnowledgeArea'];
    },
    comparedValues: parent => {
      return parent['closestValues'];
    }
  },
  Group: {
    membersProfile: parent => {
      // parent is comple group data object
      const rows = parent.profiles['members_profile_table']['rows_values'];
      const members = rows.map(elem => {
        return {
          memberType: elem['Tipo de integrante'],
          abbreviation: elem['abreviatura'],
          value: elem['Valor del indicador para el Grupo']
        };
      });
      return members;
    },
    profiles: parent => {
      console.log('hi');
      const { profiles } = parent;
      const aggregated_profiles = [];
      for (let value of Object.values(profiles)) {
        const rows = value['rows_values'];
        rows.forEach(row => {
          const profileItem = {
            profileName:
              row['Subtipo de producto'] ||
              row['Tipo de integrante'] ||
              row['Indicador'],
            abbreviation: row['abreviatura'],
            value: row['Valor del indicador para el Grupo']
          };
          console.log(profileItem);
          aggregated_profiles.push(profileItem);
        });
      }
      return aggregated_profiles;
    },
    report: async parent => {
      const client = new MongoClient(mongoURI, { useNewUrlParser: true });
      const groupSummary = parent.summary.values;
      try {
        console.log(`Trying to connect to ${mongoDBName}`);
        await client.connect();
        console.log('Connected correctly to server');
        const db = client.db(mongoDBName);
        const groupsCollection = db.collection('groups');
        const group = await groupsCollection.findOne({
          code: parent.code
        });
        const profileReport = group.closestGroupInfo;
        const diff = group.closestGroupInfo.closestValues.map((val, idx) =>
          Math.abs(val - Number(groupSummary[idx]))
        );
        profileReport['diff'] = diff;
        return profileReport || [];
      } catch (err) {
        console.error('Error getting groups: ', err);
      }
      client.close();
    }
  },
  Query: {
    groups: async () => {
      const client = new MongoClient(mongoURI, { useNewUrlParser: true });
      try {
        console.log(`Trying to connect to ${mongoDBName}`);
        await client.connect();
        console.log('Connected correctly to server');
        const db = client.db(mongoDBName);
        const groupsCollection = db.collection('groups');
        const groups = await groupsCollection
          .find({})
          .limit(100)
          .toArray();
        return groups;
      } catch (err) {
        console.error('Error getting groups: ', err);
      }
      client.close();
    },
    groupsByInstitution: async (_, args) => {
      const client = new MongoClient(mongoURI, { useNewUrlParser: true });
      try {
        await client.connect();
        console.log('Connected correctly to server');
        const db = client.db(mongoDBName);
        const groupsCollection = db.collection('groups');
        const groups = await groupsCollection
          .find({ institution: args.institution })
          .toArray();
        return groups;
      } catch (err) {
        console.error('Error getting groups: ', err);
      }
      client.close();
    },
    group: async (root, args) => {
      const client = new MongoClient(mongoURI, { useNewUrlParser: true });
      try {
        await client.connect();
        console.log('Connected correctly to server');
        const db = client.db(mongoDBName);
        const groupsCollection = db.collection('groups');
        const group = await groupsCollection.findOne({ code: args.code });
        return group;
      } catch (err) {
        console.error(`Error getting group with code ${args.code}: `, err);
      }
      client.close();
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
