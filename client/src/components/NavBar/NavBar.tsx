import React from 'react'
import { AppBar } from '@mui/material'
import { makeStyles } from '@mui/styles'

export const NavBar = () => {
  return (
    <AppBar position="static" sx={{ backgroundColor: "white", color: "black" }}>
      <h1>SummarizerBot</h1>
    </AppBar>
  )
}
