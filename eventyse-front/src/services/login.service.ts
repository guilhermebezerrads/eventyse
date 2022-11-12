import { User } from '../models/user.model';
import { EventEmitter } from '@angular/core';

export class LoginService {
  loggedUser: User = new User();

  login: EventEmitter<any> = new EventEmitter();

  doLogin(user: User): void {
    this.loggedUser = user;
    localStorage.setItem('currentUser', JSON.stringify(user));
    this.login.emit(true);
  }

  doLogoff(): void {
    this.loggedUser = new User();
    localStorage.removeItem('currentUser');
    this.login.emit(false);
  }

  isLogged(): boolean {
    return localStorage.getItem('currentUser') != null;
  }

  // doLogin(username: string, password: string) {
  //   return this.http.post<any>(`/users/authenticate`, { username: username, password: password })
  //       .pipe(map(user => {
  //           // login successful if there's a jwt token in the response
  //           if (user && user.token) {
  //               // store user details and jwt token in local storage to keep user logged in between page refreshes
  //               localStorage.setItem('currentUser', JSON.stringify(user));
  //           }

  //           return user;
  //       }));
  // }

  // doLogoff() {
  //     // remove user from local storage to log user out
  //     localStorage.removeItem('currentUser');
  // }
}
