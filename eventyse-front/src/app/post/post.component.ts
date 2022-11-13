import { Component, OnInit, Input, AfterViewChecked, ChangeDetectorRef } from '@angular/core';
import { Post } from 'src/models/post.model';
import * as L from 'leaflet';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent implements OnInit, AfterViewChecked {

  @Input() post = new Post();

  isLiked: boolean = false;
  isDisliked: boolean = false;
  isFavorite: boolean = false;

  constructor(private changeDetector : ChangeDetectorRef) { }

  ngOnInit(): void {
  }

  ngAfterViewChecked(){ this.changeDetector.detectChanges(); }

  getPostMarkers(): Array<L.Marker> {
      let markers = new Array<L.Marker>();

      this.post.map.coordinates.forEach(coord => {
        markers.push(new L.Marker(new L.LatLng(coord[0], coord[1])))
      });

      return markers;
  }

  setFavorite() {
    this.isFavorite = !this.isFavorite;
  }

  setLiked() {
    this.isLiked = !this.isLiked;

    if (this.isLiked) this.isDisliked = false;
  }

  setDisliked() {
    this.isDisliked = !this.isDisliked;

    if (this.isDisliked) this.isLiked = false;
  }

}
