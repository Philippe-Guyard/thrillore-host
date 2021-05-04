//This is an external service, meaning that it is open to the public with a request prefix: '/auth'
//This should only work with tokens and different auth methods. No user management...
const path = require('path');
require('dotenv').config({path: path.join(__dirname, '.env')});

const fs = require('fs');

const rawdata = fs.readFileSync('points.json');
const filePoints = JSON.parse(rawdata);

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

app.get('/api/leaderboard', async (req, res, next) => {    try {
        const {users} = await userService.getUsers();

        let points = users.map(user => {
            return {handle: user.login, points: Number.parseInt(user.thrillorePts) || 0}
        });
        for (let obj of filePoints) {
            obj.points = Number.parseInt(obj.points);
            const old = points.find(x => x.handle == obj.handle);
            if (old)
                old.points += obj.points;
            else
                points.push(obj);
        }

        points.sort((a, b) => (a.points < b.points ? 1 : -1))
        points = points.map((x, idx) => {
            return {...x, rank: idx + 1}
        }).slice(0, 25);

        return res.json({points: points, count: points.length});
    }
    catch (err) {
        return next(err);
    }
});

app.use((error, req, res, next) => {
   console.error(error);
   
   return res.status(500).send('Thrillore server internal error');
});

app.listen(constants.PORT, () => {
    console.log('Server up and running');
});