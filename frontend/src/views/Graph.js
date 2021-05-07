import React from 'react'
import { Sigma, RelativeSize, RandomizeNodePositions, EdgeShapes, ForceAtlas2, Filter, NOverlap } from 'react-sigma'
import Dagre from 'react-sigma/lib/Dagre'
import ForceLink from 'react-sigma/lib/ForceLink'
import { SigmaLoader } from '../components'
import { useStoreState, useStoreActions } from 'easy-peasy'
import { Row, Col, Text, Select, Spacer, Input } from '@geist-ui/react'
import Search from '@geist-ui/react-icons/search'

const Graph = () => {
    const theme = useStoreState(state => state.theme)
    const service = useStoreState(state => state.service)
    const graph = useStoreState(state => state.graph)
    const changeGraph = useStoreActions(actions => actions.changeGraph)
    const node = useStoreState(state => state.node)
    const setNode = useStoreActions(actions => actions.setNode)
    const searchTerm = useStoreState(state => state.searchTerm)
    const setTerm = useStoreActions(actions => actions.setTerm)

    let graphData

    if (service == 'dns') graphData = require('../data/dummy.json')
    else if (service == 'cdn') graphData = require('../data/dummy.json')

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
        defaultLabelColor: (theme == 'light') ? "#000" : "#FFF",
        defaultEdgeColor: "#d3d3d3",
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

    let graphComponent = <></>
    if (graph == 'forceatlas2') graphComponent = <ForceAtlas2 iterationsPerRender={1} barnesHutOptimize barnesHutTheta={1} slowDown={10} timeout={2000} worker key={`${service}1`} />
    else if (graph == 'dagre') graphComponent = <Dagre boundingBox={{ maxX: 10, maxY: 10, minX: 0, minY: 0 }} easing="cubicInOut" rankDir="LR" key={`${service}1`} />
    else if (graph == 'forcelink') graphComponent = <ForceLink background easing="cubicInOut" iterationsPerRender={1} linLogMode timeout={1000} worker key={`${service}1`} />
    else if (graph == 'noverlap') graphComponent = <NOverlap duration={3000} easing="quadraticInOut" gridSize={20} maxIterations={100} nodeMargin={10} scaleNodes={4} speed={10} /> 

    const searchNode = e => setTerm(e.target.value)

    const nodesFilter = n => {
        if (searchTerm) return n.label.toLowerCase().includes(searchTerm)
        return true
    }

    return (
        <Row gap={.8}>
            <Col span={4}>
                <Text>Select graph type</Text>
                <Select initialValue="forceatlas2" onChange={value => changeGraph(value)}>
                    <Select.Option value="forceatlas2">ForceAtlas2</Select.Option>
                    <Select.Option value="dagre">Dagre</Select.Option>
                    <Select.Option value="forcelink">ForceLink</Select.Option>
                    <Select.Option value="noverlap">NOverlap</Select.Option>
                </Select>
                <Spacer />
                <Text>Search for a node</Text>
                <Input icon={<Search />} placeholder="Search..." clearable value={searchTerm} onChange={searchNode} />
            </Col>
            <Col span={20}>
                <Sigma renderer="canvas" settings={sigmaSettings} style={{maxWidth:"inherit", height:"80vh"}} onClickNode={ e => setNode(e.data.node.id) } onClickStage={ e => setNode(null) }>
                    <SigmaLoader graph={graphData}>
                        <Filter nodesBy={nodesFilter} neighborsOf={node} />
                        { graphComponent }
                        <EdgeShapes default="dashed" key={`${service}2`} />
                        <RelativeSize initialSize={15} key={`${service}3`} />
                        <RandomizeNodePositions key={`${service}4`} />
                    </SigmaLoader>
                </Sigma>
            </Col>
        </Row>
    );
};

export default Graph;