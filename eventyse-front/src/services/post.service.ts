import { Observable, of } from "rxjs";
import { Coordinate } from "src/models/coordinate.model";
import { Post } from "src/models/post.model";
import { PostMock } from "src/shared/mocks/post.mock";
import { Injectable } from '@angular/core';
import { LoginService } from "./login.service";
import { PostComment } from "src/models/post-comment.model";

@Injectable()
export class PostService {

  constructor(private loginService: LoginService) { }

  getPosts(): Observable<Array<Post>> {
    return of([PostMock.mockPost1, PostMock.mockPost2]);
  }

  getPostsByUser(userId: string): Observable<Array<Post>> {
    return of([PostMock.mockPost1, PostMock.mockPost2]);
  }

  getPostsByTag(tag: string): Observable<Array<Post>> {
    return of([PostMock.mockPost1, PostMock.mockPost2]);
  }

  createPost(name: string, description: string, tags: string, isPublic: boolean, coordiantes: Array<Coordinate>): Observable<boolean> {
    let userId = this.loginService.loggedUser?.id;

    return of(true);
  }

  addComment(comment: string, postId: string): Observable<PostComment> {
    let user = this.loginService.loggedUser;

    console.log(comment, postId);
    return of({author: user, comment: comment, createDate: new Date()});
  }

  likePost(postId: string, liked: boolean) {
    let userId = this.loginService.loggedUser?.id;

    console.log(postId);
    return true;
  }

  favoritePost(postId: string, favorite: boolean) {
    let userId = this.loginService.loggedUser?.id;

    console.log(postId);
    return true;
  }
}
