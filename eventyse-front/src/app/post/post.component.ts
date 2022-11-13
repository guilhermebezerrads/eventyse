import { Component, OnInit, OnDestroy, Input, AfterViewChecked, ChangeDetectorRef } from '@angular/core';
import { Post } from 'src/models/post.model';
import * as L from 'leaflet';
import { PostService } from 'src/services/post.service';
import { FormControl } from '@angular/forms';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent implements OnInit, OnDestroy, AfterViewChecked {

  @Input() post = new Post();

  isLiked: boolean = false;
  isDisliked: boolean = false;
  isFavorite: boolean = false;

  commentControl = new FormControl("");

  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(
    private postService: PostService,
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
      this.postService.favoritePost(this.post.id, true);
    else
      this.postService.favoritePost(this.post.id, false);
  }

  setLiked() {
    this.isLiked = !this.isLiked;

    if (this.isLiked) {
      this.isDisliked = false;
      this.postService.likePost(this.post.id, true);
    } else
      this.postService.likePost(this.post.id, false);
  }

  setDisliked() {
    this.isDisliked = !this.isDisliked;

    if (this.isDisliked) {
      this.isLiked = false;
      this.postService.likePost(this.post.id, false);
    } else
      this.postService.likePost(this.post.id, true);
  }

  comment() {
    if (this.commentControl.value) {
      this.postService.addComment(this.commentControl.value, this.post.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        (createdPost) => {
          if (createdPost) {
            window.alert("Comentário adicionado.");
            this.post.comments.push(createdPost);
            this.commentControl.reset();
          }
        }
      );
    } else alert("Insira um comentário");
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

}
