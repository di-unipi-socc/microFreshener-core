import { Component, OnInit, ViewChild, ElementRef, Input, Output, EventEmitter } from '@angular/core';
import * as go from 'gojs';


@Component({
  selector: 'app-diagram-editor',
  templateUrl: './diagram-editor.component.html',
  styleUrls: ['./diagram-editor.component.css']
})
export class DiagramEditorComponent implements OnInit {
  private diagram: go.Diagram = new go.Diagram();
  private palette: go.Palette = new go.Palette();

  private   $ = go.GraphObject.make;

  @ViewChild('diagramDiv')
  private diagramRef: ElementRef;

  @ViewChild('paletteDiv')
  private paletteRef: ElementRef;

  @Input()
  get model(): go.Model { return this.diagram.model; }
  set model(val: go.Model) { this.diagram.model = val; }

  @Output()
  nodeSelected = new EventEmitter<go.Node|null>();

  @Output()
  modelChanged = new EventEmitter<go.ChangedEvent>();

  constructor() { 
    this.initDiagram();
    this.initPalette();
  }

  ngOnInit() {
    this.diagram.div = this.diagramRef.nativeElement;
    this.palette.div = this.paletteRef.nativeElement;
  }

  initPalette(){
    // create the palette
    this.palette = new go.Palette();
    this.palette.nodeTemplateMap = this.diagram.nodeTemplateMap;

    // initialize contents of Palette
    this.palette.model.nodeDataArray =
      [
        { text: "Service", color: "lightblue", figure: "Circle"},
        { text: "Communication Pattern", color: "orange", figure:"Diamond" },
        { text: "DB", color: "lightgreen", figure:"Rectangle"},
      ];
  }
  
  initDiagram(){
    // Create the diagram of the graph
    const $ = go.GraphObject.make;
    this.diagram = new go.Diagram();
    // mostra la griglia
    this.diagram.grid =  $(go.Panel, "Grid",
      $(go.Shape, "LineH", { stroke: "lightgray", strokeWidth: 0.5 }),
      $(go.Shape, "LineH", { stroke: "gray", strokeWidth: 0.5, interval: 10 }),
      $(go.Shape, "LineV", { stroke: "lightgray", strokeWidth: 0.5 }),
      $(go.Shape, "LineV", { stroke: "gray", strokeWidth: 0.5, interval: 10 })
    ),
    this.diagram.initialContentAlignment = go.Spot.Center;
    this.diagram.allowDrop = true;  // necessary for dragging from Palette
    this.diagram.undoManager.isEnabled = true;

    this.diagram.addDiagramListener("ChangedSelection",
        e => {
          const node = e.diagram.selection.first();
          this.nodeSelected.emit(node instanceof go.Node ? node : null);
        });
    this.diagram.addModelChangedListener(e => e.isTransactionFinished && this.modelChanged.emit(e));

    this.diagram.nodeTemplate =
      $(go.Node, "Spot",
        new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
        // the main object is a Panel that surrounds a TextBlock with a Shape
        $(go.Panel, "Auto",
          { name: "PANEL" },
           $(go.Shape,  "Circle", // default figure
              { 
                fill: "white", strokeWidth: 0,
                portId: "", cursor: "pointer",
                // allow many kinds of links
                fromLinkable: true, toLinkable: true,
                fromLinkableSelfNode: false, toLinkableSelfNode: false,
                fromLinkableDuplicates: true, toLinkableDuplicates: true
              },
              new go.Binding("fill", "color"),
              new go.Binding("figure")),
            $(go.TextBlock,
              { margin: 8, editable: true, wrap: go.TextBlock.WrapFit },
              new go.Binding("text").makeTwoWay())
          ),
      // four small named ports, one on each side:
      this.makePort("T", go.Spot.Top, false, true),
      this.makePort("L", go.Spot.Left, true, true),
      this.makePort("R", go.Spot.Right, true, true),
      this.makePort("B", go.Spot.Bottom, true, false),
   );

    this.diagram.linkTemplate =
      $(go.Link,
        // allow relinking
        { relinkableFrom: true, relinkableTo: true },
        $(go.Shape),
        $(go.Shape, { toArrow: "OpenTriangle" })
      );


  }

  // Define a function for creating a "port" that is normally transparent.
  // The "name" is used as the GraphObject.portId, the "spot" is used to control how links connect
  // and where the port is positioned on the node, and the boolean "output" and "input" arguments
  // control whether the user can draw links from or to the port.
  makePort(name, spot, output, input) {
      var $ = go.GraphObject.make;
      // the port is basically just a small transparent square
      return $(go.Shape, "Circle",
               {
                  fill: null,  // not seen, by default; set to a translucent gray by showSmallPorts, defined below
                  stroke: null,
                  desiredSize: new go.Size(7, 7),
                  alignment: spot,  // align the port on the main Shape
                  alignmentFocus: spot,  // just inside the Shape
                  portId: name,  // declare this object to be a "port"
                  fromSpot: spot, toSpot: spot,  // declare where links may connect at this port
                  fromLinkable: output, toLinkable: input,  // declare whether the user may draw links to/from here
                  cursor: "pointer"  // show a different cursor to indicate potential link point
               });
    }

    init(){

    }

}
