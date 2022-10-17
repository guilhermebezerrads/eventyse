import { Component, OnInit } from '@angular/core';
import * as L from 'leaflet';

@Component({
  selector: 'app-map-test',
  templateUrl: './map-test.component.html',
  styleUrls: ['./map-test.component.scss']
})
export class MapTestComponent implements OnInit {

  markers = new Array<L.Marker>();

  constructor() { }

  ngOnInit(): void {
    this.markers.push(
      new L.Marker([39.8282,  -98.5795])
    );

    this.markers.push(
      new L.Marker([36.2017372066406,  -94.00780498981477])
    );

    this.markers.push(
      new L.Marker([39.259485302277554,  -85.39452373981477])
    );

    this.markers.push(
      new L.Marker([42.966075955988025,  -101.56639873981477])
    );

    this.markers.push(
      new L.Marker([40.339850993496356,  -113.51952373981477])
    );
  }

}
