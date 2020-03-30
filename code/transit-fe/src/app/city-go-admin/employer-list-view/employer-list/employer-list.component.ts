import { Component } from '@angular/core';
import { Employer } from '../../shared/employer.model';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { EmployerService } from '../../shared/employer.service';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'admin-employer-list',
  templateUrl: './employer-list.component.html',
  styleUrls: ['./employer-list.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class EmployerListComponent {

  employers = new MatTableDataSource<Employer>();
  displayedColumns: string[] = ["id", "name", "maxEmployees", "description"];
  columnsToDisplay: string[] = this.displayedColumns.slice();
  expandedEmployer: Employer | null;

  constructor(private employerService: EmployerService) { 
    this.employerService.employers$.subscribe(test => this.employers.data = test);
  }

  ngOnInit(): void {
  
  }

  

}