import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ExtendedUser, User } from 'src/models/user.model';
import { PostMock } from 'src/shared/mocks/post.mock';
import { Observable, Subject} from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { takeUntil } from 'rxjs/operators';
import { UserService } from 'src/services/user.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  @Input() userId: string = "";

  user:ExtendedUser = new ExtendedUser();

  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(private userService: UserService, private route: ActivatedRoute) { }

  private userSubscriber: any;

  ngOnInit(): void {
    this.userSubscriber = this.route.params.subscribe(params => {
      this.userId = params['id'];

      this.userService.getUser(this.userId)
      .pipe(takeUntil(this.destroy$))
      .subscribe(
        user => this.user = user
      );
   });
  }

  mockPost1 = PostMock.mockPost1;
  mockPost2 = PostMock.mockPost2;

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

  hasUser(): boolean {
    return this.user.id != "";
  }

}
