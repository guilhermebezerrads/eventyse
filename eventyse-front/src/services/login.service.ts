import { ExtendedUser, User } from '../models/user.model';
import { EventEmitter, Injectable, } from '@angular/core';
import { UserMock } from 'src/shared/mocks/user.mock';
import { HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BaseService } from './base.service';

@Injectable()
export class LoginService {

  constructor(private baseService: BaseService) { }

  login: EventEmitter<any> = new EventEmitter();

  doLogin(username: string, password: string): Observable<any>  {
    return this.baseService.http.post<User>('http://localhost:5000/api/login', {
      username: username,
      password: password,
    });
  }

  doLogoff(): void {
    localStorage.removeItem('currentUser');
    localStorage.removeItem('token');
    this.login.emit(false);
  }

  isLogged(): boolean {
    return localStorage.getItem('currentUser') != null;
  }

  signUp(username: string, name: string, password: string, avatar: string): Observable<any> {
    return this.baseService.http.post<any>('http://localhost:5000/api/register', {
      username: username,
      name: name,
      password: password,
      avatar: avatar
    });
  }

  setToken(username: string, token: string) {
    localStorage.setItem('currentUser', username);
    localStorage.setItem('token', token);
    this.login.emit(true);
  }

  get loggedUser() {
    let user = new ExtendedUser("");
    let current = localStorage.getItem('currentUser') || "{}";

    user.username = current;
    user.avatar = 'assets/palmirinha.png';

    return user;
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
