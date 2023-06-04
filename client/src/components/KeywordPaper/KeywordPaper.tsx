import React from 'react'
import Paper from '@mui/material/Paper'
import Grid from '@mui/material/Grid'
import { styled } from '@mui/material/styles'
import { makeStyles } from '@mui/styles';

const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
}));

interface KeywordPaperProps {
    keywords: string[]
}

const useStyles = makeStyles({
    root: {
        width: '100%',
        maxHeight: '15%',
        overflowY: 'auto',
    },
    container: {
        padding: '10px',
    },
})

export const KeywordPaper: React.FC<KeywordPaperProps> = (props) => {
    const classes = useStyles()
    return (
        <Paper className={classes.root}>
            <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }} className={classes.container}>
                {props.keywords.map((keyword, index) => {
                    return (
                        <Grid item xs={2} sm={4} md={4} key={index}>
                            <Item>
                                {keyword}
                            </Item>
                        </Grid>
                    )
                }
                )}
            </Grid>
        </Paper>
    )
}