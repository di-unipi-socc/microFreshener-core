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
    const N = 3;
    // getIndex = number => number - 1;

    /** constructing the nodes array */
    // for (let i = 1; i <= N; i++) {
    // for (let i = 0; i < N; i++) {
    //   this.nodes.push(new Service(i));
    //   console.log("Added service");
    // }
    this.nodes.push(new Service(1));
    this.nodes.push(new Service(1));

    this.nodes.push(new Database(1));
    this.nodes.push(new Database(2));

    this.nodes.push(new CommunicationPattern(0));
    this.nodes.push(new CommunicationPattern(0));
    console.log(this.nodes.length)

    // this.links.push(new Link(this.nodes[0], this.nodes[1]));
    // this.links.push(new Link(1, 2));
    // this.links.push(new Link(2, 3));
    // this.links.push(new Link(3, 3));
    // this.links.push(new Link(4, 1));
    // this.links.push(new Link(5, 3));
    // this.links.push(new Link(6, 3));
    // this.links.push(new Link(7, 4));
    // this.links.push(new Link(8, 6));
    // this.links.push(new Link(9, 7));
    // this.links.push(new Link(i, i * m));

    // for (let i = 0; i < N; i++) {
    //   for (let m = 1; i * m < N; m++) {
    //     /** increasing connections toll on connecting nodes */
    //     // this.nodes[getIndex(i)].linkCount++;
    //     // this.nodes[getIndex(i * m)].linkCount++;
    //     this.nodes[i].linkCount++;
    //     this.nodes[i * m].linkCount++;

    //     /** connecting the nodes before starting the simulation */
    //     this.links.push(new Link(i, i * m));
    //     console.log("Added link");
    //   }
    // }
  }
}
