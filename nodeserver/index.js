//Sets up dev environment
const express = require('express');
const app = express();
const PORT = 8080;

//  Database
const { Client } = require('pg');
const client = new Client();
client.connect();

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

app.listen(PORT, () => {
  console.log('Server running on port: ' + PORT);
});
