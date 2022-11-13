import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ExtendedUser } from 'src/models/user.model';
import { PostMock } from 'src/shared/mocks/post.mock';
import { Subject} from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { UserService } from 'src/services/user.service';
import { PostService } from 'src/services/post.service';
import { Post } from 'src/models/post.model';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit, OnDestroy {

  user: ExtendedUser = new ExtendedUser();

  userPosts = new Array<Post>();

  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(
    private userService: UserService,
    private postService: PostService,
    private route: ActivatedRoute) { }

  private userSubscriber: any;

  ngOnInit(): void {
    this.userSubscriber = this.route.params.subscribe(params => {
      let userId = params['id'];

      this.userService.getUser(userId)
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        (user) => {
          this.user = user;

          this.postService.getPostsByUser(this.user.id)
          .pipe(takeUntil(this.destroy$))
          .subscribe(
            (posts) => {
              this.userPosts = posts;
            }
          );
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

}
