import { Component, OnInit, Input, AfterViewChecked, ChangeDetectorRef } from '@angular/core';
import { Post } from 'src/models/post.model';
import * as L from 'leaflet';
import { PostService } from 'src/services/post.service';
import { FormControl } from '@angular/forms';
import { LoginService } from 'src/services/login.service';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent implements OnInit, AfterViewChecked {

  @Input() post = new Post();

  isLiked: boolean = false;
  isDisliked: boolean = false;
  isFavorite: boolean = false;

  commentControl = new FormControl("");

  constructor(
    private postService: PostService,
    private loginService: LoginService,
    private changeDetector : ChangeDetectorRef) { }

  ngOnInit(): void {
  }

  ngAfterViewChecked(){ this.changeDetector.detectChanges(); }

  getPostMarkers(): Array<L.Marker> {
      let markers = new Array<L.Marker>();

      this.post.map.coordinates.forEach(coord => {
        markers.push(new L.Marker(new L.LatLng(coord[0], coord[1])))
      });

      return markers;
  }

  setFavorite() {
    this.isFavorite = !this.isFavorite;

    if (this.isFavorite)
      this.postService.favoritePost(this.post.id, this.loginService.loggedUser.id, true);
    else
      this.postService.favoritePost(this.post.id, this.loginService.loggedUser.id, false);
  }

  setLiked() {
    this.isLiked = !this.isLiked;

    if (this.isLiked) {
      this.isDisliked = false;
      this.postService.likePost(this.post.id, this.loginService.loggedUser.id, true);
    } else
      this.postService.likePost(this.post.id, this.loginService.loggedUser.id, false);
  }

  setDisliked() {
    this.isDisliked = !this.isDisliked;

    if (this.isDisliked) {
      this.isLiked = false;
      this.postService.likePost(this.post.id, this.loginService.loggedUser.id, false);
    } else
      this.postService.likePost(this.post.id, this.loginService.loggedUser.id, true);
  }

  comment() {
    if (this.commentControl.value) {
      this.postService.addComment(this.commentControl.value, this.post.id, this.loginService.loggedUser.id);
    } else alert("Insira um comentário");
  }

}
