//This is an external service, meaning that it is open to the public with a request prefix: '/auth'
//This should only work with tokens and different auth methods. No user management...
const path = require('path');
require('dotenv').config({path: path.join(__dirname, '.env')});

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

app.get('/api/leaderboard', async (req, res, next) => {
    const USERS_PER_PAGE = 50;
    const page = req.query.page || 1;
    try {
        const {users, total} = await userService.getUsers(USERS_PER_PAGE, USERS_PER_PAGE * (page - 1));

        let points = users.map(user => {
            return {login: user.login, points: user.thrillorePts || 0}
        });

        points = points.sort((a, b) => a.points < b.points);
        points = points.map((x, idx) => {
            return {...x, rank: idx + 1}
        });

        let lastPage = Math.floor(total / USERS_PER_PAGE) + 1;
        if (total % USERS_PER_PAGE == 0)
            lastPage -= 1;

        return res.json({points: points, count: points.length, lastPage: lastPage});
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