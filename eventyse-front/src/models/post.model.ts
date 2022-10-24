import { Map } from "./map.model";
import { Person } from "./person.model";
import { PostComment } from "./post-comment.model";

export class Post {
  author: Person = new Person();
  title: string = "";
  description: string = "";
  creationDate: Date = new Date();
  map: Map = new Map();
  tags: Array<string> = [];
  countLike: number = 0;
  countDislike: number = 0;
  comments: Array<PostComment> = []
}
