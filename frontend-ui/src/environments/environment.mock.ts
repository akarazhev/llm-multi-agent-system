export const environment = {
  production: false,
  mock: true,
  apiUrl: 'http://localhost:8000/api', // Not used in mock mode
  wsUrl: 'ws://localhost:8000/ws',     // Not used in mock mode
  authEnabled: false,
  keycloak: {
    url: 'http://localhost:8081',
    realm: 'llm-agents',
    clientId: 'llm-agent-ui'
  }
};
