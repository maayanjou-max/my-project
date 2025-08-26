module.exports = {
  apps: [{
    name: 'drug-agent',
    script: 'python3',
    args: 'run_server.py',
    cwd: '/home/user/webapp/drug_agent',
    instances: 1,
    exec_mode: 'fork',
    env: {
      PORT: 5000,
      DEBUG: false
    },
    log_file: './drug_agent.log',
    error_file: './drug_agent_error.log',
    out_file: './drug_agent_out.log',
    time: true
  }]
};