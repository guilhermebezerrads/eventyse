import { Person } from "./person.model";

export class PostComment {
  author: Person = new Person();
  comment: string = "";
  createDate: Date = new Date();
}
