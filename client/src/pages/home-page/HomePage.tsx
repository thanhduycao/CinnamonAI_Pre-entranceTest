import React from 'react'
import { makeStyles } from '@mui/styles'
import { Summarizer } from './components/Summarizer'
import Grid from '@mui/material/Grid'

const useStyles = makeStyles({
  root: {
    height: '100vh',
    padding: '1rem',
    backgroundColor: '#f4f4f4'
  },
  summarizerContainer: {
    height: '100%'
  },
  summarizerGrid: {
    height: '80%',
    paddingLeft: '5rem',
    paddingRight: '5rem',
    paddingTop: '2rem',
  }
})

export const HomePage: React.FC = () => {
  const classes = useStyles()
  return (
    <div className={classes.root}>
      <Grid container className={classes.summarizerContainer}>
        <Grid item xs={12} className={classes.summarizerGrid}>
          <Summarizer />
        </Grid>
      </Grid>
    </div>
  )
}
