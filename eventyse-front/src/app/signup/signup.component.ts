import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup, ValidatorFn, AbstractControl, ValidationErrors } from '@angular/forms';
import { Router } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';
import { LoginService } from 'src/services/login.service';
import { UserService } from 'src/services/user.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {

  signupFromGroup = new FormGroup({
    avatar: new FormControl(''),
    email: new FormControl('', [Validators.required, Validators.email]),
    name: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required]),
  });

  get emailFormControl() {
    return this.signupFromGroup.get('email');
  }

  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(
    private loginService: LoginService,
    private userService: UserService,
    private router: Router) {}

  ngOnInit(): void {
  }

  signUp() {
    let { avatar, email, name, password } = this.signupFromGroup.controls;
    this.loginService.signUp(email.value, name.value, password.value, avatar.value)
    .pipe(takeUntil(this.destroy$))
    .subscribe(
      (result) => {
        this.loginService.setToken(result.username, result.token);

        this.userService.getUsers().pipe(takeUntil(this.destroy$)).subscribe(
          (result) => console.log(result)
        )

        this.router.navigate(['dashboard']);
      })
  }

  imageURL: string = "assets/avatar.png";

  showPreview(event: any) {
    const file = (event.target as HTMLInputElement).files?.item(0);
    // File Preview
    const reader = new FileReader();
    reader.onload = () => {
      this.imageURL = reader.result as string;
    }
    reader.readAsDataURL(file as Blob)
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

}
