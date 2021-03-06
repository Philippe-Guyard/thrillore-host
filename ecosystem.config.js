module.exports = {
  apps : [{
    name: 'thrillore',
    script: 'app.js',
    out_file: 'logs/out.log',
    err_fille: 'logs/err.log',
    log_file: 'logs/combined.log',
    time: true
  }],
  deploy : {
    production : {
      user : 'SSH_USERNAME',
      host : 'SSH_HOSTMACHINE',
      ref  : 'origin/master',
      repo : 'GIT_REPOSITORY',
      path : 'DESTINATION_PATH',
      'pre-deploy-local': '',
      'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production',
      'pre-setup': ''
    }
  }
};
