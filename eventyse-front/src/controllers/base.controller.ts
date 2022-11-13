import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class BaseController {
  constructor(protected http: HttpClient) { }
}
