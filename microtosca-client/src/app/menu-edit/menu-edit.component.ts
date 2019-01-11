import { Component, OnInit } from '@angular/core';
import { Node, Database, Service,ForceDirectedGraph, D3Service, CommunicationPattern} from '../d3';


@Component({
  selector: 'app-menu-edit',
  templateUrl: './menu-edit.component.html',
  styleUrls: ['./menu-edit.component.css']
})
export class MenuEditComponent implements OnInit {
  service: Node;
  database: Node;
  communicationPattern: Node;

  graph:ForceDirectedGraph = null;
  
  constructor(private d3Service: D3Service) { 
    this.graph = d3Service.getGraph();
  }

  ngOnInit() {
     this.service = new Service(0);
     this.database = new Database(1);
     this.communicationPattern = new CommunicationPattern(0);
  }

  onClickMe(){
    console.log("Cliccked");
    this.d3Service.addNode(new Database(2));
  }


}
