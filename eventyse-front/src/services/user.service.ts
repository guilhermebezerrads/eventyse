import { UserMock } from "src/shared/mocks/user.mock";
import { Observable, of } from 'rxjs';
import { ExtendedUser } from "src/models/user.model";
import { Injectable } from '@angular/core';
import { LoginService } from "./login.service";
import { BaseService } from "./base.service";

@Injectable()
export class UserService {

  constructor(private baseService: BaseService, private loginService: LoginService) { }

  static loggedUserFollowers = new Array<ExtendedUser>();

  getUser(username: string): Observable<any> {
    return this.baseService.http.get<any>('http://localhost:5000/api/users/' + username, this.baseService.Options);
  }

  getUsers(): Observable<any> {
    return this.baseService.http.get<any>('http://localhost:5000/api/users', this.baseService.Options);
  }

  getFollowers(userId: string): Observable<Array<ExtendedUser>> {
    UserService.loggedUserFollowers = [UserMock.userMock1];
    return of([UserMock.userMock1]);
  }

  checkFollow(username: string): Observable<any> {
    return this.baseService.http.get<any>('http://localhost:5000/api/users/follow/' + username, this.baseService.Options);
  }

  followUser(username: string): Observable<any> {
    return this.baseService.http.put<any>('http://localhost:5000/api/users/follow/' + username, {}, this.baseService.Options);
  }

  unfollowUser(username: string): Observable<any> {
    return this.baseService.http.put<any>('http://localhost:5000/api/users/unfollow/' + username, {}, this.baseService.Options);
  }
}
