import { Component, OnInit } from '@angular/core';
import { Node, Database, Service, CommunicationPattern} from '../d3';

@Component({
  selector: 'app-menu-edit',
  templateUrl: './menu-edit.component.html',
  styleUrls: ['./menu-edit.component.css']
})
export class MenuEditComponent implements OnInit {
  service: Node;
  database: Node;
  communicationPattern: Node;

  constructor() { }

  ngOnInit() {
     this.service = new Service(0);
     this.database = new Database(1);
     this.communicationPattern = new CommunicationPattern(0);
  }

}
