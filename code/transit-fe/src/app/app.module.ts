import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CityGoAdminComponent } from './city-go-admin/city-go-admin.component';
import { AdminTopBarComponent } from './admin-top-bar/admin-top-bar.component';

@NgModule({
  declarations: [
    AppComponent,
    CityGoAdminComponent,
    AdminTopBarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
