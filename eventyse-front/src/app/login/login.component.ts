import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { LoginService } from 'src/services/login.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  loginFromGroup = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required]),
  });

  get emailFormControl() {
    return this.loginFromGroup.get('email');
  }

  loginSubscriber: any;

  isLoggedIn: boolean = false;

  constructor(private loginService: LoginService, private router: Router) {
    this.loginSubscriber = this.loginService.login.subscribe(isLoggedIn => {
      this.router.navigate(['dashboard'])
    });
  }

  ngOnInit(): void {
  }

  logIn(): void {
    let { email, password } = this.loginFromGroup.controls;
    this.loginService.doLogin(email.value, password.value);
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

}
