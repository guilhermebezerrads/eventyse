import { Component } from '@angular/core';
import { LoginService } from 'src/services/login.service';
import { Router } from '@angular/router';
import { FormControl } from '@angular/forms';
import { throws } from 'assert';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'eventyse-front';

  loginSubscriber: any;

  isLoggedIn: boolean = false;

  searchFilterControl = new FormControl("");

  constructor(private loginService: LoginService, private router: Router) {
    this.isLoggedIn = this.loginService.isLogged();

    this.loginSubscriber = this.loginService.login.subscribe(isLoggedIn => {
      this.isLoggedIn = isLoggedIn;
    });
  }

  get loggedUsername() {
    return this.loginService.loggedUser?.username;
  }

  get loggedAvatar() {
    return this.loginService.loggedUser.avatar;
  }

  logOff() {
    this.loginService.doLogoff();
    this.router.navigate(['login']);
  }

  searchPosts() {
    this.router.navigate(['dashboard', { filterTag: this.searchFilterControl.value }])
  }
}
