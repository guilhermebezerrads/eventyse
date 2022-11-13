import { HttpClient, HttpHeaders } from "@angular/common/http"
import { Injectable } from '@angular/core';

@Injectable()
export class BaseService {
  constructor(public http: HttpClient) {}

  get Options() {
    return {
      headers: new HttpHeaders({
        'Token': localStorage.getItem('token') || "",
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
        'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type, Origin, Authorization, Accept, Client-Security-Token, Accept-Encoding, X-Auth-Token, content-type'
      })
    };
  }
}
