import { Component, OnInit, Input } from '@angular/core';
import { PostMock } from 'src/shared/mocks/post.mock';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  @Input() userId: string = "";

  constructor() { }

  ngOnInit(): void {
  }

  mockPost1 = PostMock.mockPost1;
  mockPost2 = PostMock.mockPost2;

}
