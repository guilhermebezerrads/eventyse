import { ExtendedUser, User } from "src/models/user.model";

export class UserMock {
  static userMock1: ExtendedUser = {
    id: '1',
    name: 'Palmirinha',
    avatar: 'assets/palmirinha.png',
    username: 'palmirinha@email.com',
    followers: 123, following: 243, postsCount: 1234
  }
}
