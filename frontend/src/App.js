import React, { useEffect } from 'react'
import './App.css';
import { GeistProvider, CssBaseline, Page, Text } from '@geist-ui/react'
import { Switch, Route } from "react-router-dom";
import { NavBar } from "./components";
import { Error, Graph } from './views'
import { useStoreState, useStoreActions } from 'easy-peasy'

const App = () => {
  const theme = useStoreState(state => state.theme)
  const toggleTheme = useStoreActions(actions => actions.toggleTheme)

  useEffect(() => {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      toggleTheme('dark')
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      const newColorScheme = e.matches ? 'dark' : 'light';
      toggleTheme(newColorScheme)
    });

    return () => {
      window.removeEventListener('change',  e => {
        const newColorScheme = e.matches ? 'dark' : 'light';
        toggleTheme(newColorScheme)
      });
    }
  }, [])

  return (
    <GeistProvider themeType={theme}>
      <CssBaseline />
      <Page size='large'>
        <NavBar /> 
        <Switch>
          <Route path='/dns'>
            <Graph type='dns' />
          </Route>
          <Route path='/cdn'>
            <Graph type='cdn' />
          </Route>
          <Route path='/'>
            <Text h5>Click any of the options above to view respective graphs</Text>
          </Route>
          <Route component={Error} />
        </Switch>
      </Page>
    </GeistProvider>
  );
}

export default App;