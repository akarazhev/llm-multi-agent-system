export const environment = {
  production: true,
  apiUrl: '/api',
  wsUrl: `wss://${window.location.host}/ws`,
  authEnabled: true,
  keycloak: {
    url: 'https://keycloak.example.com',
    realm: 'llm-agents',
    clientId: 'llm-agent-ui'
  }
};
