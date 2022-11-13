export class User {
  username: string = '';
  name: string = '';
  avatar: string = '';
}

export class ExtendedUser extends User {
  followers: number = 0;
  following: number = 0;
  postsCount: number = 0;
  id: string = '-1';

  constructor(username: string){
    super();
    this.username = username;
  }
}
