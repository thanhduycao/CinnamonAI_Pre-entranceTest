import React from "react";
import { alpha, styled } from "@mui/material/styles";
import { Button, ButtonProps } from "@mui/material";

const BorderButton = styled(Button)<ButtonProps>(({ theme }) => ({
    color: theme.palette.getContrastText("#178733"),
    backgroundColor: "#178733",
    borderRadius: 20,
    textTransform: "none",
    fontWeight: "600px",
    "&:hover": {
        backgroundColor: alpha("#178733", 0.75),
    },
}));

export const CustomSummarizeButton = (props: ButtonProps) => {
    return (
        <BorderButton variant="outlined" {...props}>
            {props.children}
        </BorderButton>
    );
}