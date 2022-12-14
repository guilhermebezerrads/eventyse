import { AfterViewInit, Component, Input, Output, OnInit, EventEmitter } from '@angular/core';
import * as L from 'leaflet';
import { Coordinate } from 'src/models/coordinate.model';
import { LocationService } from 'src/services/location.service';
import { v4 as uuidv4 } from 'uuid';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit, AfterViewInit {

  private map : any;

  @Input() markers = new Array<L.Marker>();

  @Input() readonly = false;

  @Output() outCoordinates = new EventEmitter<Array<Coordinate>>();

  readonly mapid = uuidv4().toString();

  private readonly MARKER_ICON = L.icon({
    iconUrl: 'assets/location-pin.png',
    iconSize:     [38, 38], // size of the icon
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
  });

  constructor(private locationService: LocationService) { }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    this.locationService.getPosition().then(pos=>
    {
      this.initMap(pos.lng, pos.lat);
    });

  }

  initMap(lng: any, lat: any) {
    this.map = L.map(this.mapid).setView([lat, lng], 13);

    this.map.doubleClickZoom.disable();

    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);

    this.map.on('dblclick', this.mapOnDoubleClick, this);

    if (this.markers.length) {
      this.initMarkers();
      (this.map as L.Map).fitBounds(L.featureGroup(this.markers).getBounds());
    }
  }

  initMarkers() {
    this.markers.forEach(
      marker => this.addMarker(marker.getLatLng())
    );
  }

  mapOnDoubleClick(e: L.LeafletMouseEvent) {
    if (!this.readonly)
      this.addMarker(e.latlng);
  }

  markerOnDoubleClick(e: L.LeafletMouseEvent) {
    if (!this.readonly)
      this.removeMarker(e.sourceTarget);
  }

  removeMarker(e: L.Marker) {
    this.map.removeLayer(e);

    this.markers = this.markers.filter(f => !f.getLatLng().equals(e.getLatLng()));

    this.outCoordinates.emit(this.markers.map(
      (marker) => { return {x: marker.getLatLng().lat, y: marker.getLatLng().lng} }
    ));
  }

  addMarker(latlang: L.LatLng) {
    this.markers.push(L.marker(latlang,
      {
        icon: this.MARKER_ICON
      }).on('dblclick', this.markerOnDoubleClick, this)
      .addTo(this.map));

    this.outCoordinates.emit(this.markers.map(
      (marker) => { return {x: marker.getLatLng().lat, y: marker.getLatLng().lng} }
    ));
  }
}
