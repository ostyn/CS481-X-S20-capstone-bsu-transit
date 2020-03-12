import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CityGoAdminComponent } from './city-go-admin/city-go-admin.component';
import { AdminTopBarComponent } from './admin-top-bar/admin-top-bar.component';
import { EmployerComponent } from './employer/employer.component';
import { EmployerTopBarComponent } from './employer-top-bar/employer-top-bar.component';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { ProfileComponent } from './profile/profile.component';
import { AddEmployerComponent } from './add-employer/add-employer.component';
import { AddEmployeeComponent } from './add-employee/add-employee.component';

@NgModule({
  declarations: [
    AppComponent,
    CityGoAdminComponent,
    AdminTopBarComponent,
    EmployerComponent,
    EmployerTopBarComponent,
    NavBarComponent,
    ProfileComponent,
    AddEmployerComponent,
    AddEmployeeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
