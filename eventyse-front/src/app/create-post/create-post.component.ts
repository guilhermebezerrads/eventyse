import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup  } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginService } from 'src/services/login.service';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { MatChipInputEvent } from '@angular/material/chips';
import { Coordinate } from 'src/models/coordinate.model';

@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.scss']
})
export class CreatePostComponent implements OnInit {

  separatorKeysCodes: number[] = [ENTER, COMMA];

  createPostFromGroup = new FormGroup({
    name: new FormControl('', [Validators.required]),
    description: new FormControl('', [Validators.required]),
    tags: new FormControl([]),
    isPublic: new FormControl(''),
    coordinates: new FormControl([], [Validators.required])
  });

  constructor(private router: Router) {}

  ngOnInit(): void {
  }

  get tags() {
    return this.createPostFromGroup.get("tags")?.value
  }

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    // Add our fruit
    if (value) {
      this.createPostFromGroup.get("tags")?.setValue([...this.tags, value]);
      this.createPostFromGroup.get("tags")?.updateValueAndValidity();
    }

    // Clear the input value
    event.chipInput!.clear();
  }

  remove(tag: string): void {
    const index = this.tags.indexOf(tag);

    if (index >= 0) {
      this.createPostFromGroup.get("tags")?.setValue(
        this.tags.splice(index, 1));
      this.createPostFromGroup.get("tags")?.updateValueAndValidity();
    }
  }

  createPost() {
    let { name, description, tags, isPublic, coordinates } = this.createPostFromGroup.controls;
    this.router.navigate(['dashboard']);
  }

  setCoordinates(coordinates: Array<Coordinate>) {
    this.createPostFromGroup.get("coordinates")?.setValue(
      coordinates
    );
    this.createPostFromGroup.get("coordinates")?.updateValueAndValidity();
  }
}

