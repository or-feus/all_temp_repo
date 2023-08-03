import {Box, Button, ButtonGroup} from "@mui/material";


export default function Button_3x3() {

    return (
        <>
            <Box
                sx={{

                    // width: '100%',
                    border: '1px solid',
                    display: 'block',
                    margin: 'auto',
                    textAlign: 'center'
            }}>
                <Box>
                    <Button>1</Button>
                    <Button>2</Button>
                    <Button>3</Button>
                </Box>
                <Box>
                    <Button>4</Button>
                    <Button>5</Button>
                    <Button>6</Button>
                </Box>
                <Box>
                    <Button>7</Button>
                    <Button>8</Button>
                    <Button>9</Button>
                </Box>
            </Box>
        </>
    )

}