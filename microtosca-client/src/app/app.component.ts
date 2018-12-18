import { Component, ViewChild, ElementRef } from '@angular/core';
import { Node, Service, Database, CommunicationPattern, Link } from './d3';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Ciao microtosca-client';
  nodes: Node[] = [];
  links: Link[] = [];

  constructor() {
    const N = 9,
    getIndex = number => number - 1;

    /** constructing the nodes array */
    // for (let i = 1; i <= N; i++) {
    //   this.nodes.push(new Node(i,'communicationpattern'));
    // }
    this.nodes.push(new Service(0));
    this.nodes.push(new Service(0));

    this.nodes.push(new Database(0));
    this.nodes.push(new Database(0));

    this.nodes.push(new CommunicationPattern(0));
    this.nodes.push(new CommunicationPattern(0));


    // for (let i = 1; i <= N; i++) {
    //   for (let m = 2; i * m <= N; m++) {
    //     /** increasing connections toll on connecting nodes */
    //     this.nodes[getIndex(i)].linkCount++;
    //     this.nodes[getIndex(i * m)].linkCount++;

    //     /** connecting the nodes before starting the simulation */
    //     this.links.push(new Link(i, i * m));
    //   }
    // }
  }
}
