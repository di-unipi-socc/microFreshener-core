import { Component, OnInit, Input} from '@angular/core';
import { D3Service, ForceDirectedGraph, Node } from '../d3';

@Component({
  selector: 'app-graph-editor',
  templateUrl: './graph-editor.component.html',
  styleUrls: ['./graph-editor.component.css']
})
export class GraphEditorComponent implements OnInit {
  @Input('nodes') nodes;
  @Input('links') links;

  graph: ForceDirectedGraph;
  private _options: { width, height } = { width: 800, height: 600 };

  constructor(private d3Service: D3Service) { }

  ngOnInit() {
      /** Receiving an initialized simulated graph from our custom d3 service */
      this.graph = this.d3Service.getForceDirectedGraph(this.nodes, this.links, this.options);
      console.log(this.graph);
  }

  ngAfterViewInit() {
    console.log("initialized simulation");
     this.graph.initSimulation(this.options);
  }

  get options() {
    return this._options = {
      width: window.innerWidth,
      height: window.innerHeight
    };
  }

}
