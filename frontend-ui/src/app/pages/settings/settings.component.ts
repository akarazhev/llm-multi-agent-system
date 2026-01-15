import { ChangeDetectionStrategy, Component, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { SettingsService } from '../../shared/services/settings.service';

@Component({
  selector: 'app-settings',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatSnackBarModule
  ],
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SettingsComponent {
  private readonly settingsService = inject(SettingsService);
  private readonly snackBar = inject(MatSnackBar);
  private readonly fb = inject(FormBuilder);

  loading = signal(true);
  saving = signal(false);

  form = this.fb.group({
    baseUrl: ['', [Validators.required]],
    apiKey: [''],
    model: ['devstral'],
    timeout: [300, [Validators.min(1)]]
  });

  constructor() {
    this.loadSettings();
  }

  loadSettings(): void {
    this.loading.set(true);
    this.settingsService.getLlmSettings().subscribe(settings => {
      this.form.patchValue({
        baseUrl: settings.baseUrl,
        apiKey: settings.apiKey ?? '',
        model: settings.model ?? 'devstral',
        timeout: settings.timeout ?? 300
      });
      this.loading.set(false);
    });
  }

  save(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.saving.set(true);
    const payload = {
      baseUrl: this.form.get('baseUrl')?.value ?? '',
      apiKey: this.form.get('apiKey')?.value ?? '',
      model: this.form.get('model')?.value ?? 'devstral',
      timeout: this.form.get('timeout')?.value ?? 300
    };

    this.settingsService.updateLlmSettings(payload).subscribe(result => {
      this.saving.set(false);
      if (result) {
        this.snackBar.open('Settings saved', 'Close', {
          duration: 3000,
          horizontalPosition: 'end',
          verticalPosition: 'top'
        });
      }
    });
  }
}
