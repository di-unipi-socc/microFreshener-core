import { Component, OnInit, ViewChild, ElementRef} from '@angular/core';
import { Node, Database, Service,ForceDirectedGraph, D3Service, CommunicationPattern} from '../d3';
import * as go from 'gojs';

@Component({
  selector: 'app-menu-edit',
  templateUrl: './menu-edit.component.html',
  styleUrls: ['./menu-edit.component.css']
})
export class MenuEditComponent implements OnInit {
  private palette: go.Palette = new go.Palette();

  @ViewChild('menuPalette')
  private paletteRef: ElementRef;

  constructor(private d3Service: D3Service) { 
  }

  ngOnInit() {
    //  this.service = new Service(0);
    //  this.database = new Database(1);
    //  this.communicationPattern = new CommunicationPattern(0);
   }

  onClickMe(){
    console.log("Cliccked");
    this.d3Service.addNode(new Database(2));
  }


}
