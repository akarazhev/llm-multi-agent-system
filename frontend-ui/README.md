# LLM Multi-Agent System - Frontend UI

Modern Angular 20 frontend for the LLM Multi-Agent System with Material Design.

## 🚀 Features

- **Dashboard** - Overview of agents and workflows
- **Workflows** - Create, manage, and monitor workflows
- **Agents** - View status of all AI agents
- **Real-time Updates** - Live status updates from backend
- **Material Design 3** - Modern, beautiful UI
- **Responsive** - Works on all screen sizes
- **Type-safe** - Full TypeScript support

## 📋 Prerequisites

- Node.js 20+ or 22+ or 24+
- npm 10.8.0+
- Angular CLI 20+

## 🛠️ Installation

```bash
# Install dependencies
npm install

# Development server
npm start

# Build for production
npm run build:prod
```

## 🏃 Development

```bash
# Start dev server (http://localhost:4200)
npm start

# Run tests
npm test

# Lint code
npm run lint
```

## 📦 Build

```bash
# Development build
npm run build

# Production build
npm run build:prod
```

## 🎨 Architecture

### Components

- **Shared Components**
  - Sidenav - Navigation menu
  
- **Pages**
  - Dashboard - Main overview
  - Workflows - Workflow management
  - Workflow Detail - Individual workflow details
  - Agents - Agent status overview

### Services

- **AgentService** - Manage agent data
- **WorkflowService** - Manage workflows

### Interfaces

- **Agent** - Agent model
- **Workflow** - Workflow model
- **WorkflowState** - Workflow state model

## 🔧 Configuration

### Environment Variables

Edit `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  wsUrl: 'ws://localhost:8000/ws'
};
```

## 🎨 Styling

- **Material Design 3** with custom SPP theme
- **SCSS** for styling
- **Responsive** grid layouts
- **Custom color palette** from SPP project

### Theme Colors

- Primary: `#3061D5` (Blue)
- Secondary: `#F17B2C` (Orange)
- Tertiary: `#3b82f6` (Light Blue)

## 📱 Responsive Breakpoints

- Mobile: < 600px
- Tablet: 600px - 900px
- Desktop: > 900px

## 🧪 Testing

```bash
# Run unit tests
npm test

# Run with coverage
npm run test:coverage
```

## 🚀 Deployment

### Production Build

```bash
npm run build:prod
```

Output will be in `dist/llm-agent-ui/`.

### Serve Production Build

```bash
# Install serve globally
npm install -g serve

# Serve the build
serve -s dist/llm-agent-ui
```

## 🔗 Backend Integration

The frontend connects to the Python FastAPI backend:

- **API URL**: `http://localhost:8000/api`
- **WebSocket**: `ws://localhost:8000/ws`

Make sure the backend is running before starting the frontend.

## 📚 Documentation

- [Angular Documentation](https://angular.dev)
- [Angular Material](https://material.angular.io)
- [TypeScript](https://www.typescriptlang.org)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🛠️ Tech Stack

- **Angular 20** - Framework
- **TypeScript 5.9** - Language
- **Angular Material 20** - UI Components
- **RxJS 7.8** - Reactive programming
- **SCSS** - Styling

## 📞 Support

For issues or questions, please open an issue on GitHub.
