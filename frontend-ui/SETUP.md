# Frontend UI Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend-ui
npm install
```

### 2. Start Development Server

```bash
npm start
```

The application will be available at `http://localhost:4200`

### 3. Backend Connection

Make sure the Python backend is running:

```bash
# From project root
cd ..
source venv/bin/activate
python main.py
```

Backend API should be running at `http://localhost:8000`

---

## 📦 Available Scripts

| Script | Description |
|--------|-------------|
| `npm start` | Start dev server (port 4200) |
| `npm run build` | Build for development |
| `npm run build:prod` | Build for production |
| `npm test` | Run unit tests |
| `npm run lint` | Lint TypeScript files |

---

## 🏗️ Project Structure

```
frontend-ui/
├── src/
│   ├── app/
│   │   ├── core/               # Core interfaces and models
│   │   │   └── interfaces/     # TypeScript interfaces
│   │   ├── pages/              # Page components
│   │   │   ├── dashboard/      # Dashboard page
│   │   │   ├── workflows/      # Workflows list
│   │   │   ├── workflow-detail/# Workflow details
│   │   │   └── agents/         # Agents overview
│   │   ├── shared/             # Shared components & services
│   │   │   ├── components/     # Reusable components
│   │   │   └── services/       # HTTP services
│   │   ├── app.component.*     # Root component
│   │   ├── app.config.ts       # App configuration
│   │   └── app.routes.ts       # Routing configuration
│   ├── style/                  # Global styles
│   │   ├── spp_theme-colors.scss
│   │   └── material-variables.scss
│   ├── environments/           # Environment configs
│   ├── styles.scss             # Global styles entry
│   ├── index.html              # HTML entry
│   └── main.ts                 # Bootstrap entry
├── angular.json                # Angular CLI config
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
└── README.md                   # Documentation
```

---

## 🎨 Features

### Pages

1. **Dashboard** (`/dashboard`)
   - System overview
   - Agent status summary
   - Recent workflows
   - Quick stats

2. **Workflows** (`/workflows`)
   - All workflows list
   - Create new workflow
   - Filter and search
   - Workflow actions

3. **Workflow Detail** (`/workflows/:id`)
   - Detailed workflow information
   - Progress tracking
   - Files created
   - Error logs

4. **Agents** (`/agents`)
   - All agents overview
   - Agent status
   - Completed tasks count

### Services

- **AgentService** - Agent data management
- **WorkflowService** - Workflow CRUD operations

### Components

- **Sidenav** - Navigation menu
- Custom Material Design theme from SPP

---

## 🔧 Configuration

### API Endpoint

Edit `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',  // Change if backend runs on different port
  wsUrl: 'ws://localhost:8000/ws'       // WebSocket endpoint
};
```

### Theme Colors

Theme colors are defined in `src/style/spp_theme-colors.scss`:

- **Primary**: #3061D5 (Blue)
- **Secondary**: #F17B2C (Orange)  
- **Tertiary**: #3b82f6 (Light Blue)

---

## 🐛 Troubleshooting

### Port Already in Use

If port 4200 is busy, use a different port:

```bash
ng serve --port 4300
```

### CORS Issues

Make sure the Python backend has CORS enabled for `http://localhost:4200`

### Module Not Found

Clear node_modules and reinstall:

```bash
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors

Check TypeScript version (should be ~5.9.3):

```bash
npm list typescript
```

---

## 🚀 Production Build

### Build

```bash
npm run build:prod
```

Output will be in `dist/llm-agent-ui/`

### Deploy

1. **Static Hosting** (Nginx, Apache)
   - Copy `dist/llm-agent-ui/` to web server
   - Configure for SPA (redirect all to index.html)

2. **Docker**
   ```dockerfile
   FROM nginx:alpine
   COPY dist/llm-agent-ui /usr/share/nginx/html
   EXPOSE 80
   ```

3. **Backend Integration**
   - Serve static files from FastAPI
   - Update `apiUrl` to relative path `/api`

---

## 🧪 Testing

### Run Tests

```bash
npm test
```

### Test Coverage

```bash
npm run test:coverage
```

Coverage report will be in `coverage/` directory.

---

## 📱 Mobile Support

The UI is fully responsive and works on:

- Mobile devices (< 600px)
- Tablets (600px - 900px)
- Desktop (> 900px)

---

## 🎯 Next Steps

1. **Customize Theme**
   - Edit `src/style/spp_theme-colors.scss`
   - Modify Material palette

2. **Add Features**
   - Real-time updates via WebSocket
   - Workflow creation dialog
   - Agent configuration

3. **Integrate Backend**
   - Connect to Python FastAPI endpoints
   - Add authentication (if needed)
   - Implement WebSocket for live updates

---

## 📚 Resources

- [Angular Documentation](https://angular.dev)
- [Angular Material](https://material.angular.io)
- [RxJS](https://rxjs.dev)
- [TypeScript](https://www.typescriptlang.org)

---

**Happy coding! 🎉**
