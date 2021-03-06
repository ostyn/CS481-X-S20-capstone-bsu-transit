import { Component, Output } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ListAddDialogComponent } from './list-add-dialog/list-add-dialog.component';
import { Employer } from '../../shared/employer.model';
import { EmployerService } from '../../shared/employer.service';

@Component({
  selector: 'admin-list-add',
  templateUrl: './list-add.component.html',
  styleUrls: ['./list-add.component.css']
})
export class ListAddComponent {

  employers: Employer[] = [];
  employer: Employer = { id: null, name: null, rider_cap: null, email: null };

  constructor(public dialog: MatDialog, private employerService: EmployerService) {
    this.employerService.employers$.subscribe(addEmployers => this.employers = addEmployers);
  }

  ngOnInit(): void {

  }

  openDialog(): void {
    const dialogRef = this.dialog.open(ListAddDialogComponent, {
      width: '250px',
      data: this.employer
    });

    dialogRef.afterClosed().subscribe(result => {
      this.employerService.addEmployer(this.employer);
      result = null;
      this.employer = { id: null, name: null, rider_cap: null, email: null };
    });
  }

}
