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
    this.postService.getComments(this.post.id)
    .pipe(takeUntil(this.destroy$))
    .subscribe(
      (comments) => {
        this.post.comments = comments.map(
          (c) => {
            return {
              comment: c.text,
              createDate: c.createdDate,
              author: c.authorUsername
            }
          }
        )
      }
    )

    this.postService.checkLikedPost(this.post.id)
    .pipe(takeUntil(this.destroy$))
    .subscribe(
      (likedStatus) => {
        if (likedStatus.isLiked) {
          this.isLiked = true;
        } else {
          this.postService.checkDislikedPost(this.post.id)
          .pipe(takeUntil(this.destroy$))
          .subscribe(
            (likedStatus) => {
              if (likedStatus.isDisliked) {
                this.isDisliked = true;
              }
            }
          )
        }
      }
    )

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

    if (!this.isLiked) {
      this.postService.likePost(this.post.id, true)
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        (result) => {
          this.post.countLike += 1;
          if (this.isDisliked) {
            this.isDisliked = false;
            this.post.countDislike -= 1;
          }
        }
      );
    } else
      this.postService.likePost(this.post.id, false)
      .pipe(takeUntil(this.destroy$))
      .subscribe((result) => {
        this.post.countLike -= 1;
      });

    this.isLiked = !this.isLiked;
  }

  setDisliked() {
    if (!this.isDisliked) {
      this.postService.dislikePost(this.post.id, true)
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        (result) => {
          this.post.countDislike += 1;
          if (this.isLiked) {
            this.isLiked = false;
            this.post.countLike -= 1;
          }
        }
      );
    } else
      this.postService.dislikePost(this.post.id, false)
      .pipe(takeUntil(this.destroy$))
      .subscribe((result) => {
        this.post.countDislike -= 1;
      });

    this.isDisliked = !this.isDisliked;
  }

  comment() {
    if (this.commentControl.value) {
      this.postService.addComment(this.commentControl.value, this.post.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        (c) => {
          if (c) {
            window.alert("Comentário adicionado.");
            this.post.comments.push({
              comment: c.text,
              createDate: c.createdDate,
              author: c.authorUsername
            });
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
