import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MapTestComponent } from './map-test/map-test.component';
import { MapComponent } from './map/map.component';

const routes: Routes = [
  { path: 'map', component: MapTestComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
