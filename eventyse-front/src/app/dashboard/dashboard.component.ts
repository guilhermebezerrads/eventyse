import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';
import { Map } from 'src/models/map.model';
import { Post } from 'src/models/post.model';
import { ExtendedUser } from 'src/models/user.model';
import { PostService } from 'src/services/post.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  posts = new Array<Post>();

  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(private postService: PostService, private route: ActivatedRoute, private router: Router) { }

  private filterSubscriber: any;

  isFilteringByTag: boolean = false;
  isFilteringByFollowers: boolean = false;

  ngOnInit(): void {
    this.filterSubscriber = this.route.params.subscribe(params => {
      let filterTag = params['filterTag'] || "";
      let filterFollow = params['followers'] || false;

      if (filterTag != "") {
        this.isFilteringByTag = true;
        this.postService.getPostsByTag(filterTag)
        .pipe(takeUntil(this.destroy$))
        .subscribe(
          (posts) => {
            this.posts = (posts.roadmaps as Array<any>).map(
              (p) => {
                return {
                  id: p.id,
                  title: p.title,
                  description: p.description,
                  creationDate: p.createdDate,
                  tags: p.tags,
                  countLike: p.likes,
                  countDislike: p.dislikes,
                  map: {
                    coordinates: p.coordinates
                  },
                  comments: [],
                  author: new ExtendedUser(p.authorUsername)
                }
              }
            )
          }
        );
      } else if (filterFollow) {
        this.isFilteringByFollowers = true;
        this.postService.getPostsByFollowing()
        .pipe(takeUntil(this.destroy$))
        .subscribe(
          (posts) => {
            this.posts = (posts.roadmaps as Array<any>).map(
              (p) => {
                return {
                  id: p.id,
                  title: p.title,
                  description: p.description,
                  creationDate: p.createdDate,
                  tags: p.tags,
                  countLike: p.likes,
                  countDislike: p.dislikes,
                  map: {
                    coordinates: p.coordinates
                  },
                  comments: [],
                  author: new ExtendedUser(p.authorUsername)
                }
              }
            )
          }
        );
      } else {
        this.isFilteringByTag = false;
        this.isFilteringByFollowers = false;

        this.postService.getPosts()
        .pipe(takeUntil(this.destroy$))
        .subscribe(
          (posts) => {
            this.posts = posts.map(
              (p) => {
                return {
                  id: p.id,
                  title: p.title,
                  description: p.description,
                  creationDate: p.createdDate,
                  tags: p.tags,
                  countLike: p.likes,
                  countDislike: p.dislikes,
                  map: {
                    coordinates: p.coordinates
                  },
                  comments: [],
                  author: new ExtendedUser(p.authorUsername)
                }
              }
            )
          }
        );
      }
    })
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

  redirectTo(uri: string, params = {}) {
    this.router.navigateByUrl('/', {skipLocationChange: true}).then(()=>
    this.router.navigate([uri, params]));
 }

}
