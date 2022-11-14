import { Observable, of } from "rxjs";
import { Coordinate } from "src/models/coordinate.model";
import { Post } from "src/models/post.model";
import { PostMock } from "src/shared/mocks/post.mock";
import { Injectable } from '@angular/core';
import { LoginService } from "./login.service";
import { PostComment } from "src/models/post-comment.model";
import { ExtendedUser } from "src/models/user.model";
import { BaseService } from "./base.service";

@Injectable()
export class PostService {

  constructor(
    private loginService: LoginService,
    private baseService: BaseService) { }

  getPosts(): Observable<Array<any>> {
    return this.baseService.http.get<any>('http://localhost:5000/api/roadmaps', this.baseService.Options);
  }

  getPostsByUser(username: string): Observable<any> {
    return this.baseService.http.get<any>('http://localhost:5000/api/roadmaps/user/' + username, this.baseService.Options);
  }

  getPostsByTag(tag: string): Observable<any> {
    return this.baseService.http.get<any>('http://localhost:5000/api/roadmaps/tag/' + tag, this.baseService.Options);
  }

  getPostsByFollowing(): Observable<any> {
    return this.baseService.http.get<any>('http://localhost:5000/api/roadmaps/following', this.baseService.Options);
  }

  createPost(name: string, description: string, tags: Array<string>, isPublic: boolean, coordinates: Array<Array<number>>): Observable<any> {
    let username = this.loginService.loggedUser.username;

    return this.baseService.http.post<any>('http://localhost:5000/api/roadmaps', {
      username: username,
      title: name,
      description: description,
      tags: tags,
      coordinates: coordinates
    }, this.baseService.Options);
  }

  addComment(comment: string, postId: string): Observable<any> {
    return this.baseService.http.post<any>('http://localhost:5000/api/comments/' + postId, {
      text: comment
    }, this.baseService.Options);
  }

  removeComment(commentId: string): Observable<any> {
    return this.baseService.http.delete<any>('http://localhost:5000/api/comments/' + commentId, this.baseService.Options);
  }

  getComments(postId: string): Observable<Array<any>> {
    return this.baseService.http.get<any>('http://localhost:5000/api/comments/' + postId, this.baseService.Options);
  }

  likePost(postId: string, liked: boolean): Observable<any> {
    if(liked)
      return this.baseService.http.put<any>('http://localhost:5000/api/roadmaps/like/' + postId, {}, this.baseService.Options);
    else
      return this.baseService.http.delete<any>('http://localhost:5000/api/roadmaps/like/' + postId, this.baseService.Options);
  }

  dislikePost(postId: string, dislikePost: boolean): Observable<any> {
    if(dislikePost)
      return this.baseService.http.put<any>('http://localhost:5000/api/roadmaps/dislike/' + postId, {}, this.baseService.Options);
    else
      return this.baseService.http.delete<any>('http://localhost:5000/api/roadmaps/dislike/' + postId, this.baseService.Options);
  }

  favoritePost(postId: string, favorite: boolean) {
    let username = this.loginService.loggedUser;

    console.log(postId);
    return true;
  }

  checkLikedPost(postId: string) {
    return this.baseService.http.get<any>('http://localhost:5000/api/roadmaps/like/' + postId, this.baseService.Options);
  }

  checkDislikedPost(postId: string) {
    return this.baseService.http.get<any>('http://localhost:5000/api/roadmaps/dislike/' + postId, this.baseService.Options);
  }
}
