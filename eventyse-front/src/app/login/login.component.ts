import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { LoginService } from 'src/services/login.service';
import { Router } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  loginFromGroup = new FormGroup({
    email: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required]),
  });

  get emailFormControl() {
    return this.loginFromGroup.get('email');
  }

  isLoggedIn: boolean = false;

  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(private loginService: LoginService, private router: Router) {}

  ngOnInit(): void {
  }

  logIn(): void {
    let { email, password } = this.loginFromGroup.controls;
    this.loginService.doLogin(email.value, password.value)
    .pipe(takeUntil(this.destroy$))
    .subscribe(
      (result) => {
        if (result) {
          this.loginService.setToken(result.username, result.token);

          this.router.navigate(['dashboard']);
        }
      })
    // .pipe(first())
    // .subscribe(
    //     data => {
    //         this.router.navigate([this.returnUrl]);
    //     },
    //     error => {
    //         this.alertService.error(error);
    //         this.loading = false;
    //     });;
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

}
