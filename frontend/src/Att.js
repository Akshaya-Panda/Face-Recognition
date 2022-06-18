import React from 'react'

import {
    Table,
    Thead,
    Tbody,
    Tfoot,
    Tr,
    Th,
    Td,
    TableCaption,
    TableContainer,
  } from "@chakra-ui/react";

const Att = (att_key, att_value) => {
  return (
    <div>
    {att_key?.map((data, index) => (
        <Tr>
            <Td> {data}</Td>
        </Tr>
    ))}
    </div>
  )
}

export default Att