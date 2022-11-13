import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormControl, Validators, FormGroup  } from '@angular/forms';
import { Router } from '@angular/router';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { MatChipInputEvent } from '@angular/material/chips';
import { Coordinate } from 'src/models/coordinate.model';
import { PostService } from 'src/services/post.service';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.scss']
})
export class CreatePostComponent implements OnInit, OnDestroy {

  separatorKeysCodes: number[] = [ENTER, COMMA];

  createPostFromGroup = new FormGroup({
    name: new FormControl('', [Validators.required]),
    description: new FormControl('', [Validators.required]),
    tags: new FormControl([]),
    isPublic: new FormControl(''),
    coordinates: new FormControl([], [Validators.required])
  });

  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(private postService: PostService, private router: Router) {}

  ngOnInit(): void {
  }

  get tags() {
    return this.createPostFromGroup.get("tags")?.value
  }

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    if (value) {
      this.createPostFromGroup.get("tags")?.setValue([...this.tags, value]);
      this.createPostFromGroup.get("tags")?.updateValueAndValidity();
    }

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

    this.postService.createPost(name.value, description.value, tags.value, isPublic.value, coordinates.value)
    .pipe(takeUntil(this.destroy$))
    .subscribe(
      (isCreated) => {
        if (isCreated) {
          window.alert("Postagem criada com sucesso!");
          this.router.navigate(['/dashboard']);
        }
      }
    );
  }

  setCoordinates(coordinates: Array<Coordinate>) {
    this.createPostFromGroup.get("coordinates")?.setValue(
      coordinates
    );
    this.createPostFromGroup.get("coordinates")?.updateValueAndValidity();
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }
}

