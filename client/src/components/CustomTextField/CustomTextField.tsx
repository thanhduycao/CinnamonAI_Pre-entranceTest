import React from "react"
import { alpha, styled } from "@mui/material/styles"
import { TextField, TextFieldProps } from "@mui/material"

const NoneOutlinedTextField = styled(TextField)({
    "& .MuiOutlinedInput-root": {
        "& fieldset": {
            borderColor: "transparent",
        },
        "&:hover fieldset": {
            borderColor: "transparent",
        },
        "&.Mui-focused fieldset": {
            borderColor: "transparent",
        },
    },
    width: "100%",
    maxHeight: "85%",
    overflowY: "auto",
})

export const CustomTextField = (props: TextFieldProps) => {
    return <NoneOutlinedTextField variant="outlined" {...props} />
}