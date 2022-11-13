import { ExtendedUser, User } from '../models/user.model';
import { EventEmitter, Injectable, } from '@angular/core';
import { UserMock } from 'src/shared/mocks/user.mock';

@Injectable()
export class LoginService {
  login: EventEmitter<any> = new EventEmitter();

  doLogin(username: string, password: string): void {
    localStorage.setItem('currentUser', JSON.stringify(UserMock.userMock1));
    this.login.emit(true);
  }

  doLogoff(): void {
    localStorage.removeItem('currentUser');
    this.login.emit(false);
  }

  isLogged(): boolean {
    return localStorage.getItem('currentUser') != null;
  }

  signUp(username: string, name: string, password: string, avatar: string) {
    return true;
  }

  get loggedUser() {
    return JSON.parse(localStorage.getItem('currentUser') || "") as ExtendedUser;
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
