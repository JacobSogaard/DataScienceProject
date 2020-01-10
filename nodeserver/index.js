//Sets up dev environment
const express = require('express');
const app = express();
const PORT = 8080;

//  Database
const { Client } = require('pg');
const client = new Client();
client.connect();

app.use(express.static(__dirname + '/public'));

app.get('/', (req, res) => res.send(JSON.stringify(client)));

app.get('/cities', (req, res) => {
  client.query('SELECT * from cities', (err, results) => {
    if (err) {
      console.log('error: ' + err);
      throw err;
    }
    res.send(JSON.stringify(results.rows));
  });
});

app.get('/centers', (req, res) => {
  client.query('SELECT * from clustercenters;', (err, results) => {
    if (err) {
      console.log('error: ' + err);
      throw err;
    }
    res.send(JSON.stringify(results.rows));
  });
});

app.get('/clustercenters', (req, res) => {
  client.query(
    'SELECT * from kmeansoutput INNER JOIN clustercenters ON clustercenters.id = kmeansoutput.cluster;',
    (err, results) => {
      if (err) {
        console.log('error: ' + err);
        throw err;
      }
      res.send(JSON.stringify(results.rows));
    }
  );
});

app.get('/clusterdata/:cluster', (req, res) => {
  var cluster = req.params.cluster;
  client.query(
    `SELECT * from kmeansoutput WHERE cluster = ${cluster} ORDER BY percent DESC LIMIT 10;`,
    (err, results) => {
      if (err) {
        console.log('error: ' + err);
        throw err;
      }
      res.send(JSON.stringify(results.rows));
    }
  );
});

app.listen(PORT, () => {
  console.log('Server running on port: ' + PORT);
});
