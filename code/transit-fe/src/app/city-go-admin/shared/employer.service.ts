import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, Subject } from 'rxjs';

import { Employer } from '../shared/employer.model';


@Injectable({ providedIn: 'root' })
export class EmployerService {

  private employersUrl = 'http://127.0.0.1:5000/employers';
  private employers = new Subject<Employer[]>();
  employers$ = this.employers.asObservable();
  employerArray: Employer[] = [];

  constructor(
    private http: HttpClient) { }

  initEmployers() {
    this.getEmployers().subscribe(result => {this.employers.next(result); this.employerArray = result});

    this.employers$ = this.employers.asObservable();
  }

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };


  getEmployers (): Observable<Employer[]> {
    return this.http.get<Employer[]>(this.employersUrl)
  }

  getEmployer(id: number): Observable<Employer> {
    const url = `${this.employersUrl}/${id}`;
    return this.http.get<Employer>(url)
  }

  addEmployer (employer: Employer) {
    return this.http.post<Employer>(this.employersUrl, employer, this.httpOptions).subscribe(newEmployer => {this.employerArray.push(newEmployer); this.employers.next(this.employerArray);})
  }

  deleteEmployer (employer: Employer | number): Observable<Employer> {
    const id = typeof employer === 'number' ? employer : employer.id;
    const url = `${this.employersUrl}/${id}`;

    return this.http.delete<Employer>(url, this.httpOptions)
  }

  updateEmployer (employer: Employer): Observable<any> {
    const id = typeof employer === 'number' ? employer : employer.id;
    const url = `${this.employersUrl}/${id}`;
    return this.http.put(url, employer, this.httpOptions)
  }
}