import { UserMock } from "src/shared/mocks/user.mock";
import { Observable, of } from 'rxjs';
import { ExtendedUser, User } from "src/models/user.model";

export class UserService {

  getUser(userId: string): Observable<ExtendedUser> {
    return of(UserMock.userMock1);
  }
}
