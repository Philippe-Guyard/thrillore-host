//This is an external service, meaning that it is open to the public with a request prefix: '/auth'
//This should only work with tokens and different auth methods. No user management...
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '.env') });

const constants = require('./constants.js');

const express = require('express');
const morgan = require('morgan');

const userService = require('./services/users');

const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use(morgan('short'));

app.get('/api/hello', (req, res) => {
    res.sendStatus(200);
});

app.use((error, req, res, next) => {
    console.error(error);

    return res.status(500).send('Thrillore server internal error');
});

app.listen(constants.PORT, () => {
    console.log('Server up and running');
});