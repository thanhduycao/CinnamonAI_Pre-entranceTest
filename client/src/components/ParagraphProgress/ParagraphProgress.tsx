import React from 'react';
import { makeStyles } from '@mui/styles';
import { LinearProgress } from '@mui/material';

const useStyles = makeStyles({
    root: {
        width: '90%',
        height: '10%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        padding: '1rem',
    },
});

interface ParagraphProgressProps {
    isProcessing: boolean;
    numProgress: number;
}

export const ParagraphProgress: React.FC<ParagraphProgressProps> = (props): JSX.Element => {
    const classes = useStyles()
    const numProgressArray = Array.from({ length: props.numProgress })
    return (
        <div className={classes.root}>
            {numProgressArray.map((_, index) => {
                const width = `${100 - (index * 10)}%`
                return (
                    <LinearProgress
                        key={index}
                        color="secondary"
                        variant={props.isProcessing ? 'indeterminate' : 'buffer'}
                        sx={{ width: { width } }}
                        value={0}
                        valueBuffer={100} />
                )
            })}
        </div>
    )
}