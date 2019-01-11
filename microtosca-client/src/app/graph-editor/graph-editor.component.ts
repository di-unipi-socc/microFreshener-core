import { Component, OnInit, ViewChild, ElementRef, Input} from '@angular/core';
import { D3Service, ForceDirectedGraph, Node, Link, Service, Database } from '../d3';

@Component({
  selector: 'app-graph-editor',
  templateUrl: './graph-editor.component.html',
  styleUrls: ['./graph-editor.component.css']
})

export class GraphEditorComponent implements OnInit {
  // @Input('nodes') nodes;
  // @Input('links') links;
  // 
 
  // @ViewChild('directedGraph') directedGraph: ElementRef;

  graph: ForceDirectedGraph;
  private _options: { width, height } = { width: 800, height: 600 };

  constructor(private d3Service: D3Service) { }

  ngOnInit() {
      /** Receiving an initialized simulated graph from our custom d3 service */
      // this.graph = this.d3Service.getForceDirectedGraph(this.nodes, this.links, this.options);
      // var nodes: Node[] = [];
      // var links: Link[] = [];
      // var s = new Database(1);
      // s.x = 50;
      // s.y = 50;
  
      // links.push(new Link(nodes[0], nodes[1]));
      // this.graph = new ForceDirectedGraph([s], [], { width:200, height:200 });
      // console.log(s.x);
      // this.graph.addNode(s);

      this.graph  = this.d3Service.getGraph();
      // this.d3Service.addNode(new Service(1));
      // this.d3Service.addNode(new Database(1));
  }

  get options() {
    return this._options = {
      width: window.innerWidth,
      height: window.innerHeight
    };
  }

}
