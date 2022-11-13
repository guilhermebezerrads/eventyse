import { Component, OnInit } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { Post } from 'src/models/post.model';
import { PostService } from 'src/services/post.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  posts = new Array<Post>();

  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(private postService: PostService) { }

  ngOnInit(): void {
    this.postService.getPosts()
    .pipe(takeUntil(this.destroy$))
    .subscribe(
      posts => this.posts = posts
    );
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

}
