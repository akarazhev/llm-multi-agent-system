import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config.mock';

console.log(`
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        🎭  MOCK MODE ENABLED  🎭                          ║
║                                                            ║
║  Running with mock data - no backend required!            ║
║  All API calls will be intercepted and mocked.            ║
║                                                            ║
║  Check console for [MOCK] prefixed logs                   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
`);

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
