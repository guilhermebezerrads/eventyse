import { ExtendedUser } from "./user.model";

export class PostComment {
  author: string = "";
  comment: string = "";
  createDate: Date = new Date();
  id: string = "";
}
