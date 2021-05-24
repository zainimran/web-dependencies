import React from 'react';
import { Link } from 'react-router-dom'
import { Row, Col, Divider, Button, Text, Spacer } from '@geist-ui/react'
import { Globe, Server } from '@geist-ui/react-icons'
import { useStoreState, useStoreActions } from 'easy-peasy'

const NavBar = () => {
    const service = useStoreState(state => state.service)
    const changeService = useStoreActions(actions => actions.changeService)
    const toggleNodeDetails = useStoreActions(actions => actions.toggleNodeDetails)

    const changeServiceHandler = (e) => {
        const service = e.target.innerText
        if (service != null) {
            changeService(service)
            toggleNodeDetails(false)
        }
    }
    
    return (
        <>
            <Row gap={.8} align="middle">
                <Col span={6}>
                    <Link to='/'><Text h3>Web Dependencies</Text></Link>
                </Col>
                <Col span={17}>
                    <Row justify="end">
                        <Link to='/dns' style={{ marginRight: '15px' }}>
                            <Button auto onClick={(e) => changeServiceHandler(e)}><Globe /><Spacer x={1} inline />DNS</Button>
                        </Link>
                        <Link to='/cdn' style={{ marginRight: '15px' }}>
                            <Button auto onClick={(e) => changeServiceHandler(e)}><Server /><Spacer x={1} inline />CDN</Button>
                        </Link>
                    </Row>
                </Col>
            </Row>
            <Divider style={{ marginBottom: '15px' }} />
        </>
    )
}

export default NavBar;
