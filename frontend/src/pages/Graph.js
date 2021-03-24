import React from 'react'
import {
    Sigma, 
    RelativeSize, 
    RandomizeNodePositions,
    EdgeShapes,
    ForceAtlas2,
} from 'react-sigma';

const graph = require('../graphData.json')

const Graph = () => {
    const sigmaSettings = {
        drawEdges: true,
        drawLabels: true,
        minEdgeSize: 0.5,
        maxEdgeSize: 8,
        minNodeSize: 5,
        maxNodeSize: 20,
        clone: false,
        defaultNodeType: "def",
        defaultEdgeType: "def",
        defaultLabelColor: "#000",
        defaultEdgeColor: "#cfd2d6",
        defaultNodeColor: "#E1D804",
        defaultLabelSize: 14,
        borderSize: 1,
        edgeColor: "default",
        labelColor: "default",
        labelSize: "proportional",
        labelSizeRatio: 2,
        nodeBorderColor: "default",
        labelThreshold: 10, // The minimum size a node must have on screen to see its label displayed. This does not affect hovering behavior.
        defaultNodeBorderColor: "#000",//Any color of your choice
        defaultBorderView: "always", //apply the default color to all nodes always (normal+hover)
        minArrowSize: 8,
        scalingMode: "outside", // inside
        highlightCentralityNodeColor: '#EE3A8C',
        // Node overlap settings
        nodeMargin: 5,
        maxIterations: 100,
        gridSize: 30,
        // appearance of hovered nodes and edges
        nodeHoverColor: "#00B2EE",	
        edgeHoverColor: "#00B2EE",
        nodeClickColor: "#09a709",
        edgeClickColor: "#09a709",
        adjacentNodeHoverColor: "#00B2EE",
        // camera settings
        zoomRatio: 0.5
    }

    return (
        <Sigma
            renderer="webgl"
            graph={graph}
            settings={sigmaSettings}
            style={{maxWidth:"inherit", height:"100vh"}}
        >
            <ForceAtlas2 />
            <EdgeShapes default="arrow" />
            <RelativeSize initialSize={15}/>
            <RandomizeNodePositions/>
        </Sigma>
    );
};

export default Graph;