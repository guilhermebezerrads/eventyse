import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ExtendedUser } from 'src/models/user.model';
import { PostMock } from 'src/shared/mocks/post.mock';
import { Subject} from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { UserService } from 'src/services/user.service';
import { PostService } from 'src/services/post.service';
import { Post } from 'src/models/post.model';
import { LoginService } from 'src/services/login.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit, OnDestroy {

  user: ExtendedUser = new ExtendedUser("");

  userPosts = new Array<Post>();

  followStatus: boolean = false;

  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(
    private userService: UserService,
    private postService: PostService,
    private loginService: LoginService,
    private route: ActivatedRoute) { }

  private userSubscriber: any;

  ngOnInit(): void {
    this.userSubscriber = this.route.params.subscribe(params => {
      let userId = params['id'];

      this.userService.getUser(userId)
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        (user) => {
          this.user = {
            id: user.id,
            name: user.name,
            username: user.username,
            followers: user.followersCounter,
            following: user.followingCounter,
            avatar: "assets/palmirinha.png",
            postsCount: 0
          };

          this.postService.getPostsByUser(this.user.username)
          .pipe(takeUntil(this.destroy$))
          .subscribe(
            (posts) => {
              console.log(posts);
              this.userPosts = (posts.roadmaps as Array<any>).map(
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
              );
            }
          );

          if (this.isNotUser()) {
            this.userService.checkFollow(this.user.username)
            .pipe(takeUntil(this.destroy$))
            .subscribe(
              (followStatus) => this.followStatus = followStatus.isFollower
            )
          }
        }
      );
   });
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

  hasUser(): boolean {
    return this.user.id != "";
  }

  isNotUser(): boolean {
    return this.user.username != this.loginService.loggedUser.username;
  }

  followUser() {
    this.userService.followUser(this.user.username)
    .pipe(takeUntil(this.destroy$))
    .subscribe(
      (result) => {
        console.log(result);
        this.user.followers += 1;
        this.followStatus = true;
      }
    )
  }

  unfollowUser() {
    this.userService.unfollowUser(this.user.username)
    .pipe(takeUntil(this.destroy$))
    .subscribe(
      (result) => {
        console.log(result);
        this.user.followers -= 1;
        this.followStatus = false;
      }
    )
  }

}
