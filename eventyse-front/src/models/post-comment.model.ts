import { ExtendedUser } from "./user.model";

export class PostComment {
  author: ExtendedUser = new ExtendedUser();
  comment: string = "";
  createDate: Date = new Date();
}
