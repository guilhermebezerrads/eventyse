import { Map } from "./map.model";
import { PostComment } from "./post-comment.model";
import { ExtendedUser } from "./user.model";

export class Post {
  id: string = "";
  author: ExtendedUser = new ExtendedUser();
  title: string = "";
  description: string = "";
  creationDate: Date = new Date();
  map: Map = new Map();
  tags: Array<string> = [];
  countLike: number = 0;
  countDislike: number = 0;
  comments: Array<PostComment> = []
}
