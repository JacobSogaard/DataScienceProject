//Sets up dev environment
const express = require('express');
const app = express();
const PORT = 8080;
const HOST = 'localhost';



//  Database
const { Client } = require('pg');
const client = new Client({
    user: 'docker',
    host: 'database',
    database: 'postgres',
    password: 'docker',
    port: '5432'
});

client.query('CREATE TABLE testtable(id SERIAL PRIMARY KEY, testdata VARCHAR(80))');


app.get('/', (req, res) => res.send('hello world'));

app.get('/insert', (req, res) => {
    pool.query('INSERT INTO testtable(testdata) VALUES ("hej")', (err, result) => {
        if(err) {
            throw err;
        }
        res.send('success');
    });
});

app.listen(PORT, () => {
    console.log('Server running on port: ' + PORT);
})

// app.use(bodyParser.json())
// app.use(bodyParser.urlencoded({extended: false}))

// app.use(express.static(__dirname + '/public'));

// console.log('creating table');
// pool.query('CREATE TABLE testtable(id SERIAL PRIMARY KEY, testdata VARCHAR(80))')


// app.get('/', (req, res) => {
//     console.log('requesting : /');
//     return res.status(200).json({message: "hello"});
//     pool.query('INSERT INTO testtable(testdata) VALUES ("hej")', (err, result) => {
//         if(err) {
//             throw err;
//         }
//         res.status(200).json(result)
//     });
// })

// app.listen(PORT, HOST, () => {
//     console.log(`Running on: ${HOST}:${PORT}`)
// });