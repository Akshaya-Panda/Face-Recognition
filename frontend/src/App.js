import "./App.css";
import { useState, useEffect } from "react";
import axios from "axios";
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
import { Button, ButtonGroup } from "@chakra-ui/react";
import { Center, Square, Circle } from "@chakra-ui/react";
import Footer from "./Footer";
import Navbar from "./Navbar";

import Att from "./Att";

function App() {
  const [studentData, setStudentData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(null);
  const [dv, setDv] = useState([]);

  const url = "http://15.206.212.52:8000/attendance";

  useEffect(() => {
    const getData = async () => {
      try {
        const response = await axios.get(
          `http://15.206.212.52:8000/attendance`
        );
        setStudentData(response.data.data);
        // setDv(response.data.data.date-key)
        setError(null);
        // console.log(response.data.data);

        var mainArr = [];
        for (var i = 0; i < studentData.length; i++) {
          console.log();
          mainArr.push(studentData[i]['date-key']);
        }
        // console.log(mainArr);
      } catch (err) {
        setError(err.message);
        setStudentData([]);
      } finally {
        setLoading(false);
      }
    };
    getData();
  }, []);

  function refreshPage() {
    window.location.reload(false);
  }

  return (
    <div className="App">
      <Navbar />
      <div>
        <TableContainer>
          <Table variant="striped">
            <TableCaption>Attendance</TableCaption>
            <Thead>
              <Tr>
                <Th>Roll</Th>
                <Th>Name</Th>
                <Th>Branch</Th>
                <Th>Batch</Th>
                <Th>Attendance</Th>
              </Tr>
            </Thead>
            <Tbody>
              {studentData?.map((data, index) => (
                <Tr>
                  <Td key={data?.id}> {data?._id}</Td>
                  <Td key={data?.id}> {data?.Name}</Td>
                  <Td key={data?.id}> {data?.Branch}</Td>
                  <Td key={data?.id}> {data?.batch}</Td>
                  <Td key={data?.id}>
                    <div className="att-box">
                      <div className="att-box-key">
                        {data['date-key'].map((dat, index) => (
                          <div>{`${dat} - `}</div>
                        ))}
                      </div>
                      <div className="att-box-value">
                        {data['date-value'].map((dat, index) => (
                          <div>{dat}</div>
                        ))}
                      </div>
                    </div>
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </TableContainer>
        <Center h="100px" color="white">
          <Button colorScheme="pink" onClick={refreshPage}>
            Refresh
          </Button>
        </Center>
        <Footer />
      </div>
    </div>
  );
}

export default App;
