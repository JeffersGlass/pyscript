options = {
    name: 'cose',
    idealEdgeLength: 20,
    nodeOverlap: 50,
    refresh: 20,
    fit: true,
    padding: 30,
    randomize: true,
    componentSpacing: 100,
    nodeRepulsion: 4000000,
    edgeElasticity: 100,
    nestingFactor: 5,
    gravity: 80,
    numIter: 1000,
    initialTemp: 200,
    coolingFactor: 0.95,
    minTemp: 1.0,
    animate: 'end',
    animationEasing: 'ease-in-out-quad'
  }

/* ele1 = {
    group: "nodes",
    data: {"id": "a", "weight": 75},
}

ele2 = {
    group: "nodes",
    data: {"id": "b", "weight": 75},
}

ele3 = {
    group: "nodes",
    data: {"id": "c", "weight": 75},
}

edge1 = {group: "edges", data: {source: "a", target: "b"}}
edge2 = {group: "edges", data: {source: "b", target: "c"}}
edge3 = {group: "edges", data: {source: "c", target: "a"}} */

//let data = [ele1, ele2, ele3, edge1, edge2, edge3]

let data = []
const minElements = 10
const spanElements = 10
numElements = Math.floor(Math.random() * spanElements + minElements)
console.log(numElements)
for (var i = 0; i < numElements; i++){
    const newNode = {
        group: "nodes",
        data: {"id": i, "weight": 75},
    }
    data.push(newNode)
}

console.log(data)

const minEdges = 20
const spanEdges = 20
const numEdges = Math.floor(Math.random() * spanEdges + minEdges)
let edgeShorthand = []

while (edgeShorthand.length < numEdges){
    const firstEl = Math.floor(Math.random() * numElements)
    let secondEl = firstEl
    while (secondEl == firstEl){
        secondEl = Math.floor(Math.random() * numElements)
    }
    if (edgeShorthand.indexOf([firstEl, secondEl]) === -1){
        edgeShorthand.push([firstEl, secondEl])
    }
}

console.log(edgeShorthand)

edgeShorthand.forEach((edge) =>{
    data.push({
        group: "edges",
        data:
        {
            source: edge[0],
            target: edge[1]
        }
    })
})

gridlayout = {
    name: 'grid'
}

cy = new cytoscape({
    container: document.getElementById("cnv"),
    layout: gridlayout,
    elements: data
})

cy.style('node { background-color: green; } edge {line-color: black; width: 3} ')

cy.layout(options)

function relay() {
    let l = cy.makeLayout(options)
    l.run()
    cy.add({

        group: "edges",
        data: {
            source: 2,
            target: 5
        }
    })
}
