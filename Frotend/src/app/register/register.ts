import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class Register {
  registerForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.registerForm = this.fb.group({
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required],
      rol: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.registerForm.valid) {
      console.log('Formulario enviado:', this.registerForm.value);
      // Aquí iría la lógica para registrar el usuario
    }
  }

  onCancel(): void {
    // Lógica para cancelar y regresar
    console.log('Registro cancelado');
  }
}