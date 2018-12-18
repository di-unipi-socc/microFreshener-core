import   {Node} from "./node";

// Implementing SimulationNodeDatum interface into our custom Node class
export class Database extends Node {
    // Optional - defining optional implementation properties - required for relevant typing assistance
   
    constructor(id: number) { 
        super(id, "database"); 
    }
}