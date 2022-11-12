import { Component } from '@angular/core';
import { LoginService } from 'src/services/login.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'eventyse-front';

  loginSubscriber: any;

  isLoggedIn: boolean = false;

  constructor(private loginService: LoginService, private router: Router) {
    this.isLoggedIn = this.loginService.isLogged();

    this.loginSubscriber = this.loginService.login.subscribe(isLoggedIn => {
      this.isLoggedIn = isLoggedIn;
    });
  }

  logOff() {
    this.loginService.doLogoff();
    this.router.navigate(['login']);
  }
}
