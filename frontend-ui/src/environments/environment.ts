export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  wsUrl: 'ws://localhost:8000/ws',
  authEnabled: true,
  keycloak: {
    url: 'http://localhost:8081',
    realm: 'llm-agents',
    clientId: 'llm-agent-ui'
  }
};
