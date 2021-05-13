//TODO: We need to implement offset in user service
const {USER_HOST} = require('../constants');

const axios = require('axios');

exports.getUsers = async () => {
    const fetchResult = await axios.get(`${USER_HOST}/thrillore`);
    return {users: fetchResult.data.users, total: fetchResult.data.total};
}