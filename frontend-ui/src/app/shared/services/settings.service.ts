import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface LlmSettings {
  baseUrl: string;
  apiKey?: string | null;
  model?: string | null;
  timeout?: number | null;
}

@Injectable({ providedIn: 'root' })
export class SettingsService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  getLlmSettings() {
    return this.http.get<LlmSettings>(`${this.apiUrl}/settings/llm`).pipe(
      catchError(() =>
        of({
          baseUrl: 'http://127.0.0.1:8080/v1',
          apiKey: '',
          model: 'devstral',
          timeout: 300
        })
      )
    );
  }

  updateLlmSettings(payload: LlmSettings) {
    return this.http.put<LlmSettings>(`${this.apiUrl}/settings/llm`, payload).pipe(
      catchError(() => of(undefined))
    );
  }
}
