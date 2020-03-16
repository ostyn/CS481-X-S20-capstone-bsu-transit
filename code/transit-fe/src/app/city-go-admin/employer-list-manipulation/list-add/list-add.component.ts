import { Component, Output } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ListAddDialogComponent } from './list-add-dialog/list-add-dialog.component';
import { Employer } from '../../shared/employer.model';

import { EmployerService } from '../../shared/employer.service';
import { EventEmitter } from 'protractor';

@Component({
  selector: 'admin-list-add',
  templateUrl: './list-add.component.html',
  styleUrls: ['./list-add.component.css']
})
export class ListAddComponent {
  
  employer: Employer = { id: null, name: null, maxEmployees: null, description: null};

  constructor(public dialog: MatDialog,private employerService: EmployerService) {}

  ngOnInit(): void {
    
  }
  
  openDialog(): void {
    const dialogRef = this.dialog.open(ListAddDialogComponent, {
      width: '250px',
      data: this.employer
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      result=this.employer;
      this.employerService.addEmployer(result);
      result = null;
      this.employer = { id: null, name: null, maxEmployees: null, description: null};
    });
  }

}
