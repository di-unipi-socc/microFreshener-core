
// Implementing SimulationNodeDatum interface into our custom Node class
export class Node implements d3.SimulationNodeDatum {
    // Optional - defining optional implementation properties - required for relevant typing assistance
    index?: number;
    
    x?: number;
    y?: number;
    vx?: number;
    vy?: number;
    fx?: number | null;
    fy?: number | null;
    
    id: number;
    linkCount: number = 0;
    type: string; // service, database, communication pattern
    
    constructor(id:number, type:string) {
        this.id = id;
        this.type = type;
        this.x = 0;
        this.y =0;
    }

}

// Implementing SimulationNodeDatum interface into our custom Node class
export class Database extends Node {
    // Optional - defining optional implementation properties - required for relevant typing assistance
   
    constructor(id: number) { 
        super(id, "database"); 
    }
}

export class Service extends Node {
    // Optional - defining optional implementation properties - required for relevant typing assistance
   
    constructor(id: number) { 
        super(id, "service"); 
    }
}

export class CommunicationPattern extends Node {
    // Optional - defining optional implementation properties - required for relevant typing assistance
   
    constructor(id: number) { 
        super(id, "communicationpattern"); 
    }
}