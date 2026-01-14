import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { KeycloakService } from 'keycloak-angular';
import { environment } from '../../environments/environment';

export const authGuard: CanActivateFn = async () => {
  if (!environment.authEnabled) {
    return true;
  }

  const keycloak = inject(KeycloakService);
  const loggedIn = await keycloak.isLoggedIn();
  if (loggedIn) {
    return true;
  }
  await keycloak.login();
  return false;
};
