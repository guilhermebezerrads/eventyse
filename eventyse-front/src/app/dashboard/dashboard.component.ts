import { Component, OnInit } from '@angular/core';
import { Post } from 'src/models/post.model';
import { PostMock } from 'src/shared/mocks/post.mock';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  mockPost1 = PostMock.mockPost1;
  mockPost2 = PostMock.mockPost2;

}
