import { User } from "src/models/user.model";
import { BaseController } from "./base.controller";
import { Observable } from "rxjs";

export class AccountController extends BaseController {

  registerUser(username: string, name: string, password: string, avatar: string): Observable<User> {
    return this.http.post<User>('http://localhost:5000/api/register', {
      username: username,
      name: name,
      password: password,
      avatar: avatar
    });
  }

}
